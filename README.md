[![Stars](https://img.shields.io/github/stars/zhihao12/qx-rules)](https://github.com/zhihao12/qx-rules/stargazers)
[![Fork](https://img.shields.io/github/forks/zhihao12/qx-rules)](https://github.com/zhihao12/qx-rules/network/members)
[![Commit](https://img.shields.io/github/commit-activity/m/zhihao12/qx-rules?label=Commits)](https://github.com/zhihao12/qx-rules/commits/main)
[![](https://img.shields.io/github/last-commit/zhihao12/qx-rules)](https://github.com/zhihao12/qx-rules/commits/main)
![Rules](https://img.shields.io/badge/Rules-220333-brightgreen)
![Update](https://img.shields.io/badge/Update-每日自动-blue)

## qx-rules

自用的 Quantumult X 分流规则合集。每天由生成器自动拉取各公开规则源，合并、跨表去重、消解影子规则后推送到本仓库，共 19 张表、220,333 条规则。

- 每张表对应配置里的一个策略组，订阅时用 `force-policy` 指定去向
- `ai.list` 为原生三段格式（行尾带策略，资源解析器关闭时使用），其余为两段格式
- 每张表的生成时间与条数见文件头注释

## 0️⃣ 懒人配置

整份配置：[QuantumultX.conf](https://raw.githubusercontent.com/zhihao12/qx-rules/main/QuantumultX.conf)

与维护者自用版同一套分流架构，已脱敏处理：导入后在 `[server_remote]` 填入你自己的机场订阅、在 QX 里生成你自己的 MITM 证书即可使用。分流表全部引用本仓库，每日自动更新。

## 1️⃣ 分流规则

| 分流 | 对应 App / 网站 | 条数 |
| --- | --- | ---: |
| [广告终结者](https://raw.githubusercontent.com/zhihao12/qx-rules/main/adblock.list) | 全网广告、追踪与弹窗域名 | 210,647 |
| [国内网站](https://raw.githubusercontent.com/zhihao12/qx-rules/main/asn.list) | 国内站点 IP 段，走直连 | 5,076 |
| [苹果服务](https://raw.githubusercontent.com/zhihao12/qx-rules/main/apple.list) | App Store、iCloud、Apple Music、系统推送 | 1,870 |
| [Google](https://raw.githubusercontent.com/zhihao12/qx-rules/main/google.list) | Google 搜索、Gmail、Google Play 等谷歌服务 | 864 |
| [流媒体](https://raw.githubusercontent.com/zhihao12/qx-rules/main/streaming.list) | YouTube、Netflix、Disney+、Max、Prime Video 等影音平台 | 426 |
| [兜底分流](https://raw.githubusercontent.com/zhihao12/qx-rules/main/fallback.list) | 没被其他表命中的境外域名 | 398 |
| [Ai](https://raw.githubusercontent.com/zhihao12/qx-rules/main/ai.list) | ChatGPT、Claude、Gemini、Copilot 等 AI 服务 | 308 |
| [交易所](https://raw.githubusercontent.com/zhihao12/qx-rules/main/crypto.list) | Binance、OKX、Bybit、Coinbase 等交易所与钱包 | 243 |
| [红果去广告](https://raw.githubusercontent.com/zhihao12/qx-rules/main/hongguo.list) | 红果短剧、番茄小说的广告域名 | 126 |
| [Telegram](https://raw.githubusercontent.com/zhihao12/qx-rules/main/telegram.list) | Telegram、Swiftgram 等客户端 | 65 |
| [直连](https://raw.githubusercontent.com/zhihao12/qx-rules/main/direct.list) | 银行、支付与微信 | 57 |
| [TikTok](https://raw.githubusercontent.com/zhihao12/qx-rules/main/tiktok.list) | TikTok | 57 |
| [Meta](https://raw.githubusercontent.com/zhihao12/qx-rules/main/meta.list) | Facebook、Instagram、Threads、Messenger、WhatsApp、Meta AI | 51 |
| [Spotify](https://raw.githubusercontent.com/zhihao12/qx-rules/main/spotify.list) | Spotify | 37 |
| [规则修正](https://raw.githubusercontent.com/zhihao12/qx-rules/main/unbreak.list) | 被广告表误伤的域名放行 | 33 |
| [Github分流](https://raw.githubusercontent.com/zhihao12/qx-rules/main/proxy.list) | GitHub 及相关域名 | 31 |
| [X](https://raw.githubusercontent.com/zhihao12/qx-rules/main/x.list) | X（原 Twitter） | 31 |
| [哔哩哔哩](https://raw.githubusercontent.com/zhihao12/qx-rules/main/bilibili.list) | 哔哩哔哩 | 11 |
| [狂野飙车](https://raw.githubusercontent.com/zhihao12/qx-rules/main/gameloft.list) | 狂野飙车 9 | 2 |

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
