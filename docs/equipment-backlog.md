# 设备库待补清单

> 设备库（equipment）按「热门和常见型号」收录。本文件登记**已确认要补、但规格尚未核齐**的型号，
> 以及**核实后不录**的型号与原因。数据口径与收录标准见 `data/catalog/equipment/` 现有条目
> （A 级 = 官方页面/手册逐项核对，缺的写 null，不编造）。

## 当前收录（69 件，data-v2026.11.23，16 子类五族）

| 族 | 子类 | 数量 | 型号 |
|---|---|---|---|
| 加工设备 | FDM 3D 打印机 | 13 | 拓竹 A1/P1S/P2S/A1 mini/H2D、创想 K1/K1 Max/K1C/K2 Pro/Ender-3 V3 SE/Ender-3 V3、Snapmaker Artisan/U1 |
| 加工设备 | 光固化 3D 打印机 | 1 | ELEGOO Saturn 4 Ultra 12K |
| 加工设备 | CNC 雕刻机 | 1 | 造物时代 Carvera |
| 加工设备 | 激光切割与雕刻 | 5 | xTool P2/F1/M1/D1 Pro、创想 Falcon2 22W |
| 焊接与返修 | 焊台与铁锅 | 5 | 正点原子 T100/T300/T80P、HAKKO FX-888D、FNIRSI HS-02 |
| 焊接与返修 | 热风枪与返修 | 2 | 正点原子 H550、快克 861DW |
| 电源 | 可调电源 | 4 | 正点原子 DP100、ISDT MP305A/B、FNIRSI DPS-150 |
| 测量仪器 | 万用表 | 7 | 优利德 UT89X/UT39E+/UT33D+/UT136B+/UT61E、FNIRSI DMT-99/DMT-A100 |
| 测量仪器 | 钳形表 | 3 | 正点原子 CM1、FNIRSI TDM120P、优利德 UT210E |
| 测量仪器 | 示波器 | 7 | FNIRSI 1013D/1014D/2C53P/DST-210、正点原子 DS100、优利德 UPO2104CS/UPO2074HD |
| 测量仪器 | 信号发生器 | 4 | 优利德 UTG2122X/UTG962E、FNIRSI SG-004A/TSG3020 |
| 测量仪器 | 电子负载 | 3 | 优利德 UTL8512A+/UTL8211+、正点原子 EL15 |
| 测量仪器 | 逻辑分析仪 | 5 | 正点原子 DL16/DL16 Plus/DL32 Pro、FNIRSI DLA-16/32 PLUS |
| 测量仪器 | 元件测试仪 | 5 | 优利德 UTR2830E、正点原子 LT1/LT2、FNIRSI LCR-ST1/ST2 |
| 调试与工具 | 下载与调试 | 2 | 正点原子 ATK-HSDAP/Mini-Pro |
| 调试与工具 | 电动与手工工具 | 2 | 正点原子 S40、FNIRSI SWM-10 |

68/69 有产品图；**仅 xtool-d1-pro 缺图**（官网 429 限流无法取图）。

## 待核规格（下一批补）

暂无。热门与常见型号已基本覆盖；后续按用户指定型号或新榜单热度增量补充。

## 等待官方发布

| id | 型号 | 状态 |
|---|---|---|
| alientek-dp200 | 正点原子 DP200 | 官网仍标注「新品即将上市」，规格未公布（用户反馈 200W/30V/6.8A）；已确认为 DP100 升级款、属可调电源，待手册发布后补录 |

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
