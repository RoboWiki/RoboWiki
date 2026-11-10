# SO-101（struct-so-arm101）BOM 发现

- 数据文件：`data/boms/struct-so-arm101.json`
- 官方来源：SO-ARM100 仓库当前 README 的 “Parts For Two Arms (Follower and Leader Setup)”
  https://github.com/TheRobotStudio/SO-ARM100#parts-for-two-arms-follower-and-leader-setup
- 口径：Leader + Follower 双臂 12 个舵机，按减速比拆 C001(7)/C044(2)/C046(3)；本文件只录 US 列，官方 Total `$229.88` 与逐行相加一致。

## ① BOM 用到、站内 taxonomy 没有的行业品类

| 品类 | BOM 里的样子 | 站内现状 | 证据 |
| --- | --- | --- | --- |
| AC-DC 电源适配器 | 5 V 适配器（DC 5.5×2.1），每臂 1 个 | `power` 无适配器子类；`charger` 是电池平衡充 | README row 6 |
| 3D 打印耗材与服务 | PLA+，0.4/0.6 喷嘴，15% 填充；另有 `3DPRINT.md` 打印服务 | 无耗材、无外协打印服务品类 | https://github.com/TheRobotStudio/SO-ARM100/blob/main/3DPRINT.md |
| 工装夹具 | Table Clamp 4 个装 | `equipment` 只有“电动与手工工具”；`structural/机构件` 是本体件 | README row 7 |
| 整机/分套件商品 | Seeed、WowRobo、RobotEd、ForgeMotion 卖“打印件套件/电子件套件/整机”三档 | 站内缺“套件”商品形态，只有整机与单品 | https://github.com/TheRobotStudio/SO-ARM100#kits |
| 触觉传感器（可选） | AnySkin 触觉皮肤加装在夹爪 | `sensor` 子类里没有触觉/电子皮肤（只有触摸传感器芯片级） | https://shop.wowrobo.com/products/enhanced-anyskin-premium-crafted-editionwowskin |

## ② 高价值、但部件库缺失的件

1. **Feetech STS3215 C044（7.4 V，1:191）** —— Leader 臂 2 个，$13.89/个。站内只有通用 `feetech-sts3215-7v4`（规格书即 C001）与 `feetech-st-3215-c018`，没有 C044 条目；站内条目自己也写了“C044/C046/C047 参数不同，不混为一行”。
   - 证据：README row 2 https://www.alibaba.com/product-detail/Feetech-STS3215-SO-ARM101-Servo-7_1601430747897.html
2. **Feetech STS3215 C046（7.4 V，1:147）** —— Leader 臂 3 个，$13.89/个，同属高价值缺口。
   - 证据：README row 3 https://www.alibaba.com/product-detail/Feetech-STS3215-SO-ARM101-Servo-7_1601430760797.html
3. **Leader 臂 6 个装 bundle** —— 官方专门给了一条“一次买齐 3×C046 + 2×C044 + 1×C001”的链接，属于可入库的“套装 SKU”，站内没有套装形态。
   - 证据：README 脚注 2 https://www.alibaba.com/product-detail/6PCS-7-4V-STS3215-Servos-for_1601428584027.html
4. **Waveshare 总线舵机控制板（Bus Servo Adapter A）** —— 双臂 2 块，$10.6/块，整机唯一下位机，站内无 Waveshare 品牌、无该板。
   - 证据：README row 4 https://www.amazon.com/Waveshare-Integrates-Control-Circuit-Supports/dp/B0CTMM4LWK/ ；官方 wiki https://www.waveshare.com/wiki/Bus_Servo_Adapter_(A)
5. **32×32 UVC 相机模组 / 腕部相机支架配套件** —— README 第 5 节给了 6 种腕部相机支架（含 D405/D435），但站内 `camera` 只有 RealSense D405/D435i/D455/D457 等成品，缺最常用的 32×32 UVC 模组。
   - 证据：https://github.com/TheRobotStudio/SO-ARM100#optional-hardware
6. **TPU 95A 打印耗材（柔性夹爪）** —— 官方 Compliant Gripper 需 TPU 95A + PLA 底座，站内无耗材品类。
   - 证据：https://github.com/TheRobotStudio/SO-ARM100/tree/main/Optional/Compliant_Gripper

## ③ 可联动的设备工具（站内已有 equipment 条目）

