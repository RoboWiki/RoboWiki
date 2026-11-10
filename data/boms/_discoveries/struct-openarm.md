# struct-openarm 拆解发现

OpenArm 2.0 双臂（Enactic，Apache-2.0 / CERN-OHL-S-2.0）。BOM 是 Google Drive 上的 `OpenArm 2.0 BOM.xlsx`，四段共 79 行，**只有型号 + 供应商，没有价格**，全部靠 MiSUMi（标准件 + meviy 定制）和 DAMIAO 关节电机撑起来。

## ① BOM 用到、站内 taxonomy 没有的行业品类

- **meviy 定制机加件（按型号下单的 CNC 铝件）**：37 行、占总行数 47%，全部是 `MVBLK-ASN-48S-xxxxx-L` 这类 meviy 询价码。站内 `structural` 只有通用结构件、型材、轴承、齿轮，没有"按 3D 模型外协机加"这一档（只对应到 `service`，但 service 目前空着）。
  <https://docs.openarm.dev/hardware/openarm-2.0/general>
- **铝型材支撑柱（MiSUMi HFS 系列）**：General 页写明"support pillars are made of MiSUMi aluminum frames"，但 BOM 表里没有这一行——既是 taxonomy 缺口也是 BOM 缺口。
  <https://docs.openarm.dev/hardware/openarm-2.0/general>
- **关节电机专用配件（圆支柱/台阶螺栓/定位销/超薄树脂垫圈）**：站内 `fastener` 是 RM 语境的内六角/热熔嵌件，缺"精密定位销 + 台阶螺栓"这类装配精度件。
- **USB 延长/中继（KB-USB-RLC305 / RCC305）与 USB Hub**：末端与头部相机走 USB，站内无此类链路件。
- **ZED mini 双目相机**：站内 `camera` 有 ZED 2i，缺 mini 这一档。

## ② 高价值但部件库缺失的件

| 件 | 规格 | 证据 |
| --- | --- | --- |
| DAMIAO DM-J8009P-2EC / J4340P / J4340 / J4310-2EC V1.1 | **站内 4 颗全部已收录**（`达妙-dm-dm-j8009p-2ec` 等），是这批整机里匹配最干净的一组 | <https://docs.openarm.dev/hardware/openarm-2.0/motor> |
| DM-J8009P-2EC 参数 | 24V，额定 20 Nm / 峰值 40 Nm，峰值电流 50 A | 同上（Motor 页规格表） |
| **Arducam B0495** | 腕部相机 ×2 + 顶部相机 ×1，共 3 个 | BOM「End efector #22」「Integration #1」 |
| **StereoLabs ZED mini（ZED-121210）** | 头部双目，站内只有 ZED 2i | BOM「Head Camera #1」<https://www.stereolabs.com/store> |
| SL-GEAHS1.0-36-6-A-17-QFC24-M3 精加工直齿轮 | 夹爪传动，4 件；站内 `misumi-gear-1m-20t` 是 20T，齿数不符 | MiSUMi 标准件目录 |
| FL6700ZZ / FL6803ZZ / B6802ZZ 法兰轴承 | 关节薄型轴承，站内有 6802-2RS 但密封形式不同 | MiSUMi 标准件目录 |
| MiSUMi 铝型材（支撑柱） | 官方文字提到但 BOM 未列，无法取证截面与长度 | <https://docs.openarm.dev/hardware/openarm-2.0/general> |

## ③ 可联动的设备工具

- **24V 大电流电源（最大缺口）**：16 个关节电机，DM8009P 峰值 50 A@24V，整机峰值远超 1 kW；站内 equipment/supply 只有 `fnirsi-dps-150`（150W）、`isdt-mp305a/b`（300W）、`alientek-dp100`，**没有 24V/40A 级工业开关电源**。
  <https://docs.openarm.dev/hardware/openarm-2.0/motor>
- **USB-CAN 调试**：开箱调试必须，站内 `module` 有 `damiao-usb2can`、`damiao-usb2canfd-dual`、`lingzu-robstride-usb-can-hub`——这三条可以直接挂到整机页面。
- **示波器 + 万用表**：CAN 差分波形与 24V 母线排查 → `uni-t-upo2104cs`、`fnirsi-2c53p`、`uni-t-ut61e`。
- **CNC（谨慎联动）**：整机无打印件，全部 CNC/机加；`carvera`（Makera）工作区只够小法兰/相机支架，J1/J2 主体件必须走 meviy 外协，不要在页面上写成"用 Carvera 就能做"。
- **焊接**：电动机关节自带驱动，无需自制板，焊台只在做线束时需要 → `hakko-fx888d`。

## ④ 可联动的采购库渠道

- **WowRobo（深圳）**：官方制造伙伴，整机报价 OpenArm 2 from $6,500 / V1.1 $5,400 / Cell $6,200 / KER $2,599 / KER 编码器单元 $49；站内采购库没有该条。
  <https://docs.openarm.dev/purchase>
- **RT Corporation（东京）**：官方日本渠道，报价制、含日规电源与 1 年保修——采购库里缺"海外官方代理"这一类。
  <https://docs.openarm.dev/purchase>
- **MiSUMi（meviy + 标准件）**：79 行里 65 行来自 MiSUMi，是最大的单点依赖；站内 structural 已收了 6 条 MiSUMi 条目，但没有"meviy 询价"入口。
  <https://meviy.misumi-ec.com>
- **DAMIAO 官方渠道**：站内 actuator 已有 39 条达妙型号，缺的是"整套关节包"报价形式。
- **Arducam / StereoLabs / UGREEN / Sanwa / Belkin**：相机与线缆均来自消费电子品牌，站内采购库无对应。

## ⑤ 适合 RoboWiki 定位的其他发现

- **BOM 真源在 Google Drive 不在 git**：`openarm_hardware` 只放链接，GitHub Releases 的 163 MB tar.gz 只是镜像。复现的人最容易在这里踩空，方案页应直接给 Drive 文件夹与本 xlsx 的入口。
  <https://drive.google.com/drive/folders/14RM-fIPml0HTMnt2zcTXjNxJj9s2R_mG>
- **BOM 无价，但渠道有整机价**：$6,500 是"装好测好"的成品价，与自购件成本是两个口径，页面上必须分开写，否则会误导"自己买件更便宜"。
- **四段结构清晰**（Arm 44 / End effector 23 / Head camera 4 / Integration 8），天然适合做"底座 / 末端 / 头部 / 集成"的分层 BOM 展示。
- **"无 PM 的 BOM"**：全程只有型号与供应商，没有单价、没有交期，正好可以做成"BOM → meviy 一键询价 / 一键配齐"的落地页样例。
- **单臂 7 DOF + 夹爪 = 每臂 8 电机**，双臂 16 台，容量与负载（额定 4.1 kg / 峰值 6.0 kg）可直接与站内 SO-101、XLeRobot 做"舵机级 vs 关节级"分级对照。
