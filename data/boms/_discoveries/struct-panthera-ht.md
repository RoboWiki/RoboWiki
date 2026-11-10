# 高擎 Panthera-HT（struct-panthera-ht）BOM 发现

- BOM 在 Model 仓 3_BOM/：当前版 BOM.xlsx 与旧版 BOM_v1.xlsx：https://github.com/HighTorque-Robotics/Panthera-HT_Model/tree/main/3_BOM
- BOM.xlsx 是 Panthera-HT V3.1（2026-09-04 输出），第一张表 Panthera-HT3.1装配BOM清单即整机；同工作簿另有 xlerobot-HT、PI+ 清单与打印/复模/钣金/电机型号说明页，未混入本机：https://github.com/HighTorque-Robotics/Panthera-HT_Model/blob/main/3_BOM/BOM.xlsx
- 整机 103 行 / 345 件：CNC 18 项 20 件、钣金 11 项 12 件、电机 5 项 7 台、打印件 13 项 18 件、复模件 8 项 8 件、标准件 42 项 274 件、线材 6 根
- 全表没有价格列，只有料号、数量与淘宝链接，103 行全部 unit_price=null
- 电机：joint1 HTDW-5036-02-CNE、joint2/3 HT-6056-36、joint4 HT-5036-02、joint5/6 HTDW-4438-CNE-30、夹爪 HT-3536，见《电机型号数量整理文档》页
- 精确匹配仅 1 项：HTDW-5036-02-CNE（`hightorque-htdw-5036-02-cne`）；HTDW-4438-CNE-30 与站内 HTDW-4438-30-NE-JC 命名不同，HT-3536 与站内 HTDW-3532-02-DNE 型号不同，均留 null
- 控制/功率板本体缺失：BOM 只在“通用盒子功率底板”位置列了安装螺丝，没有 7CAN 功率板；旧版 BOM_v1 有“通信板”1 件：https://github.com/HighTorque-Robotics/Panthera-HT_Model/blob/main/3_BOM/BOM_v1.xlsx
- 电源与上位机未列：Panthera 表没有 24V 电源适配器、CAN 转接和上位机（同工作簿 xlerobot-HT 表有 220V→24V 适配器）
- BOM_v1 与 V3.1 电机型号不一致：6036-02-DNE/5036-02-DNE/4438-30-NE → HT-6056-36/HT-5036-02/HTDW-4438-CNE，跨版本不能混用
- 复模件 8 个外观盖按硅胶复模、类 ABS；打印件主体 PETG-CF 45%，L5_C 与夹爪软指为 TPU
- 标准件含 3 种轴承、小法兰轴承、MGN9 导轨 + 2 滑块、304 螺丝 M1.6–M6、铜螺柱与圆柱销，均为淘宝零售件
- 机械文件同仓：SolidWorks 2024 v3.1/v1、STEP 整机与加工/打印/钣金分类，MIT 许可：https://github.com/HighTorque-Robotics/Panthera-HT_Model
