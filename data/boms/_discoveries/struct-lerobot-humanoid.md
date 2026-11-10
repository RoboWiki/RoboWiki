# struct-lerobot-humanoid 拆解发现

12 DOF 双足平台（Apache-2.0）。bom.csv 128 行 / 520 件，**整表无价格**；全表只有 1 行精确匹配（Raspberry Pi 5），成本结构完全依赖外部询价。

- **RobStride O0/O2/O3/O5（共 12 台）**：整机最贵的 12 件；站内 actuator 只有 RS00/RS02/RS03/RS05 等 RS 系列，O 系列无条目与参数 <https://github.com/RobStride/Product_Information>
- **SAVVYCANFD 2CH 双路 CAN FD 适配器**：官方注释称是目前唯一验证支持 RobStride 协议的适配器；站内 module 只有达妙 USB2CANFD 与灵足 USB-CAN HUB（后者明确不支持 CAN FD）<https://github.com/huggingface/lerobot-humanoid-hardware/blob/main/hardware/bom/bom.csv>
- **IMU（BNO055 或 BNO085）**：二选一未定；站内只有 BNO055 裸芯片 `jlc-c93216`，无 BNO085、也无模组形态 <https://github.com/huggingface/lerobot-humanoid-hardware/blob/main/docs>
- **轴承 35x72x17 / 15x21x4 / 5x16x5（26 件）**：站内轴承只有 6203/6802/MR105 等标准型号，这三档尺寸无对应 <https://github.com/huggingface/lerobot-humanoid-hardware/tree/main/hardware/cad/stl>
- **Norelem 27628-01-05 杆端球关节 ×8 + ISO7379 肩螺栓 12 件**：站内 transmission/fastener 都没有"球关节 + 肩螺栓"这一档装配精度件 <https://github.com/huggingface/lerobot-humanoid-hardware/blob/main/hardware/bom/bom.csv>
- **76 件 STL 打印件**：官方另出 bom_buy.csv 把打印件剔除（52 行可买件），说明打印件成本按耗材/代打另算 <https://github.com/huggingface/lerobot-humanoid-hardware/blob/main/hardware/bom/bom_buy.csv>
- **可联动设备**：76 件 STL → `bambulab-p1s` / `bambulab-a1-mini`；CAN 与 48V 母线排故 → `uni-t-ut61e`、`fnirsi-1013d`；大功率调试供电 → `isdt-mp305b`
- **可联动渠道**：树莓派官方 <https://www.raspberrypi.com/products/raspberry-pi-5/>；灵足官网 <https://www.robstride.com/>；装配/打印/接线文档 <https://github.com/huggingface/lerobot-humanoid-hardware/tree/main/docs>
- **价格缺口**：仓库只给"整机 <$5,000"的目标价，属叙述性目标，展示时不得用它倒推分项价 <https://github.com/huggingface/lerobot-humanoid-hardware>
