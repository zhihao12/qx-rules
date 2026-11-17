[![Stars](https://img.shields.io/github/stars/zhihao12/qx-rules)](https://github.com/zhihao12/qx-rules/stargazers)
[![Fork](https://img.shields.io/github/forks/zhihao12/qx-rules)](https://github.com/zhihao12/qx-rules/network/members)
[![Commit](https://img.shields.io/github/commit-activity/m/zhihao12/qx-rules?label=Commits)](https://github.com/zhihao12/qx-rules/commits/main)
[![](https://img.shields.io/github/last-commit/zhihao12/qx-rules)](https://github.com/zhihao12/qx-rules/commits/main)
![Rules](https://img.shields.io/badge/Rules-220923-brightgreen)
![Update](https://img.shields.io/badge/Update-每日自动-blue)

## qx-rules

自用的 Quantumult X 分流规则合集。每天由生成器自动拉取各公开规则源，合并、跨表去重、消解影子规则后推送到本仓库，共 19 张表、220,923 条规则。

- 每张表对应配置里的一个策略组，订阅时用 `force-policy` 指定去向
- `ai.list` 为原生三段格式（行尾带策略，资源解析器关闭时使用），其余为两段格式
- 每张表的生成时间与条数见文件头注释

## 0️⃣ 懒人配置

整份配置：[QuantumultX.conf](https://raw.githubusercontent.com/zhihao12/qx-rules/main/QuantumultX.conf)

与维护者自用版同一套分流架构，已脱敏处理：导入后在 `[server_remote]` 填入你自己的机场订阅、在 QX 里生成你自己的 MITM 证书即可使用。分流表全部引用本仓库，每日自动更新；重写见第 4 节，懒人配置里已整套带上。

## 1️⃣ 分流规则

| 分流 | 对应 App / 网站 | 来源 | 条数 |
| --- | --- | --- | ---: |
| [广告终结者](https://raw.githubusercontent.com/zhihao12/qx-rules/main/adblock.list) | 全网广告、追踪与弹窗域名 | [Cats-Team/AdRules](https://github.com/Cats-Team/AdRules) | 210,647 |
| [国内网站](https://raw.githubusercontent.com/zhihao12/qx-rules/main/asn.list) | 国内站点 IP 段，走直连 | [VirgilClyne/GetSomeFries](https://github.com/VirgilClyne/GetSomeFries) | 5,076 |
| [苹果服务](https://raw.githubusercontent.com/zhihao12/qx-rules/main/apple.list) | App Store、iCloud、Apple Music、系统推送 | [blackmatrix7](https://github.com/blackmatrix7/ios_rule_script) | 1,870 |
| [Google](https://raw.githubusercontent.com/zhihao12/qx-rules/main/google.list) | Google 搜索、Gmail、Google Play 等谷歌服务 | [MagicRule](https://magicrule.pages.dev) | 864 |
| [游戏](https://raw.githubusercontent.com/zhihao12/qx-rules/main/games.list) | Steam、Epic、PlayStation、Xbox、Nintendo 等游戏平台 | [blackmatrix7](https://github.com/blackmatrix7/ios_rule_script) | 568 |
| [流媒体](https://raw.githubusercontent.com/zhihao12/qx-rules/main/streaming.list) | YouTube、Netflix、Disney+、Max、Prime Video 等影音平台 | [ddgksf2013/Filter](https://github.com/ddgksf2013/Filter) + [MagicRule](https://magicrule.pages.dev) | 426 |
| [兜底分流](https://raw.githubusercontent.com/zhihao12/qx-rules/main/fallback.list) | 没被其他表命中的境外域名 | [ConnersHua/RuleGo](https://github.com/ConnersHua/RuleGo) | 398 |
| [Ai](https://raw.githubusercontent.com/zhihao12/qx-rules/main/ai.list) | ChatGPT、Claude、Gemini、Copilot 等 AI 服务 | [VPSDance](https://github.com/VPSDance/ai-proxy-rules) | 308 |
| [交易所](https://raw.githubusercontent.com/zhihao12/qx-rules/main/crypto.list) | Binance、OKX、Bybit、Coinbase 等交易所与钱包 | [MagicRule](https://magicrule.pages.dev) + 本地补遗 | 243 |
| [红果去广告](https://raw.githubusercontent.com/zhihao12/qx-rules/main/hongguo.list) | 红果短剧、番茄小说的广告域名 | [neishe47](https://github.com/neishe47/ios_rule_script) + 本地补遗 | 126 |
| [Telegram](https://raw.githubusercontent.com/zhihao12/qx-rules/main/telegram.list) | Telegram、Swiftgram 等客户端 | [MagicRule](https://magicrule.pages.dev) + 本地补遗 | 65 |
| [直连](https://raw.githubusercontent.com/zhihao12/qx-rules/main/direct.list) | 银行、支付与微信 | [blackmatrix7](https://github.com/blackmatrix7/ios_rule_script) + 本地补遗 | 57 |
| [TikTok](https://raw.githubusercontent.com/zhihao12/qx-rules/main/tiktok.list) | TikTok | [MagicRule](https://magicrule.pages.dev) | 57 |
| [Meta](https://raw.githubusercontent.com/zhihao12/qx-rules/main/meta.list) | Facebook、Instagram、Threads、Messenger、WhatsApp、Meta AI | 本地自维护 + [MagicRule](https://magicrule.pages.dev) | 51 |
| [Spotify](https://raw.githubusercontent.com/zhihao12/qx-rules/main/spotify.list) | Spotify | [MagicRule](https://magicrule.pages.dev) | 37 |
| [社交](https://raw.githubusercontent.com/zhihao12/qx-rules/main/social.list) | Discord、Reddit | [blackmatrix7](https://github.com/blackmatrix7/ios_rule_script) | 35 |
| [规则修正](https://raw.githubusercontent.com/zhihao12/qx-rules/main/unbreak.list) | 被广告表误伤的域名放行 | [ddgksf2013/Filter](https://github.com/ddgksf2013/Filter) | 33 |
| [Github分流](https://raw.githubusercontent.com/zhihao12/qx-rules/main/proxy.list) | GitHub 及相关域名 | [blackmatrix7](https://github.com/blackmatrix7/ios_rule_script) + 本地补遗 | 31 |
| [X](https://raw.githubusercontent.com/zhihao12/qx-rules/main/x.list) | X（原 Twitter） | [blackmatrix7](https://github.com/blackmatrix7/ios_rule_script) + 本地补遗 | 31 |

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

## 4️⃣ 重写（懒人配置已整套带上）

| 重写 | 用途 | 来源 |
| --- | --- | --- |
| 微博去广告 | 微博 App 去广告 | [ddgksf2013/Rewrite](https://github.com/ddgksf2013/Rewrite) |
| 哔哩哔哩三件套 | 去广告、区域解锁、功能增强 | [Biliverse](https://github.com/Biliverse) |
| 双语字幕 | Spotify、YouTube 双语字幕 | [DualSubs](https://github.com/DualSubs) |
| 广告净化（墨鱼系列） | 去开屏、彩云天气、知乎、高德、网易云、闲鱼、喜马拉雅、小宇宙、汽水音乐、微信小程序、小红书 | [ddgksf2013/Rewrite](https://github.com/ddgksf2013/Rewrite) |
| 喜马拉雅补漏、YouTube 增强 | 喜马拉雅与 YouTube 补充净化 | [fmz200/wool_scripts](https://github.com/fmz200/wool_scripts) |
| 网页优化 | Safari 超级搜索、豆瓣观影跳转、Google 重定向与人机增强 | [ddgksf2013](https://github.com/ddgksf2013/Rewrite)、[NobyDa](https://github.com/NobyDa/Script) |
| 百度网盘净化与倍速 | 百度网盘去广告、倍速播放 | [ddgksf2013](https://github.com/ddgksf2013) |
| 微信解锁被屏蔽的 URL | 微信内打开被屏蔽链接 | [zZPiglet](https://github.com/ddgksf2013/Rewrite) |
| BoxJS | 订阅与脚本管理面板 | [chavyleung/scripts](https://github.com/chavyleung/scripts) |
| Spotify 增强 | Spotify 播放与音质增强 | [app2smile/rules](https://github.com/app2smile/rules) |
| 波点音乐增强 | 波点音乐去广告与播放增强 | [WeiGiegie/666](https://github.com/WeiGiegie/666) |
| 红果穿山甲接口 | 红果短剧广告接口空响应 | 本地自维护 |
| 其他增强 | Swiftgram 增强、小红书发帖时间、桌面组件 | [ddgksf2013](https://github.com/ddgksf2013)、[meichiny](https://github.com/meichiny/rednote-feed-time)、[SylvanRoe](https://github.com/SylvanRoe/Scripting) |
