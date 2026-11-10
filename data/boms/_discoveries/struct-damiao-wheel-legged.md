# 达妙开源轮足仓（struct-damiao-wheel-legged）BOM 发现

- 机加版 BOM 一个 Sheet 三张表：电机材料购买表 8 行（有单价）、材料购买表 17 行（有单价）、打印件 16 行（无价）：<https://gitee.com/kit-miao/wheel-legged/blob/master/硬件/机加版/购买清单/机加版bom表.xlsx>
- 表内「总计 2887.3」是公式错误：H60=SUM(G13:G29,G3:G8)，漏掉 USB 转 CAN(93) 与 DMH6215(298) 两行；按行重算应为 3578.3 元（DMH6215 按单价 299×2 计）。
- DMH6215 行自身也矛盾：数量 2、单价 299，总价栏却写 298；本文件按 299×2=598 计并在 unresolved 标注。
- 机加件不在购买清单里，而在同目录 `机加工图纸及模型/轮足加工bom.xls`：13 项（连杆 4、铝方管 3、玻纤板 6），只有材料与数量，单价栏空：<https://gitee.com/kit-miao/wheel-legged/blob/master/硬件/机加版/机加工图纸及模型/轮足加工bom.xls>
- 打印件 16 项 33 件全无价（自打印），只给外形尺寸与部分扫掠/墙数参数，是机加版之外的第二套结构方案。
- 打印件版 BOM 对照：电机/线材/五金同一套，螺丝换成 M3*10/15/25/35、M5*20/30，尼龙柱 3.2*5*25、轮胎 5.5x2，总计 2871.2（同样漏算 391 元）：<https://gitee.com/kit-miao/wheel-legged/blob/master/硬件/打印件版/购买清单/3d打印件版本/双轮腿平衡机器人开源-bom表.xlsx>
- 电池只打印电池盒、两张 BOM 都没列电池型号与价格。
- 精确匹配只有 1 项：DM-H6215 → `damiao-dm-h6215`；开发板（199 元，无型号）、DM-USBCU1、DM-J4310-2EC（未标 V1.1/V1.2）都只能留空。
- 执行器占已标价 84%：4×DM4310 599 元=2396 + 2×DMH6215 299 元=598。
- 大文件 raw 直链返回 403「large file require login」，改用 `git clone --filter=blob:none` + `git cat-file` 取 xlsx（14.8 MB）。
- 仓库 MIT；机械/机加工图纸、安装视频与爆炸图、STM32H7 控制代码（DM-balance）、Simulink 平衡仿真齐全，无自制 PCB。
