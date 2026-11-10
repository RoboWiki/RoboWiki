# PAROL6（struct-parol6）BOM 发现

- 真表在 `BOM/README.md`，`BOM/BOM.md` 只是 207 字节的转链说明；仓库根无 PCB 目录，控制板走官方成品：https://github.com/Source-Robotics/PAROL6-Desktop-robot-arm/tree/main/BOM
- 全表 10 节 62 行、375 件，**没有任何价格列**（无单价/合计/整机报价），故 priced_subtotal=0，价格缺口靠第三方询价补：https://github.com/Source-Robotics/PAROL6-Desktop-robot-arm/blob/main/BOM/README.md
- 缺价外的口径坑：软管写 “5 meters”（qty=5/m），真空吸盘夹爪 3 行与小打印床改造 3 行未标明是否标配：https://github.com/Source-Robotics/PAROL6-Desktop-robot-arm/blob/main/BOM/README.md
- 缺口①：站内无 TMC5160、NEMA17 步进（16/45/65 Ncm）、EG 20:1/10:1 行星减速箱、HTD3M 带轮、AXK3552 与 NSK HR32906J/HR32907J 轴承：https://www.omc-stepperonline.com/eg-series-planetary-gearbox
- 缺口②：采购库 234 家里没有 StepperOnline、AliExpress  affiliate 与 Source Robotics 官方店，而本 BOM 的购买链接几乎全是这三家：https://source-robotics.com/
- 缺口③：`amass-xt30` 是公母对，BOM 只要 “xt30 connector female” 单头，口径不同不能算精确匹配：https://github.com/Source-Robotics/PAROL6-Desktop-robot-arm/blob/main/BOM/README.md
- 74 张 BOM reference images 可作缺图件与替代料比对素材：https://github.com/Source-Robotics/PAROL6-Desktop-robot-arm/tree/main/BOM/BOM%20reference%20images
- 官方提示螺丝/同步带/轴承本地买、MG 系列减速箱是更便宜但背隙更大的替代：https://www.omc-stepperonline.com/mg-series-planetary-gearbox
- 电子件里有 6 片 TMC5160 + 成品控制板（STM32F446RE），即“官方板 + 自行插驱动”的两段式，适合与站内 `motor_driver` 品类联动：https://github.com/Source-Robotics/PAROL6-Desktop-robot-arm/tree/main/PAROL6%20control%20board%20main%20software
- 打印件与装配资料齐全（STL/STEP、Building instructions、URDF/MuJoCo），只缺 PCB 源文件：https://github.com/Source-Robotics/PAROL6-Desktop-robot-arm/tree/main/STL
