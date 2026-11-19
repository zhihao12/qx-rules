#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gen.py — QX 自建订阅生成器（纯标准库，盒子上独立运行）

输入（均在本脚本同目录）：
  sources.yaml    outputs（目标表清单）+ sources（上游源清单）
  overrides.yaml  rules（自现行配置 filter_local 提取的本地覆盖规则）
输出：
  out/<file>      按策略组分开的 .list 表
  cache/<id>.txt  上游源的最近一次成功拉取副本
  gen.log         每次运行追加一行统计

YAML 子集说明（本脚本自带极简解析器，只支持这一种形状）：
  顶层键以 `key:` 起始，其值是若干扁平字典组成的列表；
  列表项以 `  - k: v` 起始，后续键以 `    k: v` 缩进；
  值是纯标量，按第一个 `: ` 切分键与值，值可为空；
  `true/false` 读作布尔，纯数字读作整数，其余读作字符串；
  `#` 起始行与空行忽略。不要在这个子集里写嵌套结构或引号字符串。

合并与去重语义：
  全局序 = overrides（按文件顺序）在前，sources（按清单顺序）在后，
  与现行配置「filter_local 优先、filter_remote 按文件顺序」一致。
  沿全局序维护已认领的 host-suffix / host 集合：
    后出现的 host-suffix 若等于或隶属于已认领后缀，整条丢弃（影子消解）；
    后出现的 host 若已被认领或隶属于已认领后缀，丢弃；
  这类规则在旧顺序里永远不会命中，丢弃不改变任何去向。
  host-keyword / host-wildcard / user-agent / ip-asn / ip-cidr / ip6-cidr
  为异型透传：不参与后缀去重，只去掉同表内完全重复条目。

