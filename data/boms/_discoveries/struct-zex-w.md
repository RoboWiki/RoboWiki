# struct-zex-w 拆解发现

ZEX-W（MIT，16DOF 串联轮足，18.04 kg）。官方 BOM 是一张淘宝采购流水：16DOF 主线 75 行 + 8DOF 旧版 58 行，本清单合计 **18,195.96 元**，作者自述"纯16dof 大致成本 1.8w 左右"。<https://github.com/zeitvex/RC_WheelLeg/tree/main/03_hardware>
## ① 缺的行业品类
- **通讯模块（USB-CAN / FDCAN）**：品类表没有 module 一类，整机把两块达妙 USB-CAN（各 109 元）记在"驱动"里，本站只能落 `misc`。<https://gitee.com/kit-miao/usb2canfd-dual>
- **关节电机成品线束**：CyberGear 双直母头 18AWG 硅胶线、XT30(2+2) 转 GH1.25 共 9 行 516 元；站内只有 JST GH1.25 本体与 5264 端子线，无 RS02 成品线束。
- **轮足轮系**：8 寸 200x45 轮胎 ×4 + 5M/AT5 非标同步轮 22 个 + HTD5M 带；站内 `transmission` 只有 GT2/2GT，`wheel` 只有麦轮与全向轮，两处都接不上。
- **金属增材与整包机加**：316L SLM 1261 元、6061 CNC 694 元按整包报，`service` 品类没有任何点价/外协条目可挂。
## ② 可补部件（BOM 有价、目录缺价或无条目）
- **RS02**：`灵足-robstride-rs02` 参考价 699，BOM 记官方店 629、闲鱼二手 380；16 台电机占整机 41%，是站内 RS02 最完整的价格证据。<https://www.robstride.com/>
- **达妙 DM-USB2CANFD Dual / DM-USB2CAN**：目录两条均无价，BOM 都是 109 元，可直接补价。<https://gitee.com/kit-miao/damiao>
- **Jetson Orin Nano 8G**：目录只有 8G 计算模组，BOM 是 seeed 的"8G + 256G 硬盘"套件 2300 元，缺一个套件 SKU。<https://www.seeedstudio.com/>
- **Odin1（3000 元）与飞起来 6S 21700（197 元）**精确命中 `sens-manifold-odin1`、`feiqilai-jumbo-power-6s-21700`，两条都能回填价格。<https://manifoldtechltd.github.io/wiki/odin_series/odin1/14.%20Technical%20Specifications_.html>
## ③ 可联动设备 / 采购渠道
- 3D 打印：4 卷 PETG（21.8–49 元）+ 全部机身打印件 → 拓竹 A1 mini / P1S；压线与烧录（8DOF 段有 DAPLink 46 元）→ FNIRSI HS-02、正点原子 S40。
- 渠道：75 行全是淘宝店铺，站内 234 家采购库只命中**固万基旗舰店**（`sup-3a5c9aa9`）；嘉立创、铨洲、正泰、达妙、灵足、seeed、留形均缺。
## ④ 适合站点的发现
- **"1.8 万造一台 16DOF 轮足"** 是本站最便宜的足式移动整机锚点（比 OpenArm 低一个量级），16×RS02 + Orin + Odin1 可直接与商用四足做参数对照。
- 这是**真实采购流水**：合并单元格分组合计、实付款含运费、8 台二手电机、同规格两次采购不同价（M5 锁紧螺母 5.25 / 5.00），最适合做"BOM ≠ 报价单"的教案。
- 作者公开三条降本路径：RK3588 替 Orin、二手工业 IMU + 拆机雷达替 Odin1、拆分结构件降本，可直接做成"降本选项"字段。
