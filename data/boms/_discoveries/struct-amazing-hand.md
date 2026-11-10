# struct-amazing-hand 拆解发现

- 主 BOM 是 Google Sheet（gid=1269903342），单手物料 €116,89；控制分两段 OR 路线，TOTAL 分别为 €128,28 与 €142,29，美元列按 1,16 换算。 <https://docs.google.com/spreadsheets/d/1QH2ePseqXjAhkWdS9oBYAcHPrxaxkSRCgM_kOK0m52E/edit?gid=1269903342>
- 8× Feetech SCS0009 @€7,15 = €57,20，占单手物料 49%，是唯一执行器；站内 servo 目录只有 STS3215 与 ST/HD 系列，缺 SCS 系列。 <https://www.alibaba.com/product-detail/Feetech-SCS009-Micro-Mini-Size-SCS_62058112947.html>
- 第二贵是 M2 球头拉杆 L19：16 套 €17,60；官方给了同规格第二卖家链接，说明球头是易缺货件。 <https://www.amazon.fr/dp/B0CWRZFK42>
- 指关节用 D2×10 / D2×16 空心轴 + GFM 0608-04 铜衬套，站内 transmission 仅覆盖轴承/齿轮/同步带/联轴器/丝杆，无光轴销与自润滑衬套。 <https://fr.aliexpress.com/item/1005008281348810.html>
- 热塑自攻螺丝单价 €0,01（2.5×6 16 颗、2.5×8 30 颗），原表两行链接标注的规格互相写反，采购时易买错。 <https://fr.aliexpress.com/item/1005006883251273.html>
- M2.5 大外径垫圈 €0,43/件共 4 件，属于"大垫圈 serie"非标规格，站内 fastener 无此口径。 <https://www.amazon.fr/dp/B09BLJBRDF>
- 3D 打印件只给打包价 €15（1 件计入），官方未给件数、克重与工时，成本口径不可复用。 <https://github.com/pollen-robotics/AmazingHand/tree/main/cad>
- 控制路线 A：WaveShare 总线舵机驱动板 €11,39（USB→半双工 TTL），站内无同功能条目。 <https://www.amazon.fr/dp/B0CJ6TP3TP>
- 控制路线 B：Arduino Mega €24 + TTLinker Mini €1,40，比路线 A 贵 €14；站内 controller_low 无 Arduino，module 只有 CAN 转换。 <https://www.alibaba.com/product-detail/TTLinker-Mini-UART-Signal-Conversion-Board_1601526016354.html>
- 补充 BOM 只列链接不列价：M2 丝锥、5V 外接电源、球头/衬套/丝杆替代件，需外接 5V/2A 才能驱动 8 个舵机。 <https://www.amazon.fr/Carbosing-10W-Adaptateur-Alimentation-Intelligente/dp/B0DZHZXDJ4>
- 原件链接全部指向 Amazon FR / AliExpress / Alibaba；站内 234 家采购库无这些海外零售/批发渠道条目。 <https://docs.google.com/spreadsheets/d/1QH2ePseqXjAhkWdS9oBYAcHPrxaxkSRCgM_kOK0m52E/edit?gid=1269903342>
- 固件与仿真齐全：Python pypot/rustypot + ArduinoExample + MuJoCo/mink，另有摄像头手势跟踪示例，可直接做二次开发入口。 <https://github.com/pollen-robotics/AmazingHand>
