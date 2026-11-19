# 红果去广告 · HongGuo AdBlock

红果短剧（`com.phoenix.video`）去广告规则汇总。红果是字节的产品，本身没几个专属域名，广告全走字节共用体系：穿山甲 SDK 下发、zijieapi 广告 API、snssdk 路径广告、fqnovel 埋点。所以只盯「红果」字样是拦不干净的，本仓把红果与番茄系（同源体系）社区规则做了交叉验证后合并，并附一份真机验证过的「绝不拦截」放行清单。

## 文件

| 文件 | 用途 |
| --- | --- |
| [qx/hongguo-filter.conf](qx/hongguo-filter.conf) | Quantumult X 分流规则（filter_remote 订阅） |
| [qx/hongguo-rewrite.conf](qx/hongguo-rewrite.conf) | Quantumult X 重写（rewrite_remote 订阅，需 MITM） |
| [shadowrocket/hongguo.module](shadowrocket/hongguo.module) | Shadowrocket 模块 |
| [domains.txt](domains.txt) | 纯域名清单（AdGuard Home / Pi-hole / hosts） |

## Quantumult X 用法

分流（必选，免证书）：

```
https://raw.githubusercontent.com/zhihao12/qx-rules/main/hongguo/qx/hongguo-filter.conf, tag=红果去广告, update-interval=172800, opt-parser=false, enabled=true
```

放进 `[filter_remote]`。本表自带 reject 策略。注意 QX 里 filter_local 优先于 filter_remote，基础服务放行写在 filter_local（见下方清单），不要写进本表。

重写（可选，需开 MITM 并信任证书）：

```
https://raw.githubusercontent.com/zhihao12/qx-rules/main/hongguo/qx/hongguo-rewrite.conf, tag=红果去广告重写, update-interval=172800, opt-parser=false, enabled=true
```

放进 `[rewrite_remote]`。作用是把穿山甲接口和红果广告域名返回空 JSON（reject-dict），比直接断连更干净，SDK 不会当成网络错误重试。

## 拦截分层

1. **穿山甲 / Pangle SDK**：`pangolin` 关键词 + `pglstatp-toutiao.com`、`pglstatp-toutiao-b.com` 后缀。开屏与插播广告的主要来源。
2. **字节广告 API**：`ads3/ads5-normal.zijieapi.com` 与 `-lf` 变体，含通配。
3. **广告素材签名域**：`p3/p6/p9-ad-sign.byteimg.com`。其中 p3 与抖音商城图片共用，抖音图片异常就删 p3 那行（社区模块对此有分歧，本仓默认保留并标注）。
4. **广告跳转与追踪**：`zlink.ugsdk.cn`、`zlink.toutiao.com`、`effect.snssdk.com`、`ichannel.snssdk.com`。
5. **视频广告 CDN**：`*-reading-ad.qznovelvod.com`、`*-iosreadingvideo.qznovelvod.com`，只拦广告子域，不碰正片 CDN。
6. **埋点 / 上报**：`mon.toutiaocloud.*`、`i/is(-lq).snssdk.com`、`applog.fqnovel.com`、`*-misc.fqnovel.com` 等。不影响看剧，介意可整段删。
7. **进阶路径拦截**（重写文件里默认关闭）：红果自家 API 的 `*.snssdk.com/api/ad/` 路径广告，域名层看不出来，只能 MITM 后按路径拦。代价是解密字节主 API 域，没把握别开。

## 绝不拦截（重点）

下面这些是字节基础服务，拦了红果会转圈、卡顿、加载失败。本仓维护者在真机上验证过：2026-11-04 拦截后卡顿，11-12 一度撤销放行又因卡顿恢复。请把它们写进本地直连放行，不要被任何「全家桶」规则带偏：

- `tnc*.snssdk.com`、`tnc*.zijieapi.com`（配置下发）
- `security.snssdk.com`、`security-lq.snssdk.com`（安全校验）
- `mssdk.zijieapi.com`（风控基础服务）
- `gecko3.zijieapi.com`、`gecko5.zijieapi.com`（资源下发）
- `lf-normal-gr-sourcecdn.bytegecko.com`、`lf-webcast-gr-sourcecdn.bytegecko.com`（正片资源）

同理，**切勿整域拦截** `zijieapi.com`、`snssdk.com`、`pstatp.com`、`bytedance.com`。社区个别模块这么写（含 `DOMAIN-KEYWORD, zijieapi` 全家桶、番茄模块把 security/gecko/mssdk 一并 reject 的做法），番茄是阅读应用或许能忍，红果是视频应用，搬过来必卡。

## 已知边界

- 「看广告领金币 / 解锁剧集」与普通广告共用 SDK，拦截后这类入口会一并失效，这是模式决定的，无解。
- 首页推荐卡片、金币任务、VIP 推广是红果第一方业务，不走广告域名，拦不掉。
- 出现持续转圈或黑屏：先停用重写只留分流；还不行就逐段注释分流里的埋点段与素材段定位。

## 来源与致谢

域名逐条对照以下公开来源交叉验证（2026-11-19 汇总），并叠加维护者本人的真机误杀记录：

- [akiralereal/shadowrocket-toolkit](https://github.com/akiralereal/shadowrocket-toolkit) 红果模块（GPL-3.0）
- [k6nfmm7dbr-commits/hongguo-lite](https://github.com/k6nfmm7dbr-commits/hongguo-lite) 红果短剧瘦身
- [LOWERTOP/Shadowrocket-First](https://github.com/LOWERTOP/Shadowrocket-First) 红果果皮箱
- [bluee1111/egern-hongguo-adblock](https://github.com/bluee1111/egern-hongguo-adblock)
- [lzwsoldier/stash-hongguo-adblock](https://github.com/lzwsoldier/stash-hongguo-adblock) 与其上游 [azel-ko/stash-adblock-rules](https://github.com/azel-ko/stash-adblock-rules)
- [spaoye/hongguo-adblock](https://github.com/spaoye/hongguo-adblock)（番茄 + 红果 Loon 插件，部分激进条目未采纳，见「绝不拦截」）
- [QingRex/LoonKissSurge](https://github.com/QingRex/LoonKissSurge) 番茄小说去广告（可莉，部分条目与红果放行清单冲突，未采纳并已注明）
- doovvip/sublink-worker2 · HongGuo-Surge-Native（经 hongguo-lite 转引交叉验证）

本仓只做汇总、筛选与格式适配，规则本身来自社区公开成果。仅供个人学习与自用。