| 设备 | 站内 id | 联动理由与证据 |
| --- | --- | --- |
| 拓竹 A1 mini | `bambulab-a1-mini` | README 给 Prusa/UP（205×250）与 Ender（220×220）整套 STL；小床机型需按 A1 mini 分件方案打印 |
| 拓竹 P1S | `bambulab-p1s` | README 打印建议列 Bambu A/P/X 系列（0.4 喷嘴/0.2 层高/15% 填充） |
| 创想 Ender-3 V3 | `creality-ender-3-v3` | README 以 Ender 系（220×220）作为整套 STL 的目标床尺寸 |
| 优利德 UT210E 钳形表 | `uni-t-ut210e` | 12 个 STS3215 同时上电的电流分配与堵转排查 |
| 正点原子 DL16 逻辑分析仪 | `alientek-dl16` | TTL 串行总线包/波特率与舵机 ID 排查（README Debugging Motors 节给了 Feetech 上位机与 FT_SCServo_Debug_Qt） |
| ISDT MP305A 可调电源 | `isdt-mp305a` | 换 12 V 舵机需 12 V 5A+，可调限流电源比固定适配器更适合首上电 |
| 正点原子 S40 电动螺丝刀 | `alientek-s40` | SO-101 主打“装配更简单、无需拆齿轮”，电动螺丝刀可作升级工具位 |

证据：https://github.com/TheRobotStudio/SO-ARM100#step-1-choose-a-printer 、https://github.com/TheRobotStudio/SO-ARM100#debugging-motors

## ④ 可联动的采购库渠道

与 SO-100 同一批套件商（站内供应商库无一家），差别是 SO-101 套件更全，且部分家只做 SO-101：

| 渠道 | 卖什么 | 证据 |
| --- | --- | --- |
| Seeed Studio（国际 / 中国淘宝 / 日本 Akizuki / AliExpress） | 含 3D 打印件的套件 | https://www.seeedstudio.com/SO-ARM100-Low-Cost-AI-Arm-Kit.html |
| WowRobo（国际 / 中国淘宝） | SO-ARM101 装配版 | https://shop.wowrobo.com/products/so-arm101-diy-kit-assembled-version-1 |
| RobotEd（瑞士） | 打印框架 / 电子件 / 整机三档 | https://roboted.ch/en/shop/so-101-robot-arm-kit |
| Robonine（国际） | 零件套件 + 腕部相机 + ArUco 方块 | https://robonine.com/shop/so-arm101-black-white-robotic-arm-kit/ |
| PartaBot（美国） | 装配版整机 | https://partabot.com |
| ForgeMotion Labs（美国 / Amazon US） | 打印框架、电子件、整机 | https://forgemotionlabs.com/products |
| RoboSEasy（韩国） | 韩国本地 | https://smartstore.naver.com/roboseasy |
| NeoBot（中国淘宝） | 淘宝套件 | https://item.taobao.com/item.htm?ft=t&id=957685951340 |
| Autodiscovery（EU） | 欧盟套件 | https://autodiscovery.eu/en/products/so-101-kit |
| Phospho | 仅 Follower 臂（VR 遥操作用） | https://robots.phospho.ai |

一级件渠道：飞特 Alibaba 官方店（C001/C044/C046 与 6 个装 bundle）、微雪 Waveshare（控制板）。日本 Akizuki Denshi 单舵机 `¥2,980 JPY` 对 `¥97.72 RMB`，是“同一颗舵机跨区价差”的典型样本，适合作采购对比条目。
证据：https://github.com/TheRobotStudio/SO-ARM100#kits

## ⑤ 适合 RoboWiki 定位的其他发现

1. **README 就是 SO-101 文档**：仓库标题已改成 “Standard Open SO-100 & SO-101 Arms”，parts 表只服务 SO-101，SO-100 被标 deprecated（`SO100.md`）。站内两台整机共用同一个 `artifacts.bom` URL，实际只有 SO-101 对得上——SO-100 应改指 `SO100.md` 的 anchor。
2. **减速比拆行是本机最有价值的信息**：Leader 臂不是“6 个同款舵机”，而是 3×C046 + 2×C044 + 1×C001（Follower 全 C001）。买错齿轮比装不上，属于典型“看似同型号、实则不同料”的坑，值得在方案页显式提示。
3. **`price_cny: 682` 是单臂价**：官方单臂 `$121.94 / ¥682.23`、双臂 `$229.88 / ¥1,343.16`；站内整机价取的是单臂口径，与 BOM 的双臂口径不一致，需要在页面标注。
4. **RMB 合计也是旧值**：CN 列逐行相加 `¥1,354.76`，官方 Total 写 `¥1,343.16`（与 SO-100 表同一个数字），说明这张表的 RMB 合计跨版本没跟着改。USD 列加法是对的（`$229.88` 精确对账）。
5. **官方 12 V 升级提示只在 DO 段**：12 V 30 kg·cm 只对 Follower 可选，Leader 永远 7.4 V；且必须同时换 12 V 5A+ 电源。这是“升级一半就烧/带不动”的典型组合坑。
6. **可选硬件已成生态**：举升底座、4040 型材底座、AnySkin 触觉、TPU 柔性夹爪、6 种腕部相机支架，还有 XLeRobot（双 SO101 + LeKiwi + 300 Wh 电池，总价 $660）——可作为“SO-101 衍生方案”与站内 `xlerobot` 条目的交叉链接。
   证据：https://github.com/TheRobotStudio/SO-ARM100#optional-hardware
