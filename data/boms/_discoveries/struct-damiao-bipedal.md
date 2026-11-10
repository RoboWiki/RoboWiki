# 达妙双足人形（struct-damiao-bipedal）BOM 发现

- 官方 BOM 目录三份工作簿，按整机一套合并：https://gitee.com/kit-miao/bipedal-robot/tree/master/%E7%A1%AC%E4%BB%B6/BOM%E8%A1%A8
- 机械bom表.xlsx 只有 32 项：27 项螺丝/螺母/垫片/尼龙柱数量均写“1 件”（按包购买，不是装配颗数），5 项轴承给 6/10/6/4/2 个；整表无单价：https://gitee.com/kit-miao/bipedal-robot/blob/master/%E7%A1%AC%E4%BB%B6/BOM%E8%A1%A8/%E6%9C%BA%E6%A2%B0bom%E8%A1%A8.xlsx
- 三份表都没有机身/四肢加工件（CNC、钣金、3D 打印）清单，结构件只能按仓库三维模型自行加工：https://gitee.com/kit-miao/bipedal-robot/tree/master/%E7%A1%AC%E4%BB%B6
- 硬件产品.xlsx 覆盖 19 个关节：10×DM-4340@799 + 1×DM-6006@799 + 4×DM-4310@599 + 4×DM-3507@499 = 13181 元，占已标价小计 89%：https://gitee.com/kit-miao/bipedal-robot/blob/master/%E7%A1%AC%E4%BB%B6/BOM%E8%A1%A8/%E7%A1%AC%E4%BB%B6%E4%BA%A7%E5%93%81.xlsx
- DM-MC02 开发板 199 元；站内目录已注明 DM-MC-Board02 与商城简写 DM-MC02 是同一款板，故精确匹配 `damiao-dm-mc-board02`
- 主控“达妙 ORIN 载板+核心板”与“NUC”二选一：载板 800 元有价，ORIN Nano 核心板与 i9 NUC 都无价，小计不能当整机主控成本
- 人形线材.xlsx 分下肢/上肢两列，合并后 XT30 2+2 双端 12 根、GH1.25 2P 5 根、16AWG 红黑各 3 米等，整表无单价：https://gitee.com/kit-miao/bipedal-robot/blob/master/%E7%A1%AC%E4%BB%B6/BOM%E8%A1%A8/%E4%BA%BA%E5%BD%A2%E7%BA%BF%E6%9D%90.xlsx
- KCD1 带灯船型开关只写“电源开关”、GH1.25 2P 胶壳只写“备用(1份10个)”，均无数量，未计入行
- 电池为格氏 ACE 4000mAh 6S 30C XT60，468 元；站内只有 5300mAh 版本，容量不同不匹配
- IMU 只写“达妙IMU”，未给型号；DM-4340/6006/4310/3507、ORIN 载板也都未写到站内目录的具体型号/版本，全部留 null
- 防滑垫标“重要”但无价；小风扇 4.45 元；ROS 手柄 78 元
- 精确匹配仅 1 项：DM-MC02 开发板（`damiao-dm-mc-board02`）
- 价格口径为淘宝/天猫小批量价，未含运费与税；仓库未声明 LICENSE
