# SO-100（struct-so-arm100）BOM 发现

- 数据文件：`data/boms/struct-so-arm100.json`
- 官方来源：`SO100.md`（当前 SO-ARM100 README 已把 SO-100 标为 deprecated，parts 表仍在这里）
  https://github.com/TheRobotStudio/SO-ARM100/blob/main/SO100.md#parts-for-two-arms-standard-teleoperation-setup
- 口径：Leader + Follower 双臂，12 个 STS3215；本文件只录 US 列，官方 Total `$232` 与逐行相加 `$244` 不符（见 ⑤）。

## ① BOM 用到、站内 taxonomy 没有的行业品类

| 品类 | BOM 里的样子 | 站内现状 | 证据 |
| --- | --- | --- | --- |
| AC-DC 电源适配器 | 5 V 开关电源，DC 5.5×2.1 mm，每臂 1 个；换 12 V 舵机要 12 V 5A+ | `power` 只有 DC-DC / BMS / 分电 / 开关，`charger` 是电池平衡充，没有“桌面适配器”这一类 | SO100.md row 4 https://github.com/TheRobotStudio/SO-ARM100/blob/main/SO100.md |
| 3D 打印耗材与打印服务 | PLA，0.4 mm 喷嘴 / 0.2 mm 层高 / 13% 填充；官方另有 `3DPRINT.md` 打印服务页 | 站内 22 品类里没有耗材、也没有外协加工/打印服务（BOM schema 的 `consumable` / `service` 无对应品类） | https://github.com/TheRobotStudio/SO-ARM100/blob/main/3DPRINT.md |
| 工装夹具（桌夹） | Table Clamp，双臂 4 个装 $9 | `equipment` 有“电动与手工工具”子类但没有夹具；`structural` 的“机构件（夹爪/吸盘/拨盘）”是机器人本体件，不是装夹工装 | SO100.md row 5 |
| 整机套件（kit）作为商品 | Seeed / WowRobo 等卖的“3D 打印件套件 / 电子件套件 / 装配整机” | 站内只有整机方案页与单品部件页，没有“套件（含打印件+电子件）”这一层商品形态 | https://www.seeedstudio.com/SO-ARM100-Low-Cost-AI-Arm-Kit.html |

建议：`power` 增子类“AC-DC 适配器”，新增或复用 `consumable`（打印耗材）与 `service`（打印/加工），`structural` 增子类“夹具与工装”。

## ② 高价值、但部件库缺失的件

1. **Waveshare 总线舵机控制板（Bus Servo Adapter A）** —— 双臂 2 块，$11/块，是整机唯一“下位机”，站内连 Waveshare 品牌都没有。
   - 证据：SO100.md row 2 Amazon 链接 https://www.amazon.com/Waveshare-Integrates-Control-Circuit-Supports/dp/B0CTMM4LWK/
   - 官方 wiki（UART/USB 两种接法、STS 系列总线）：https://www.waveshare.com/wiki/Bus_Servo_Adapter_(A)
2. **STS3215 12 V 30 kg·cm 版本** —— README 明确的可选升级，站内只有 `feetech-sts3215-7v4`（7.4 V 19 kg·cm）与 ST-3215-C018，12 V/30 kg 档缺失。
   - 证据：SO-ARM100 README 顶部 IMPORTANT 段落 + 12 V 购买链接
     https://github.com/TheRobotStudio/SO-ARM100#sourcing-parts
     https://www.alibaba.com/product-detail/6PCS-12V-30KG-STS3215-High-Torque_1601216757543.html
3. **5 V 5A+ / 12 V 5A+ 桌面电源适配器（DC 5.5×2.1）** —— 每臂一个，缺件直接影响上电，站内无条目。
   - 证据：SO100.md row 4 https://www.amazon.com/Facmogu-Switching-Transformer-Compatible-5-5x2-1mm/dp/B087LY41PV/
4. **32×32 UVC 相机模组 / 腕部相机支架配套件** —— 可选的腕部与顶置相机，README 给了多种支架但没有相机条目；站内 `intel-realsense.json` 有 D405/D435i，缺 32×32 UVC 模组这一常用低成本件。
   - 证据：README Optional Hardware 第 2、5 节 https://github.com/TheRobotStudio/SO-ARM100#optional-hardware
5. **桌面快速夹（TAODAN 4pcs）** —— 装调必需，站内既无夹具也无此类五金。
   - 证据：SO100.md row 5 https://www.amazon.com/TAODAN-Trigger-Ratchet-Woodworking-Processes/dp/B0DJNXF8WH

## ③ 可联动的设备工具（站内已有 equipment 条目）

