# 全开源整机 BOM 分析

由 `tools/analyze_boms.py` 从 `data/boms/*.json` 生成；价格按各机官方 BOM 原币种统计，不换算、不估补。

- 方案库全开源整机：24 台
- 官方 BOM 已结构化：22 台
- 官方 BOM 未发布、仅有器件骨架：灵足 EL-A3、OpenDoge V1.1（EL05 电机）

## 逐机概览

| 整机 | BOM 行 | 件数 | 已标价合计 | 缺价行 | 站内匹配 |
| --- | ---: | ---: | ---: | ---: | ---: |
| Amazing Hand | 13 | 103 | 153.68 EUR | 0 | 0/13 |
| DOLY DIY / Maker Edition | 43 | 73 | 0.00 USD | 43 | 0/0 |
| G-Exo 下肢外骨骼（V2.2） | 25 | 44 | 4,611.00 CNY | 0 | 2/25 |
| HTDW4438 MiniDog | 29 | 100 | 15,182.45 CNY | 1 | 1/28 |
| LeRobot Humanoid（12 DOF 双足平台） | 128 | 520 | 0.00 USD | 128 | 0/0 |
| Open Duck Mini V2 | 29 | 55 | 432.34 EUR | 0 | 1/29 |
| OpenArm 2.0（双臂） | 79 | 557 | 0.00 USD | 79 | 0/0 |
| PAROL6 | 62 | 375 | 0.00 USD | 62 | 0/0 |
| ROBOTO 01（RP1） | 444 | 1898 | 0.00 CNY | 444 | 0/0 |
| ROBOTO Origin（RPO） | 63 | 832 | 49,672.53 CNY | 23 | 3/40 |
| SO-100 | 6 | 19 | 244.00 USD | 0 | 1/6 |
| SO-101 | 8 | 19 | 229.88 USD | 0 | 1/8 |
| Sesame Robot | 31 | 96 | 0.00 USD | 31 | 0/0 |
| XLeRobot 0.4 | 20 | 49 | 1,055.15 USD | 1 | 1/19 |
| ZEX-W | 75 | 184 | 18,195.96 CNY | 0 | 9/75 |
| reBot Arm B601 (DM) | 83 | 431 | 1,623.35 USD | 56 | 3/27 |
| reBot Arm B601 (RS) | 79 | 368 | 1,466.98 USD | 58 | 2/21 |
| 达妙 AGV 四转四驱 | 27 | 139 | 4,563.54 CNY | 2 | 3/25 |
| 达妙 OpenDoge（OpenDog01） | 85 | 234 | 17,653.11 CNY | 45 | 3/40 |
| 达妙双足人形 | 57 | 123 | 14,779.45 CNY | 47 | 1/10 |
| 达妙开源轮足仓（机加版） | 54 | 102 | 3,578.30 CNY | 29 | 1/25 |
| 高擎 Panthera-HT | 103 | 345 | 0.00 CNY | 103 | 0/0 |

## BOM 品类分布

| BOM 品类 | 行数 | 站内落点 |
| --- | ---: | --- |
| `fastener` | 403 | structural.fastener |
| `structural` | 334 | structural.plate |
| `printed_part` | 222 | structural.printed（新增） |
| `wiring` | 183 | connector.cable / terminal |
| `transmission` | 92 | structural.bearing / belt / gear / shaft |
| `actuator` | 64 | actuator / servo |
| `misc` | 47 | open_hw.accessory |
| `power` | 38 | power / battery / charger |
| `interface` | 28 | remote_controller / power.switch |
| `pcb` | 27 | open_hw.control / module |
| `tooling` | 20 | 设备库（工具 / 仪表） |
| `consumable` | 18 | 材料库 / 设备耗材 |
| `compute` | 14 | controller_high.sbc |
| `sensor` | 12 | imu / sensor |
| `actuator_driver` | 8 | motor_driver |
| `controller` | 8 | controller_low.mcu |
| `thermal` | 8 | open_hw.accessory（暂） |
| `perception` | 8 | camera / lidar |
| `cable_management` | 5 | connector.cable |
| `service` | 4 | 采购库（加工 / 打样） |

## 跨机型共用件

