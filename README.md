# qx-rules

Quantumult X 分流规则表合集，由生成器每日自动合并公开规则源、去重后推送。

- 每张表对应配置里的一个策略组，订阅时用 `force-policy` 指定去向
- `ai.list` 为原生三段格式（行尾带策略），其余为两段格式
- 生成时间见每张表文件头注释

| 文件 | 去向 |
| --- | --- |
| adblock.list | reject |
| ai.list | Ai |
| apple.list | 苹果服务 |
| asn.list | direct |
| bilibili.list | 哔哩哔哩 |
| crypto.list | 交易所 |
| direct.list | direct |
| fallback.list | 兜底分流 |
| gameloft.list | 狂野飙车 |
| google.list | Google |
| hongguo.list | reject（逐行策略） |
| meta.list | Meta |
| proxy.list | proxy |
| spotify.list | Spotify |
| streaming.list | 流媒体 |
| telegram.list | Telegram |
| tiktok.list | TikTok |
| unbreak.list | direct |
| x.list | X |
| youtube.list | 流媒体 |
