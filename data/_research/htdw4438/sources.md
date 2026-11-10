# HTDW4438 MiniDog 资料核对（2026-11-10）

## 关键事实
- 主仓：https://github.com/Lain-Ego0/HighTorque-MiniDog （默认 main，13 star）。`HTDW4438-OpenDog` 已重命名为该仓，旧 URL 301 到主仓，README 仍写旧名与「主仓库（当前）」。主仓无 LICENSE。
- 结构/URDF：`1.Hardware/htdw_4438_urdf/urdf/htdw_4438.urdf` 有 12 个 revolute + 4 个 fixed 关节（每条腿 髋/大腿/小腿，足端固定），即 12 DOF；17 个 link 惯性质量合计 4.356 kg。
- 尺寸：`base_link.STL` 包围盒 204×140×141 mm；训练站高目标 `base_height_target = 0.185 m`（HTDW4438_Isaacgym/legged_gym/envs/htdw_4438/htdw_4438_config.py）。
- 执行器：官方 BOM 12 × HTDW-4438（¥899/个）；项目文档含 HTDW-4438-30-NE 模型与 -32-NE 安装图，仓内未写机器人用哪一版。
- 主控：RoBoBox-7C 开发套件（RK3588 核心板 + 功率板 + 7 路 CAN，¥2999）；IMU 为 YESENSE（SDK 有 yesense_ros 与 yesense 脚本）。
- 电池：HTB24（BOM 记 24V）；`3.Document/高擎动力电池资料/电池参数.png` 对应 HTB24-02：22.2V 5000mAh 111Wh Li-ion，0.5 kg。
- 训练：Isaacgym（BSD-3 系）、HIMloco（MIT）、AMP（CC BY-NC-SA 4.0）；sim2real 仓 README 仅「建设中」（MIT）；LocoWiki 无 LICENSE；LocoWiki.github.io 在 LocoWiki 组织下（MIT）。

## BOM
- 有。官方 `3.Document/BOM.xlsx`（BOM 页 29 行采购表 + 「URDF重量实测」页按件质量），已整理为 `data/boms/struct-htdw4438.json`，校验通过：29 行、100 件、已标价 ¥15182.45、1 行无价（XT30 线材）。

## openness 判断
- 记 `full`：官方 BOM + SolidWorks 全零件/总装 + URDF + 实机 SDK + 三套训练框架同时在公开仓库。
- 保留：无自制 PCB（主控/电池/电机为高擎成品，hardware/firmware 留空）；sim2real 部署仓尚未填内容；主仓与 LocoWiki 无许可证，AMP 为非商用。

## 未核实
- 整机实称质量：URDF 4.36 kg 与 BOM 按件合计约 5.4 kg 不一致，官方无实称值，speed_max_mps / payload / 续航留空。
- HTDW-4438 具体减速比与轴承版本；是否随整机配相机/遥控器。
