# struct-rebot-b601-rs 拆解发现

Seeed reBot B601 RS（灵足 RobStride 关节）。官方 BOM 是 README 里 7 张 Markdown 表，本次拆出 79 行 / 368 件，21 行有价（合计 1466.98 USD），58 行缺价。
<https://github.com/Seeed-Projects/reBot-DevArm/blob/main/hardware/reBot_B601_RS/README.md>

- 电机占成本 77%：RS00×4（125 USD/台）+ RS06×3（210 USD/台）= 1130 USD；其余外购件合计不到 340 USD。
- 结构件全部外协：27 种 CNC 铝件（5052）表里只有加工工艺与公差，没有价格列，也没有 DM 版那种"整批均价"行，逐件全缺。
- 打印件 16 种（含线束夹与电源盒 3 件外壳）同样无价；DM 版的 50 USD 整批均价在 RS 版没有，两版价格不可直接类比。
- 10 行螺丝 Reference Price 空白、数量为 80+/60+/48+ 下限（按整数录入并注明）；4 行 XT30 2+2 成品线的价格列放的是示意图。
- 唯一 CNY 行是 M3x2.5 六角螺母（2 个，2.10 CNY），按不换算纪律置 null 未计入合计。
- 站内精确对上 2 行：RobStride RS00→`灵足-robstride-rs00`、RS06→`灵足-robstride-rs06`。
- 目录缺口：6803ZZ / AXK5578 轴承、MGN9-170 导轨与 MGN9 滑块、模数 1 16T 齿轮、LRS-600-48 电源、RobStride 版 CAN-USB 板（站内只有 USB-CAN HUB）、XT30 2+2 成品线。
- 页面只给 5 档 Seeed kit 链接、无整机价，例如 <https://www.seeedstudio.com/reBot-Arm-B601-RS-Disassembly-Kit-Version-with-Power-Supply-Bundle.html>
