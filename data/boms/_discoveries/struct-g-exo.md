# struct-g-exo 拆解发现

G-Exo V2.2（MIT）。BOM 25 行 / ¥4,611，执行器占 55%；RS02×4 是唯一精确匹配件，其余多是淘宝散件与碳纤维外协，价格全为作者询价的约值。

- **6S 3000mAh 小动力电池 ×2**：站内 6S 只有 ACE 5300mAh（`ace-gtech-6s-5300-30c`），缺 66.6Wh 这一档 <https://github.com/Lain-Ego0/G-Exo/blob/main/1.hardware/BOM.md>
- **6S LiPo 平衡充**：站内 `isdt-mp305a/b` 是直流电源，`power` 没有任何 LiPo 平衡充电器条目 <https://www.isdt.co/>
- **SpacemiT K3 COM260 核心板**：站内 compute 只有 Jetson / 树莓派 / 瑞芯微，缺 RISC-V + NPU 这一支 <https://www.spacemit.com/>
- **G354 车规 6 轴 IMU ×4**：站内 imu 全是裸芯片（BNO055 等），无车规模块形态，原表按 ¥0 记 "已有" <https://github.com/Lain-Ego0/G-Exo/blob/main/1.hardware/BOM.md>
- **碳纤维管/板外协加工 ¥580**：非电机项最大一笔，站内 `service` 品类为空、`structural` 只有 3mm 碳板现货 <https://github.com/Lain-Ego0/G-Exo/tree/main/1.hardware>
- **3D 打印耗材（按 kg 计价）**：站内 `consumable` 无 PETG/PLA 打印耗材条目，只有胶水焊料类 <https://github.com/Lain-Ego0/G-Exo/blob/main/1.hardware/BOM.md>
- **可联动设备**：打印结构件 → `bambulab-a1-mini` / `bambulab-p1s`；母线压降排查 → `uni-t-ut61e`；RS02 调试 → `lingzu-robstride-usb-can-hub` <https://github.com/Lain-Ego0/G-Exo>
- **可联动渠道**：灵足官网 RS02 ¥699（学生 9 折 ~¥629，BOM 即此价）<https://www.robstride.com/>；RS02 手册/固件与 CAN 协议 <https://github.com/RobStride/Product_Information>
- **价格口径**：原表自述为"大致估计"，主控/IMU/USB-CAN 记 ¥0（借到或已有），站点展示须标 "已有件，非采购价" <https://github.com/Lain-Ego0/G-Exo/blob/main/1.hardware/BOM.md>
