#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""由两轮 DNS 检测结果生成清理名单（zombies.txt / niche.txt / prune.txt）。

僵尸：两轮都返回 NXDOMAIN 才算。安全闸：僵尸数超过受检域名的 40%
视为解析侧异常，整轮放弃、旧名单不动，退出码 1。
极小众（轻档）：仅一家源覆盖、母域名不在 Umbrella 百万榜、四段以上
深层域名。Umbrella 拉取失败时保留上一份 niche.txt。
"""
import io
import os
import sys
import urllib.request
import zipfile

BASE = os.path.dirname(os.path.abspath(__file__))
UMBRELLA_URL = "https://s3-us-west-1.amazonaws.com/umbrella-static/top-1m.csv.zip"
TWO_LEVEL = {
    "co.uk", "com.cn", "com.tw", "co.jp", "com.hk", "com.au", "co.kr",
    "com.br", "co.in", "com.mx", "com.sg", "com.my", "co.nz", "co.za",
    "com.ar", "com.tr", "com.vn", "com.ph", "co.id", "com.co", "com.pe",
    "com.uy", "com.ec", "com.do", "ac.uk", "gov.uk", "edu.cn", "com.ua",
    "com.pk", "com.ng", "com.eg",
}


def load_tsv(path):
    d = {}
    with open(path, encoding="utf-8", errors="replace") as f:
        for line in f:
            p = line.rstrip("\n").split("\t")
            if len(p) == 2:
                d[p[0]] = p[1]
    return d


def values(path):
    s = set()
    with open(path, encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            p = [x.strip().lower() for x in line.split(",")]
            if len(p) >= 2 and p[0] in ("host", "host-suffix"):
                s.add(p[1])
    return s


def etld1(d):
    parts = d.split(".")
    if len(parts) <= 2:
        return d
    if ".".join(parts[-2:]) in TWO_LEVEL and len(parts) >= 3:
        return ".".join(parts[-3:])
    return ".".join(parts[-2:])


def covered_by(v, table):
    parts = v.split(".")
    for i in range(len(parts) - 1):
        if ".".join(parts[i:]) in table:
            return True
    return False


def main():
    r1 = load_tsv(os.path.join(BASE, "verdicts_r1.tsv"))
    r2 = load_tsv(os.path.join(BASE, "verdicts_r2.tsv"))
    zombies = sorted(d for d, v in r1.items() if v == "D" and r2.get(d) == "D")
    if len(zombies) > 0.40 * max(1, len(r1)):
        print("ABORT: zombies %d 超过受检 %d 的 40%%，疑似解析异常，保留旧名单"
              % (len(zombies), len(r1)))
        return 1
    with open(os.path.join(BASE, "zombies.txt"), "w", encoding="utf-8") as f:
        for d in zombies:
            f.write(d + "\n")
    print("zombies: %d" % len(zombies))

    niche = None
    try:
        req = urllib.request.Request(UMBRELLA_URL, headers={"User-Agent": "Mozilla/5.0"})
        data = urllib.request.urlopen(req, timeout=120).read()
        zf = zipfile.ZipFile(io.BytesIO(data))
        umb = set()
        for raw in io.TextIOWrapper(zf.open("top-1m.csv"), encoding="utf-8", errors="replace"):
            parts = raw.strip().split(",", 1)
            if len(parts) == 2:
                umb.add(parts[1].lower())
        src = {n: values(os.path.join(BASE, "cache", n + ".txt"))
               for n in ("adrules", "bm7ads", "heidai")}
        pool = set()
        for table in src.values():
            pool |= table
        niche = []
        for v in pool:
            if v.count(".") < 3:
                continue
            cnt = sum(1 for table in src.values() if covered_by(v, table))
            if cnt == 1 and v not in umb and etld1(v) not in umb:
                niche.append(v)
        niche.sort()
        print("niche recomputed: %d" % len(niche))
    except Exception as exc:
        print("niche recompute failed (%s), keeping previous niche.txt" % exc)
    if niche is not None:
        with open(os.path.join(BASE, "niche.txt"), "w", encoding="utf-8") as f:
            for d in niche:
                f.write(d + "\n")
    else:
        prev = os.path.join(BASE, "niche.txt")
        niche = []
        if os.path.exists(prev):
            with open(prev, encoding="utf-8") as f:
                niche = [line.strip() for line in f if line.strip()]

    prune = sorted(set(zombies) | set(niche))
    with open(os.path.join(BASE, "prune.txt"), "w", encoding="utf-8") as f:
        f.write("# adblock 清理名单：两轮 DNS 检测确认的僵尸域名 + 极小众轻档（四段以上深层域名）\n")
        f.write("# 由 build_prune.py 每月自动生成，gen.py 消费（仅作用于 adblock.list）\n")
        for d in prune:
            f.write(d + "\n")
    print("prune total: %d (zombies %d + niche %d - overlap %d)"
          % (len(prune), len(zombies), len(niche), len(set(zombies) & set(niche))))
    return 0


if __name__ == "__main__":
    sys.exit(main())
