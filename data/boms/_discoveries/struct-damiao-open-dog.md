# 达妙 OpenDog01（struct-damiao-open-dog）BOM 发现

- 官方 BOM 目录 3 份工作簿（机械+电控采购+机加/打印件、线材、早期电控表）：https://gitee.com/kit-miao/open-dog/tree/master/%E7%A1%AC%E4%BB%B6/BOM%E8%A1%A8
- 机械表 16.9 MB：contents API 只回前 10 MB（base64 截断）、raw 直链 403，最终用 `git clone --filter=blob:none` + `git cat-file` 取全量：https://gitee.com/kit-miao/open-dog/blob/master/硬件/BOM表/四足机械bom表.xlsx
- 一个 Sheet 混装“电控采购/机械采购/铝件/钣金/铝管/玻纤/打印件”，图片列为 `#VALUE!` 占位需按行号定位；机械采购小计 620.11 元与表内总计一致：同上
- 机械采购里六面螺母（铝管骨架）166.8 元占 27%，M4 螺母 6 包 21 元；螺丝按“包”买、装配清单按“颗”用，两套口径需分开看：同上
- 装配螺丝清单（第 88–129 行）出现 M3*8 / M3*20 / M4*14 三种采购表未列的规格：同上
- 线材表分“下肢/上肢”两列，说明还有装在上肢的机械臂扩展（XT30 2+2 双端线上肢 2 根、SH1.0 8P 卧贴 4 个）：https://gitee.com/kit-miao/open-dog/blob/master/硬件/BOM表/四足线材.xlsx
- 线材表 KCD1 船型开关、GH1.25 2P 胶壳只写“电源开关”“备用”，无数量，两行未计入 BOM：同上
- 硬件产品.xlsx 与机械表电控部分重复且冲突：电池 1×537.82 元 vs 机械表 2×608 元；该表另有 ROS 手柄 78 元、NUC 无价：https://gitee.com/kit-miao/open-dog/blob/master/硬件/BOM表/硬件产品.xlsx
- 成本主体是 12 个 DM-J6248P-2EC ×1241 元 = 14892 元，占已标价部分 84%：https://gitee.com/kit-miao/open-dog/blob/master/硬件/BOM表/四足机械bom表.xlsx
- 精确匹配仅 2 项：DM-J6248P-2EC（`达妙-dm-dm-j6248p-2ec`）、USB 转双路 CANFD（`damiao-usb2canfd-dual`）
- 达妙 IMU 只写“IMU模块”无型号（站内只有 DM-IMU-L1）；ORIN NX 载板 BOM 为 V1.1、站内是 V2.X，均不匹配：https://gitee.com/kit-miao/open-dog
- 电源板/四足分电板/24V→19.5V 电源板有工程与打板文件，可自制，但 BOM 未列其元件：https://gitee.com/kit-miao/open-dog/tree/master/硬件/硬件电路板开源资料
- 机加件+钣金+铝管+玻纤+打印件共 33 项 72 件全部无价，是最大报价缺口；仓库无 LICENSE，复用前需联系作者：https://gitee.com/kit-miao/open-dog