失败策略：任一源拉不到且无缓存，或任一输出表为空，则整轮放弃，
不改动 out/ 里任何现有文件，退出码非 0。单表写入用临时文件加改名，
不会留下写一半的表。
"""

import os
import sys
import time
import urllib.request
from datetime import datetime

BASE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(BASE, "out")
CACHE_DIR = os.path.join(BASE, "cache")
LOG_PATH = os.path.join(BASE, "gen.log")

QX_TYPES = {
    "HOST": "host",
    "HOST-SUFFIX": "host-suffix",
    "HOST-KEYWORD": "host-keyword",
    "HOST-WILDCARD": "host-wildcard",
    "IP-CIDR": "ip-cidr",
    "IP6-CIDR": "ip6-cidr",
    "IP-CIDR6": "ip6-cidr",
    "IP-ASN": "ip-asn",
    "USER-AGENT": "user-agent",
}
SURGE_TYPES = {
    "DOMAIN": "host",
    "DOMAIN-SUFFIX": "host-suffix",
    "DOMAIN-KEYWORD": "host-keyword",
    "IP-CIDR": "ip-cidr",
    "IP-CIDR6": "ip6-cidr",
    "USER-AGENT": "user-agent",
}
VERBATIM_TYPES = {"user-agent", "host-wildcard", "ip-asn"}
DOMAIN_TYPES = {"host", "host-suffix", "host-keyword", "host-wildcard"}


# ---------- 极简 YAML 子集解析 ----------

def _scalar(text):
    if text == "":
        return ""
    if text == "true":
        return True
    if text == "false":
        return False
    if text.lstrip("-").isdigit():
        return int(text)
    return text


def parse_simple_yaml(path):
    doc = {}
    current_key = None
    current_item = None
    with open(path, encoding="utf-8") as fh:
        for raw in fh:
            line = raw.rstrip("\n")
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            if not line.startswith(" "):
                # 顶层键
                key = stripped[:-1] if stripped.endswith(":") else stripped
                current_key = key
                doc[current_key] = []
                current_item = None
                continue
            if stripped.startswith("- "):
                current_item = {}
                doc[current_key].append(current_item)
                stripped = stripped[2:]
            if current_item is None:
                raise ValueError("YAML 子集解析失败（列表项外出现键值）: %s" % line)
            if ": " in stripped:
                k, v = stripped.split(": ", 1)
            elif stripped.endswith(":"):
                k, v = stripped[:-1], ""
            else:
                raise ValueError("YAML 子集解析失败（无键值分隔）: %s" % line)
            current_item[k.strip()] = _scalar(v.strip())
    return doc


# ---------- 规则解析 ----------

def parse_rule_line(line, fmt):
    """返回 dict(type, value, policy, extra, raw) 或 None（注释/空行/无法识别）。"""
    text = line.strip()
    if not text or text.startswith("#") or text.startswith("//") or text.startswith(";"):
        return None
    parts = [p.strip() for p in text.split(",")]
    table = SURGE_TYPES if fmt == "surge" else QX_TYPES
    rtype = table.get(parts[0].upper())
    if rtype is None or len(parts) < 2:
        return None
    if rtype == "ip-asn":
        value = parts[1].split("//")[0].strip()
        return {"type": rtype, "value": value, "policy": None, "extra": [], "raw": text}
    value = parts[1]
    if rtype in DOMAIN_TYPES and rtype != "user-agent":
        value = value.lower()
    rest = parts[2:]
    if fmt == "surge":
        policy, extra = None, rest
    else:
        policy = rest[0] if rest else None
        extra = rest[1:] if len(rest) > 1 else []
    return {"type": rtype, "value": value, "policy": policy, "extra": extra, "raw": text}


def ancestors_or_self(domain):
    parts = domain.split(".")
    return [".".join(parts[i:]) for i in range(len(parts))]


# ---------- 拉取 ----------

def fetch_source(src):
    """返回 (text, status)：status 为 live 或 cache；失败抛异常。"""
    cache_path = os.path.join(CACHE_DIR, src["id"] + ".txt")
    req = urllib.request.Request(src["url"], headers={"User-Agent": "Mozilla/5.0 (qx-selfhost-gen)"})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = resp.read().decode("utf-8", errors="replace")
        if not data.strip() or data.lstrip().startswith("<"):
            raise ValueError("拉取内容不像规则表")
        tmp = cache_path + ".tmp"
        with open(tmp, "w", encoding="utf-8") as fh:
            fh.write(data)
        os.replace(tmp, cache_path)
        return data, "live"
    except Exception:
        if os.path.exists(cache_path):
            with open(cache_path, encoding="utf-8") as fh:
                return fh.read(), "cache"
        raise


# ---------- 主流程 ----------

def main():
    started = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sources_doc = parse_simple_yaml(os.path.join(BASE, "sources.yaml"))
    overrides_doc = parse_simple_yaml(os.path.join(BASE, "overrides.yaml"))
    outputs = sources_doc["outputs"]
    sources = sources_doc["sources"]
    out_names = [o["file"] for o in outputs]
    os.makedirs(OUT_DIR, exist_ok=True)
    os.makedirs(CACHE_DIR, exist_ok=True)

    # 全局序规则流：overrides 在前，sources 在后
    stream = []          # 每条：dict(out,type,value,effpolicy,extra,raw,origin)
    fetch_status = {}
    for item in overrides_doc.get("rules", []):
        stream.append({
            "out": item["out"], "type": item["type"], "value": str(item["value"]),
            "effpolicy": item["policy"], "extra": [], "raw": None, "origin": "overrides",
        })
    for src in sources:
        try:
            text, status = fetch_source(src)
        except Exception as exc:
            print("ABORT: source %s 拉取失败且无缓存: %s" % (src["id"], exc))
            return 2
        fetch_status[src["id"]] = status
        parsed = 0
        for line in text.splitlines():
            rule = parse_rule_line(line, src["format"])
            if rule is None:
                continue
            parsed += 1
            eff = src.get("force_policy") or rule["policy"]
            stream.append({
                "out": src["out"], "type": rule["type"], "value": rule["value"],
                "effpolicy": eff, "extra": rule["extra"], "raw": rule["raw"],
                "origin": src["id"],
            })
        if parsed == 0:
            print("ABORT: source %s 解析出 0 条规则" % src["id"])
            return 2

    # 广告表清理名单（可选）：prune.txt 与本脚本同目录，每行一个域名，
    # 由离线检测生成（僵尸域名加极小众域名）。仅作用于 adblock.list 的
    # host / host-suffix 规则：规则域名自身或任一父域在名单内即剔除。
    # 在影子消解之前过滤，被剔除的父域不再遮蔽名单外的子域规则。
    prune_count = 0
    prune_path = os.path.join(BASE, "prune.txt")
    if os.path.exists(prune_path):
        prune_set = set()
        with open(prune_path, encoding="utf-8") as fh:
            for line in fh:
                d = line.strip().lower()
                if d and not d.startswith("#"):
                    prune_set.add(d)
        if prune_set:
            filtered = []
            for rule in stream:
                if rule["out"] == "adblock.list" and rule["type"] in ("host", "host-suffix") and any(
                    a in prune_set for a in ancestors_or_self(rule["value"])
                ):
                    prune_count += 1
                    continue
                filtered.append(rule)
            stream = filtered

    # 影子消解 + 透传去重（沿全局序）
    claimed_suf = set()
    claimed_host = set()
    seen_passthrough = set()
    kept = {name: [] for name in out_names}
    stats = {name: {"kept": 0, "shadow": 0, "dup": 0, "by_origin": {}} for name in out_names}
    for rule in stream:
        st = stats[rule["out"]]
        rtype = rule["type"]
        if rtype == "host-suffix":
            if any(a in claimed_suf for a in ancestors_or_self(rule["value"])):
                st["shadow"] += 1
                continue
            claimed_suf.add(rule["value"])
        elif rtype == "host":
            if rule["value"] in claimed_host or any(
                a in claimed_suf for a in ancestors_or_self(rule["value"])
            ):
                st["shadow"] += 1
                continue
            claimed_host.add(rule["value"])
        else:
            key = (rule["out"], rtype, rule["value"])
            if key in seen_passthrough:
                st["dup"] += 1
                continue
            seen_passthrough.add(key)
        kept[rule["out"]].append(rule)
        st["kept"] += 1
        st["by_origin"][rule["origin"]] = st["by_origin"].get(rule["origin"], 0) + 1

    for name in out_names:
        if stats[name]["kept"] == 0:
            print("ABORT: output %s 为空表，整轮放弃" % name)
            return 3

    # opt_parser 为 false 的表（如 ai.list）QX 按原生格式逐行解析，行内必须带策略，
    # 生成时把 force_policy 补回行尾；其余表维持两段式（由 force-policy 统一指定）
    policy_of = {}
    for o in outputs:
        if str(o.get("opt_parser", "true")).strip().lower() == "false":
            policy_of[o["file"]] = o.get("force_policy", "")

    # 落盘（临时文件 + 改名）
    for output in outputs:
        name = output["file"]
        lines = [
            "# %s | 自建订阅表（gen.py 生成，勿手改）" % name,
            "# generated: %s" % started,
            "# rules: %d" % stats[name]["kept"],
        ]
        for rule in kept[name]:
            lines.append(emit_line(rule, policy_of.get(name)))
        tmp_path = os.path.join(OUT_DIR, ".tmp-" + name)
        with open(tmp_path, "w", encoding="utf-8") as fh:
            fh.write("\n".join(lines) + "\n")
        os.replace(tmp_path, os.path.join(OUT_DIR, name))

    summary_parts = []
    for name in out_names:
        st = stats[name]
        comp = ",".join("%s=%d" % (k, v) for k, v in sorted(st["by_origin"].items()))
        part = "%s kept=%d shadow=%d dup=%d [%s]" % (name, st["kept"], st["shadow"], st["dup"], comp)
        if name == "adblock.list" and prune_count:
            part += " pruned=%d" % prune_count
        summary_parts.append(part)
    fetch_part = ",".join("%s=%s" % (k, v) for k, v in sorted(fetch_status.items()))
    log_line = "%s OK | %s | fetch: %s" % (started, " | ".join(summary_parts), fetch_part)
    print(log_line)
    with open(LOG_PATH, "a", encoding="utf-8") as fh:
        fh.write(log_line + "\n")
    return 0


def emit_line(rule, policy=None):
    rtype = rule["type"]
    if rtype in VERBATIM_TYPES:
        if rule["raw"]:
            return rule["raw"]
        return "%s, %s" % (rtype, rule["value"])
    if rtype in ("ip-cidr", "ip6-cidr"):
        if rule["extra"]:
            return "%s, %s, %s, %s" % (rtype, rule["value"], rule["effpolicy"], ", ".join(rule["extra"]))
        if policy:
            return "%s, %s, %s" % (rtype, rule["value"], policy)
        return "%s, %s" % (rtype, rule["value"])
    if policy:
        return "%s, %s, %s" % (rtype, rule["value"], policy)
    return "%s, %s" % (rtype, rule["value"])


if __name__ == "__main__":
    sys.exit(main())
