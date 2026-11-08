# 设备库待补清单

> 设备库（equipment）按「热门和常见型号」收录。本文件登记**已确认要补、但规格尚未核齐**的型号，
> 以及**核实后不录**的型号与原因。数据口径与收录标准见 `data/catalog/equipment/` 现有条目
> （A 级 = 官方页面/手册逐项核对，缺的写 null，不编造）。

## 当前收录（45 件，data-v2026.11.20）

| 子类 | 数量 | 型号 |
|---|---|---|
| 3D 打印机 | 11 | 拓竹 A1 / P1S / P2S / A1 mini / H2D，创想三维 K1 / K1 Max / K2 Pro / Ender-3 V3 SE，Snapmaker Artisan / U1 |
| 激光切割与雕刻 | 3 | xTool P2 / F1 / M1 |
| 焊接与返修 | 6 | 正点原子 T100 / T300 / T80P / H550，快克 861DW，HAKKO FX-888D |
| 可调电源 | 3 | 正点原子 DP100，ISDT MP305A / MP305B |
| 测量仪器 | 22 | 优利德 UT89X / UT39E+ / UT33D+ / UT136B+ / UPO2104CS / UPO2074HD / UTG2000X（UTG2122X）/ UTG962E / UTL8500X+（UTL8512A+）/ UTL8200+（UTL8211+）/ UTR2830E，FNIRSI DMT-99 / DMT-A100 / TDM120P / 1013D / 1014D / DLA-16 PLUS / DLA-32 PLUS，正点原子 CM1 / DS100 / DL16 / DL32 Pro |

## 待核规格（下一批补）

暂无。热门与常见型号已基本覆盖；后续按用户指定型号或新榜单热度增量补充。

## 等待官方发布

| id | 型号 | 状态 |
|---|---|---|
| alientek-dp200 | 正点原子 DP200 | 官网标注「新品即将上市」，规格未公布；已确认为 DP100 升级款、属可调电源，待手册发布后补录 |

## 核实后不录

| 型号 | 原因 |
|---|---|
| QUICK 快克 858D | 快克官网热风拆焊台分类无此型号；858D 为市面白牌通用型号，非快克官方产品 |
| BAKON BK936A | BAKON 官网焊台分类无此型号（仅有 BK936 / SBK936B / SBK936D+ 等）；第三方目录的 bk936A+ 参数非授权来源，不采信 |
| 正点原子 DS213 | 官网产品分类与下载中心均无此型号（仅有 DS100，已录入） |
| 正点原子 T300 Pro | 官网仅 T300（已按 alientek-t300 录入），T300 Pro 官网未列 |

## 手工与电动工具（tool 子类）

榜单证据最弱，暂不收录；设备库保持「仪器级」含金量。后续若收，需先定子类口径
（电磨 / 台钻 / 螺丝刀套装是否同层）。

## 核参通路备注

- 拓竹官网（bambulab.com）对直接抓取返回 403，但 **store.bblcdn.com 官方 CDN 的规格单 PDF 可直下载**
  （P1S / P2S / A1 mini / H2D 均有 Spec Sheet），是最稳的官方口径来源。
- 创想三维走 crealitycloud.cn 产品页；优利德走 instruments.uni-trend.com.cn / meters.uni-trend.com.cn；
  正点原子走 alientek.com；FNIRSI 走 fnirsi.com/products/<型号>。
