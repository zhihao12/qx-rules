#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""从 gen.py 的上游缓存提取三源并集域名，供月度存活检测使用。

输入：cache/adrules.txt、cache/bm7ads.txt、cache/heidai.txt
输出：domains.txt（去重排序后的 host / host-suffix 值）
"""
import os

BASE = os.path.dirname(os.path.abspath(__file__))


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


def main():
    out = set()
    for name in ("adrules", "bm7ads", "heidai"):
        out |= values(os.path.join(BASE, "cache", name + ".txt"))
    with open(os.path.join(BASE, "domains.txt"), "w", encoding="utf-8") as f:
        for d in sorted(out):
            f.write(d + "\n")
    print("domains: %d" % len(out))


if __name__ == "__main__":
    main()