| 件（规范化名称） | 使用机型数 | 机型 |
| --- | ---: | --- |
| powersupply | 5 | struct-parol6, struct-rebot-b601, struct-rebot-b601-rs, struct-so-arm100, struct-so-arm101 |
| screwdriverset | 4 | struct-rebot-b601, struct-rebot-b601-rs, struct-so-arm100, struct-so-arm101 |
| bearing | 3 | struct-lerobot-humanoid, struct-rebot-b601, struct-rebot-b601-rs |
| 轴承 | 3 | struct-open-duck-mini, struct-openarm, struct-panthera-ht |
| 1206贴片电阻120r | 2 | struct-damiao-bipedal, struct-damiao-open-dog |
| 16awg电源线 | 2 | struct-damiao-bipedal, struct-damiao-open-dog |
| 304stainlesssteelphillipscountersunkheadscrew | 2 | struct-rebot-b601, struct-rebot-b601-rs |
| 304stainlesssteelphillipspanheadscrew | 2 | struct-rebot-b601, struct-rebot-b601-rs |
| 3in1iecinletsocket | 2 | struct-rebot-b601, struct-rebot-b601-rs |
| armhandle | 2 | struct-rebot-b601, struct-rebot-b601-rs |
| brushlessmotor | 2 | struct-rebot-b601, struct-rebot-b601-rs |
| canusbdriverboard | 2 | struct-rebot-b601, struct-rebot-b601-rs |
| gear | 2 | struct-rebot-b601, struct-rebot-b601-rs |
| gh1254p胶壳 | 2 | struct-damiao-bipedal, struct-damiao-open-dog |
| gripperconnectora | 2 | struct-rebot-b601, struct-rebot-b601-rs |
| gripperconnectorb | 2 | struct-rebot-b601, struct-rebot-b601-rs |
| gripperfinger | 2 | struct-rebot-b601, struct-rebot-b601-rs |
| gripperhorizontallimit | 2 | struct-rebot-b601, struct-rebot-b601-rs |
| gripperslidermetalbracket | 2 | struct-rebot-b601, struct-rebot-b601-rs |
| gripperslidersupportbracket | 2 | struct-rebot-b601, struct-rebot-b601-rs |
| hexnut | 2 | struct-rebot-b601, struct-rebot-b601-rs |
| linearrail | 2 | struct-rebot-b601, struct-rebot-b601-rs |
| link5 | 2 | struct-rebot-b601, struct-rebot-b601-rs |
| lowerarmleftfiller | 2 | struct-rebot-b601, struct-rebot-b601-rs |
| lowerarmrightfiller | 2 | struct-rebot-b601, struct-rebot-b601-rs |
| microsd卡 | 2 | struct-open-duck-mini, struct-xlerobot |
| motor1bearingmount | 2 | struct-rebot-b601, struct-rebot-b601-rs |
| motorcontrolboard | 2 | struct-so-arm100, struct-so-arm101 |
| outputport | 2 | struct-rebot-b601, struct-rebot-b601-rs |
| poweracwiring | 2 | struct-rebot-b601, struct-rebot-b601-rs |
| powercord | 2 | struct-rebot-b601, struct-rebot-b601-rs |
| rack | 2 | struct-rebot-b601, struct-rebot-b601-rs |
| raspberrypi5 | 2 | struct-lerobot-humanoid, struct-xlerobot |
| roboticarmbaselink | 2 | struct-rebot-b601, struct-rebot-b601-rs |
| roboticarmbaseplatform | 2 | struct-rebot-b601, struct-rebot-b601-rs |
| ros无线手柄 | 2 | struct-damiao-bipedal, struct-damiao-open-dog |
| screw | 2 | struct-rebot-b601, struct-rebot-b601-rs |
| siliconepad | 2 | struct-rebot-b601, struct-rebot-b601-rs |
| sliderblock | 2 | struct-rebot-b601, struct-rebot-b601-rs |
| slidertogripperextension | 2 | struct-rebot-b601, struct-rebot-b601-rs |

## 站内目录覆盖

- 已标价 BOM 行：391；精确匹配到站内部件：32（8.2%）
- 未匹配的条目按 `data/boms/_discoveries/*.md` 的候选清单处理；只有确认厂商型号与参数后才进目录。

## 发现与缺口

详细候选见 `data/boms/_discoveries/`。

---

# BOM 交叉结论（人工整理）

## 1. 成本结构

- 执行器是绝对大头：达妙 OpenDog01 占已标价 **84%**、RPO **63%**、reBot B601 **62%**、Open Duck Mini **47%**、ZEX-W **41%**。先定关节，再谈结构降本。
- 感知可以反超执行器：XLeRobot 的 RealSense D415 一项 $364，占已标价 **34%**，比 12 个 STS3215 还贵。
- 结构件与机加是最大的“价格黑洞”：reBot 21 种 CNC 只给整批 $250、19 种打印件整批 $50；RP1 131 行 CNC + 50 行打印件全部无价；OpenDog 33 项机加/钣金/玻纤/打印全无价。

## 2. 价格可得性

15 台有官方 BOM 的整机里 **5 台完全没有价格列**：RP1、PAROL6、OpenArm 2.0、Doly、Sesame；另 OpenDoge 的 BOM 本身未发布（仅有器件骨架）。其余 10 台有价，但普遍缺结构件、紧固件与外协加工报价。

## 3. BOM 惯例品类 → 站内落点

