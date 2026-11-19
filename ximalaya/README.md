# 喜马拉雅去广告（自有合并版）

喜马拉雅在 QX 圈的去广告规则主要就两家：墨鱼（ddgksf2013）和奶思（fmz200），本目录把两家 2026-11-19 的现行版本全量合并成自有订阅，规则一条未删（奶思版默认关闭的 4 条以注释保留）。响应处理脚本 `ximalaya_json.js` 仍由原作者 ddgksf2013 的仓库托管，本仓只合并规则本体。

## 文件

- [qx/ximalaya-filter.conf](qx/ximalaya-filter.conf)：分流规则 9 条（广告域名 reject，来自奶思版的域名段）
- [qx/ximalaya-rewrite.conf](qx/ximalaya-rewrite.conf)：重写规则，墨鱼版 24 条加奶思版 18 条，QX 片段格式（无段头，hostname 裸行）

## QX 订阅行

```
https://raw.githubusercontent.com/zhihao12/qx-rules/main/ximalaya/qx/ximalaya-filter.conf, tag=喜马拉雅去广告, update-interval=86400, opt-parser=false, enabled=true
https://raw.githubusercontent.com/zhihao12/qx-rules/main/ximalaya/qx/ximalaya-rewrite.conf, tag=喜马拉雅去广告, update-interval=86400, opt-parser=false, enabled=true
```

分流行加进 `[filter_remote]`，重写行加进 `[rewrite_remote]`，需开启 MITM 并信任证书。广告仍在时先清缓存或重装应用（原作者说明）。

## 来源

- [ddgksf2013/Rewrite](https://github.com/ddgksf2013/Rewrite) 的 AdBlock/Ximalaya.conf（墨鱼版 V1.0.27）
- [fmz200/wool_scripts](https://github.com/fmz200/wool_scripts) 的 QuantumultX Ximalaya.snippet（奶思版，2026-11-11）
