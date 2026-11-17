[![Stars](https://img.shields.io/github/stars/zhihao12/qx-rules)](https://github.com/zhihao12/qx-rules/stargazers)
[![Fork](https://img.shields.io/github/forks/zhihao12/qx-rules)](https://github.com/zhihao12/qx-rules/network/members)
[![Commit](https://img.shields.io/github/commit-activity/m/zhihao12/qx-rules?label=Commits)](https://github.com/zhihao12/qx-rules/commits/main)
[![](https://img.shields.io/github/last-commit/zhihao12/qx-rules)](https://github.com/zhihao12/qx-rules/commits/main)
![Rules](https://img.shields.io/badge/Rules-220334-brightgreen)
![Update](https://img.shields.io/badge/Update-每日自动-blue)

## QX 规则自留地

自用的 Quantumult X 分流规则合集。每天由生成器自动拉取各公开规则源，合并、跨表去重、消解影子规则后推送到本仓库，共 20 张表、220,334 条规则。

- 每张表对应配置里的一个策略组，订阅时用 `force-policy` 指定去向
- `ai.list` 为原生三段格式（行尾带策略，资源解析器关闭时使用），其余为两段格式
- 每张表的生成时间与条数见文件头注释

## 1️⃣ 分流规则

| 表 | 去向 | 条数 |
| --- | --- | ---: |
| [adblock.list](https://raw.githubusercontent.com/zhihao12/qx-rules/main/adblock.list) | reject | 210,647 |
| [apple.list](https://raw.githubusercontent.com/zhihao12/qx-rules/main/apple.list) | 苹果服务 | 1,870 |
| [asn.list](https://raw.githubusercontent.com/zhihao12/qx-rules/main/asn.list) | direct | 5,076 |
| [google.list](https://raw.githubusercontent.com/zhihao12/qx-rules/main/google.list) | Google | 864 |
| [fallback.list](https://raw.githubusercontent.com/zhihao12/qx-rules/main/fallback.list) | 兜底分流 | 398 |
| [ai.list](https://raw.githubusercontent.com/zhihao12/qx-rules/main/ai.list) | Ai | 308 |
| [streaming.list](https://raw.githubusercontent.com/zhihao12/qx-rules/main/streaming.list) | 流媒体 | 257 |
| [crypto.list](https://raw.githubusercontent.com/zhihao12/qx-rules/main/crypto.list) | 交易所 | 243 |
| [youtube.list](https://raw.githubusercontent.com/zhihao12/qx-rules/main/youtube.list) | 流媒体 | 170 |
| [hongguo.list](https://raw.githubusercontent.com/zhihao12/qx-rules/main/hongguo.list) | reject（逐行策略） | 126 |
| [telegram.list](https://raw.githubusercontent.com/zhihao12/qx-rules/main/telegram.list) | Telegram | 65 |
| [direct.list](https://raw.githubusercontent.com/zhihao12/qx-rules/main/direct.list) | direct | 57 |
| [tiktok.list](https://raw.githubusercontent.com/zhihao12/qx-rules/main/tiktok.list) | TikTok | 57 |
| [meta.list](https://raw.githubusercontent.com/zhihao12/qx-rules/main/meta.list) | Meta | 51 |
| [spotify.list](https://raw.githubusercontent.com/zhihao12/qx-rules/main/spotify.list) | Spotify | 37 |
| [unbreak.list](https://raw.githubusercontent.com/zhihao12/qx-rules/main/unbreak.list) | direct | 33 |
| [proxy.list](https://raw.githubusercontent.com/zhihao12/qx-rules/main/proxy.list) | proxy | 31 |
| [x.list](https://raw.githubusercontent.com/zhihao12/qx-rules/main/x.list) | X | 31 |
| [bilibili.list](https://raw.githubusercontent.com/zhihao12/qx-rules/main/bilibili.list) | 哔哩哔哩 | 11 |
| [gameloft.list](https://raw.githubusercontent.com/zhihao12/qx-rules/main/gameloft.list) | 狂野飙车 | 2 |

## 2️⃣ 在 Quantumult X 里引用

```ini
[filter_remote]
https://raw.githubusercontent.com/zhihao12/qx-rules/main/ai.list, tag=Ai, force-policy=Ai, update-interval=172800, opt-parser=false, enabled=true
https://raw.githubusercontent.com/zhihao12/qx-rules/main/meta.list, tag=Meta, force-policy=Meta, update-interval=172800, opt-parser=true, enabled=true
```

其余表同理，把文件名与 `force-policy` 换成上表对应的去向即可。

## 3️⃣ 更新方式

- 生成器每天北京时间约 06:23 自动运行：拉取上游源，合并去重后推送
- 任一源拉取失败时保留上一版，绝不写空表
- 本地例外与补遗规则（Meta 全家、交易所补遗、Telegram 客户端域名等）随生成器一并合入
