#!/bin/sh
# 广告表清理名单月度复检：刷新上游缓存，提取三源并集域名，两轮 DNS
# 存活检测，重建 prune.txt，再生成并推送。盒子 cron 每月 20 日运行。
cd /usr/local/share/qx-rules || exit 1
exec >> monthly_prune.log 2>&1
echo "=== monthly prune $(date) ==="
python3 gen.py || exit 1
python3 build_domains.py || exit 1
python3 dnscheck.py domains.txt verdicts_r1.tsv || exit 1
awk -F'\t' '$2!="A"{print $1}' verdicts_r1.tsv > recheck.txt
python3 dnscheck.py recheck.txt verdicts_r2.tsv || exit 1
python3 build_prune.py || exit 1
python3 gen.py || exit 1
cp prune.txt repo/prune.txt
cp zombies.txt repo/zombies.txt 2>/dev/null
cp niche.txt repo/niche.txt 2>/dev/null
./push.sh
echo "=== done $(date) ==="