| BOM 品类 | 站内已有落点 | 判断 |
| --- | --- | --- |
| `actuator` | `actuator` / `servo` | 直接可用 |
| `actuator_driver` | `motor_driver` | 直接可用 |
| `controller` | `controller_low.mcu` | 直接可用 |
| `compute` | `controller_high.sbc` | 直接可用 |
| `sensor` | `imu` / `sensor` | 直接可用 |
| `perception` | `camera` / `lidar` | 直接可用 |
| `power` | `power` / `battery` / `charger` | 直接可用 |
| `wiring` | `connector.cable` / `connector.terminal` | 可用，但缺“整机线束”条目 |
| `pcb` | `open_hw.control` / `module` | 可用，PCBA 打样无独立入口 |
| `structural` | `structural.plate` | 直接可用 |
| `printed_part` | `structural.printed`（本轮新增） | 已补槽位，尚无条目 |
| `fastener` | `structural.fastener` | 直接可用 |
| `transmission` | `structural.bearing/belt/gear` + `structural.shaft`（本轮新增） | 已补光轴/销/衬套槽位 |
| `thermal` | 无 | 暂归 `open_hw.accessory` |
| `interface` | `remote_controller` / `power.switch` | 急停、按键无独立落点 |
| `cable_management` | `connector.cable` | 可用 |
| `consumable` | 材料库 / 设备库耗材 | 不进部件目录 |
| `tooling` | 设备库（工具/仪表） | 不进部件目录 |
| `service` | 采购库（加工/打样） | 不进部件目录 |

## 4. 最值得补的目录缺口

按跨机型复现频率排序：

1. **12V 总线舵机链**：Feetech STS3215 12V（XLeRobot 17 台）+ Waveshare Bus Servo Adapter (A)（SO-100/101、Open Duck、Amazing Hand 共 4 台）。
2. **Feetech SCS0009**：Amazing Hand 8 颗，占单手物料 49%，站内 servo 只有 STS/ST/HD 系列。
3. **步进 + 驱动 + 减速箱**：PAROL6 的 NEMA17（16/45/65 Ncm）、TMC5160、EG 20:1/10:1 行星减速箱；站内一条都没有。
4. **直线导轨与轴承**：reBot/PAROL6 的 MGN9-170 + 滑块、6707ZZ/6803ZZ/AXK5578、HR32906J/HR32907J，站内只有通用轴承槽位。
5. **通讯模块**：ZEX-W / OpenDoge / reBot 的 DM-USB2CANFD Dual 已有条目但无价，BOM 给出 ¥109 的直接证据。
6. **RS02 价格证据**：ZEX-W 16 台官方店 ¥629、二手 ¥380，站内参考价 ¥699，可补一条“官方店/二手”价格来源。
7. **Jetson Orin Nano 套件**：ZEX-W 用 Seeed “8G + 256G” 套件 ¥2300，站内只有裸模组。
8. **Raspberry Pi Zero 2W**：Open Duck 主控，`controller_high` 只有 Pi 4/5。
9. **达妙 DM4310/DM4340P V4 版次**：reBot 使用 V4，站内是早期版次，采购时容易买错。

## 5. 可联动的设备与采购库

- **设备库**：3D 打印 → 拓竹 A1 mini / P1S；压线与焊端子 → FNIRSI HS-02；上电排故 → UNI-T UT61E、ALIENTEK DP100/DP200；小件 CNC 不在设备库，走采购库加工服务。
- **采购库缺口**：StepperOnline、Waveshare、Seeed Studio、Source Robotics 官方店，以及 Amazon FR / AliExpress / nknet 等海外零售。现有 234 家以华强北/淘宝渠道为主，海外 BOM 几乎零命中。
- **站内已有可回填价**：`灵足-robstride-rs02`、`damiao-usb2canfd-dual`、`sens-manifold-odin1`、`feiqilai-jumbo-power-6s-21700`。

## 6. 需要修正的数据口径

- **两个 OpenDoge 不是同一台**：达妙科技 `OpenDog01`（DM6248P 电机，Gitee）与 OpenDogeRobotics `OpenDoge V1.1`（EL05 电机，GitHub）是同名不同厂项目，BOM、生态与部署链互不通用。本清单分别记 `struct-damiao-open-dog` 和 `struct-opendoge-v1`。
- **OpenDoge V1.1**：官方 BOM 仍标 “In progress”，`OpenDoge_hardware` 只有 mechanical 与 datasheets；按“全开源 = BOM + 机械 + 硬件”的定义，它目前不满足全开源，应在方案卡上明确或降为半开源。
- **SO-100**：`artifacts.bom` 当前指向 SO-101 的表，应改到 `SO100.md` 的 parts 锚点。
- **RP1**：BOM 主控是 RBE-MAIN-RK3588S + Orange Pi CM5，没有 Jetson Orin；整机参数页写 Orin NX 16GB，需注明是商用配置还是开源 BOM 配置。
- **ZEX-W**：官方 xlsx 里还有 8DOF 旧版 58 行，不能与 16DOF 主线混算；本清单只取 16DOF。
- **Doly**：官方只发 6 块板卡的元件级 TSV（125 个元件），不是整机采购 BOM；整机行按 maker guide 反推。
- **OpenArm**：79 行中 65 行来自 MiSUMi 定制件，官方 BOM 无价；$6500 是成品报价，不是物料合计。
- **reBot B601**：本次只拆 DM 版；RS 版在兄弟目录，不能混为同一份 BOM。
