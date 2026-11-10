# struct-doly-diy 拆解发现

DOLY-DIY（Limitbit，Maker Edition，CC BY-NC-SA 4.0）。官方 BOM 只到**板级元件清单**，站点现在的品类体系基本对不上；下面是值得补的口子，全部带证据。

## ① BOM 用到、站内 taxonomy 没有的行业品类

- **元件级板卡 BOM（Designator / Footprint / Manufacturer Part）**：6 个 CSV 共 125 行，全是 0603 阻容、SOT-23、FPC 座这类 SMT 件，站内 23 个品类（舵机/电机/相机/雷达…）没有任何一格能放。
  <https://github.com/robotdoly/DOLY-DIY/tree/main/Electronics/BOM>
- **FPC/FFC 柔性排线 + 0.5 mm 间距 FPC 座**：THD0515-08/12/24/45CL-SN 四种，站内 connector 只有 JST/GH/XH/PH、USB-C、DC 座，缺 FPC 连接器这一整类。
  <https://github.com/robotdoly/DOLY-DIY/blob/main/Electronics/BOM/BOM_Head.csv>
- **圆形 LCD 模组（1.28" IPS 12PIN round）**：头部双眼屏，站内无显示屏/显示模组品类（`interface` 只覆盖遥控器/急停/按键）。
  <https://github.com/robotdoly/DOLY-DIY/blob/main/Electronics/BOM/BOM_Head.csv>
- **Dock 触点充电（DockChargeContact / PAD 触点）**：MagSafe 式触点回充，站内 charger 品类只有航模平衡充。
  <https://github.com/robotdoly/DOLY-DIY/blob/main/Electronics/BOM/BOM_Charger.csv>
- **触摸电容检测 IC（MTCH101T）／音频 Codec（TLV320AIC3110）**：站内 chip 品类偏 RM 电源类，没有人机交互类 IC。
  <https://github.com/robotdoly/DOLY-DIY/blob/main/Electronics/BOM/BOM_Head.csv>

## ② 高价值但部件库缺失的件

| 件 | 规格 / 证据 | 为什么值得补 |
| --- | --- | --- |
| Raspberry Pi CM4 | 主板用 2× `DF40C-100DS-0.4V(51)`（Hirose 100P 板对板）承载 CM4，BOM_MainBoard 第 39/40 行 <https://github.com/robotdoly/DOLY-DIY/blob/main/Electronics/BOM/BOM_MainBoard.csv> | 站内只有整板 RPi 4/5，没有 CM4 模组与配套连接器 |
| INA219AIDR 电流监测 | 主控板 U4，#61 <https://github.com/robotdoly/DOLY-DIY/blob/main/Electronics/BOM/BOM_MainBoard.csv> | 站内 `ti-ina226` 有 INA226，缺同系列 INA219（12V 总线最常用） |
| LSM6DSRTR IMU | 主控板 U15，#27（同文件） | 站内有三颗 ST IMU（LSM6DS3TR-C/DSLTR/DSOXTR），独缺 DSR |
| ADS1015IDGSR 12-bit ADC | 主控板 U18，#28（同文件） | 站内 sensor 只有编码器与限位开关，无通用 ADC |
| TP5000-QFN16 锂电充电 | 主控板 U13，#53（同文件） | 单节锂电 2A 充电，站内 power 只有 BMS 保护板，无充电 IC |
| VL6180X ToF ×2 | 防撞板 TOF_L/TOF_R <https://github.com/robotdoly/DOLY-DIY/blob/main/Electronics/BOM/BOM_Bumper.csv> | 站内 sensor 无 ToF/接近传感器 |
| ME6211C28M5G（2.8V 版） | 头部板 U16，#16 <https://github.com/robotdoly/DOLY-DIY/blob/main/Electronics/BOM/BOM_Head.csv> | 站内只收 `ME6211C33M5G-N`（3.3V），同系列不同电压容易下错单 |

> 板级元件里目前唯一能精确对上站内条目的是 `MT3608`（Doly 主控板 U16/U17 → `jlc-c84817`）。

## ③ 可联动的设备工具

- **3D 打印**：14 个 STEP/STL、18 件，官方指定 PLA/PETG → 可挂 `bambulab-a1-mini`、`bambulab-p1s`、`creality-k1c`。
  <https://github.com/robotdoly/DOLY-DIY/tree/main/Printables/PLA-PETG>
- **回流焊/热风**：6 块板共 125 个 SMT 件，手贴需热风台 → `quick-861dw`、`hakko-fx888d`、`fnirsi-hs-02`。
- **直流电源 + 万用表**：板卡上电调试（TP5000/MT3608/DRV8837）→ `alientek-dp100`、`uni-t-ut61e`。
- **示波器 + LCR**：0603 被动件与 I2C/SPI 时序排故 → `fnirsi-1013d`、`fnirsi-lcr-st1`。
- **不需要 CNC**：全机无金属结构件，机械件全部打印，CNC 类设备无可挂点。

## ④ 可联动的采购库渠道

- **PCB 打样**：6 块板只有 Gerber（`Gerber_MainBoard_1.2mm.zip` 等），必须外发打样 → 嘉立创/JLCPCB 一类渠道，站内采购库 234 家里没有对应条目。
  <https://github.com/robotdoly/DOLY-DIY/tree/main/Electronics/Gerber>
- **被动件与连接器**：0603 阻容（SAMSUNG/YAGEO/UniOhm）、Molex `1050570001`、Hirose `DF40C-100DS`、THD FPC 座，属于立创商城/华秋一类目录分销的典型货。
- **Doly 官方商店只卖整机**，不卖散件，这也是官方 BOM 没有单价的原因。
  <https://shop.doly.ai>

## ⑤ 适合 RoboWiki 定位的其他发现

- **交互式 iBOM 现成可嵌**：`Electronics/InteractiveView/*.html` 是每块板的 iBOM，能直接在整机详情页做"点板看件"的联动，不用自研。
  <https://github.com/robotdoly/DOLY-DIY/tree/main/Electronics/InteractiveView>
- **许可证是最硬的边界**：CC BY-NC-SA 4.0 明确禁止商用，方案页需要把"仅教学/自用"讲清楚，否则会误导打包售卖的人。
  <https://github.com/robotdoly/DOLY-DIY/blob/main/LICENSE>
- **只给 Gerber 不给 KiCad 源**：可以改板但不能改设计，属于"可制造但不可再设计"，和站内其他全开源整机的口径要区分。
- **装配手册把零件编成 E/C/S/H 码**：`[E01]`…`[R04]` 与步骤一一对应，天然适合做成"零件 → 步骤"双向索引。
  <https://robotdoly.github.io/DOLY-DIY/maker/>
- **BOM 粒度错位**：官方把 BOM 拆在板卡层（125 个元件），整机层只有 guide 的零件码清单且无价。整机 BOM 写成 43 行是"板卡 + 机构件"折中，板内元件数写进了 spec，后续若要做元件级采购必须再补一层。