| 设备 | 站内 id | 联动理由与证据 |
| --- | --- | --- |
| 拓竹 A1 mini | `bambulab-a1-mini` | SO100.md 给了 A1 mini 专用的分件打印 STL（床小需分 2 件），README 也把 Bambu A/P/X 列为实测机型 |
| 拓竹 P1S | `bambulab-p1s` | README 打印建议列 Bambu A/P/X 系列；SO100.md 有 Bambu P1P 的 3mf |
| 创想 Ender-3 V3 | `creality-ender-3-v3` | README 以 Ender 3（220×220）为代表性打印床尺寸给出整套 STL |
| 优利德 UT210E 钳形表 | `uni-t-ut210e` | STS3215 7.4 V 堵转电流 2.5 A、额定 650 mA，总线舵机供电排查常用钳形表 |
| 正点原子 DL16 逻辑分析仪 | `alientek-dl16` | 调试 TTL 半双工串行总线包（README 的 Debugging Motors 节给了 Feetech 上位机与 FT_SCServo_Debug_Qt） |
| ISDT MP305A 可调电源 | `isdt-mp305a` | 官方只配固定 5 V 适配器；调试堵转/温升需要可调限流电源 |
| 正点原子 S40 电动螺丝刀 | `alientek-s40` | 官方 BOM 只有手动精密螺丝刀（#0/#1），电动款可作为“升级工具”推荐位 |

证据：https://github.com/TheRobotStudio/SO-ARM100#printing-the-parts 、https://github.com/TheRobotStudio/SO-ARM100/blob/main/SO100.md

## ④ 可联动的采购库渠道

官方 README 的 Kits 一节列了 10 家套件商，站内 `data/suppliers.json`（RM 红黑榜口径）一家都没有，建议新增“开源硬件套件商”这类渠道，并区分“含打印件 / 含电子件 / 整机装配”：

| 渠道 | 卖什么 | 证据 |
| --- | --- | --- |
| Seeed Studio（国际站 / 中国淘宝店） | 含 3D 打印件的 SO-ARM100 套件 | https://www.seeedstudio.com/SO-ARM100-Low-Cost-AI-Arm-Kit.html |
| WowRobo（国际站 / 中国淘宝店） | SO-ARM101 装配版 DIY 套件 | https://shop.wowrobo.com/products/so-arm101-diy-kit-assembled-version-1 |
| RobotEd（瑞士） | 打印框架套件 / 电子件套件 / 整机套件三档 | https://roboted.ch/en/shop/so-101-robot-arm-kit |
| Robonine（国际） | 零件套件，含腕部相机与 ArUco 方块 | https://robonine.com/shop/so-arm101-black-white-robotic-arm-kit/ |
| PartaBot（美国） | 装配版，兼售 LeKiwi / Koch | https://partabot.com |
| ForgeMotion Labs（美国 / Amazon US） | 打印框架、电子件、整机 | https://forgemotionlabs.com/products |
| RoboSEasy（韩国） | 韩国本地渠道 | https://smartstore.naver.com/roboseasy |
| NeoBot（中国淘宝） | 淘宝套件 | https://item.taobao.com/item.htm?ft=t&id=957685951340 |
| Autodiscovery（EU） | 欧盟套件 | https://autodiscovery.eu/en/products/so-101-kit |
| Phospho | 仅 Follower 臂（配 VR 头显用） | https://robots.phospho.ai |

另有两类“原厂/一级”渠道值得入库：飞特 Alibaba 官方店（舵机，SO100.md row 1 链接）、微雪 Waveshare 官方 wiki/店铺（控制板）。
证据汇总：https://github.com/TheRobotStudio/SO-ARM100#kits

## ⑤ 适合 RoboWiki 定位的其他发现

1. **`data/robots/so-arm100.json` 的 `artifacts.bom` 指向错了表**：现在指向 README 的 `#parts-for-two-arms-follower-and-leader-setup`，那是 **SO-101** 的表；SO-100 的表在 `SO100.md`。建议改指 `https://github.com/TheRobotStudio/SO-ARM100/blob/main/SO100.md#parts-for-two-arms-standard-teleoperation-setup`，或补 `bom_note` 说明“README 主表已切 SO-101”。（本次任务不改 robots 数据）
2. **官方合计与逐行不符**：双臂表舵机标 `$15×12=$180`，其余行 64，合计应为 `$244`，但官方 Total 写 `$232`——`$232` 等价于 `12×$14`（单臂表单价）。RMB 列同理：逐行相加 `¥1,354.76`，官方写 `¥1,343.16`（与 SO-101 表同一数字，疑为旧值）。这是很好的“BOM 对账”教学案例：Σ行 ≠ Total 时以行单价为准。
3. **单臂 / 双臂口径混乱**：`price_cny: 682` 等于单臂 `¥682.23`，但 BOM 与 README 主推的是双臂套装 `¥1,343.16`。方案页应显式标注“价格口径=单臂”，否则用户按 ¥682 预算会少一半。
4. **`SO100.md` 脚注失效**：正文引用 `#myfootnote1/2/3`，但文件内没有任何 `<a name="myfootnoteN">` 定义，舵机版本、电源规格、螺丝刀建议三条脚注读不到。可记为“官方文档瑕疵”。
5. **12 V 升级是连带升级**：换 12 V 舵机必须同时换 12 V 5A+ 电源（README IMPORTANT 段明说），属于典型选型陷阱，适合做“避坑”条目。
6. **USD 列并非最低价**：同一舵机 CN `¥97.72`、EU `€12.2`、US `$13.89`，而 EU 电源 `€15.7` 明显高于 US `$10`；地区价差是 RoboWiki 采购对比的天然素材（不换算，按原币并列）。
