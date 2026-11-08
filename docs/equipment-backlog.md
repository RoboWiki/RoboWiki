# 设备库待补清单

> 设备库（equipment）按「热门和常见型号」收录。本文件登记**已确认要补、但规格尚未核齐**的型号，
> 以及**核实后不录**的型号与原因。数据口径与收录标准见 `data/catalog/equipment/` 现有条目
> （A 级 = 官方页面/手册逐项核对，缺的写 null，不编造）。

## 待核规格（下一批补）

### 3D 打印机

| id | 型号 | 已确认的官方口径 | 待核 |
|---|---|---|---|
| bambulab-p1s | 拓竹 P1S | 成型 256×256×256 mm、最高速度 500 mm/s（官网产品页 + Wiki） | 热床温度、重量、尺寸、材料清单 |
| bambulab-p2s | 拓竹 P2S | 成型 256×256×256 mm、喷嘴 300 ℃、净重 14.9 kg、392×406×478 mm（官网 specs 页 + Wiki FAQ） | 最大速度、材料清单 |
| bambulab-a1-mini | 拓竹 A1 mini | 成型 180×180×180 mm（Wiki FAQ） | 速度、温度、重量、尺寸 |
| bambulab-h2d | 拓竹 H2D | 单喷嘴 325×320×325 / 双喷嘴交集 300×320×320 / 并集 350×320×320 mm、喷嘴 350 ℃（官网技术参数页） | 热床温度、重量、尺寸、材料清单；激光模组能力写 notes |
| creality-k1-max | 创想三维 K1 Max | — | 全部（crealitycloud.cn / creality.com 官方页） |
| creality-k2-pro | 创想三维 K2 Pro | — | 全部 |
| creality-ender3-v3-se | 创想三维 Ender-3 V3 SE | — | 全部 |
| snapmaker-artisan | Snapmaker Artisan | — | 全部（三合一，3D 尺寸为主，激光/CNC 幅面写 notes） |
| snapmaker-u1 | Snapmaker U1 | — | 全部；查不到可靠规格则跳过 |

注：拓竹官网（bambulab.com）对抓取返回 403，需用官方检索摘要或 Wiki/手册 PDF 核对。

### 测量仪器

| id | 型号 | 待核 |
|---|---|---|
| uni-t-utg2000x | 优利德 UTG2000X 系列 | 取官方在售具体型号（UTG2122B/UTG2062B 等）后录规格 |
| uni-t-utg962e | 优利德 UTG962E 函数/任意波形发生器 | 全部 |
| uni-t-utl8500x-plus | 优利德 UTL8500X+ 系列电子负载 | 取具体型号后录规格 |
| uni-t-utl8200-plus | 优利德 UTL8200 系列电子负载 | 取具体型号后录规格 |
| uni-t-utr2830e | 优利德 UTR2830E 元件测试仪 | 全部 |
| alientek-dl16 | 正点原子 DL16 逻辑分析仪 | 全部（alientek.com / openedv.com） |
| alientek-dl32-pro | 正点原子 DL32 Pro 逻辑分析仪 | 全部 |
| fnirsi-dla16-plus | FNIRSI DLA-16 PLUS | 全部（fnirsi.com 英文站或官方说明书 PDF） |
| fnirsi-dla32-plus | FNIRSI DLA-32 PLUS | 全部 |

### 等待官方发布

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
