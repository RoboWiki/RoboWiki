# OpenDoge V1.1 生态与契约核验（2026-11-10）

## 仓库核验（gh api repos/<owner>/<repo>，均 HTTP 200、未归档）
- OpenDoge_origin — 官方项目 / 总览与契约；无 LICENSE 文件。
- OpenDoge_hardware — 官方结构资产（V1.1 CAD/STEP/3MF + datasheets）；无 LICENSE。
- OpenDoge_description — URDF/STL/RViz/Gazebo/MJCF；URDF/package.xml 声明 BSD。
- OpenDoge_train — 训练/评估/ONNX 导出；Apache-2.0；LainLab- 为历史前缀。
- OpenDoge_deploy — C++ 非 ROS 真机运行时；Apache-2.0；运行时已迁移 48 维契约。
- OpenDogeRobotics.github.io — 浏览器仿真源码；Apache-2.0；站点 https://opendogerobotics.github.io/ 返回 200。
- opendoge_ros2_core — ROS2 Humble ros2_control 工作区（opendoge-apx 变体）；Apache-2.0；2025-12 后未更新。
- OpenDoge_URDF — 早期 URDF 包，已被 description 覆盖；无 LICENSE。
- LainLab — 训练上游；组织内为 Lain-Ego0/LainLab 的 fork（Apache-2.0），homepage https://lain-ego0.github.io/playground/ 返回 200。
- GOUJIAO — 中文教程站源码（Next.js + Fumadocs，24 篇 mdx 含 OpenDoge 六仓内容）；无 LICENSE，无公开站点地址。
- BEEF-ROS2 — 通用中文 ROS2 实战教程；MIT；README 与仓库树无 OpenDoge 关联。
- rl_sar — 第三方通用 sim2real 框架（fan-ziqi，Apache-2.0）；组织内有 fork；非直系子仓。

## 契约数字来源
- origin 契约：OpenDoge_origin/README_cn.md 第 15、96 行及「跨仓库契约」表——48 维观测（lin_vel3+ang_vel3+gravity3+q12+dq12+last_action12+cmd3）、12 维动作、Kp=12、Kd=0.5（实机 0.8）、action_scale=0.25；开发计划.md 记录 49→48 维迁移。
- deploy 旧说明：OpenDoge_deploy/README.md 第 78–83 行仍写 UniLab 策略 49 维 / Kp=20 / Kd=0.3 / action_scale=0.50。
- deploy 当前实现：deploy/include/opendoge_deploy/types.hpp 为 kObsDim=48、kp=12.0、kd=0.5、action_scale=0.25；2026-11-08 提交「迁移 LainLab 部署契约」与 docs/lainlab_deploy_migration.md 记录同一迁移，旧 opendoge_r5.onnx 不兼容。结论：README 属旧策略说明，当前运行时与 origin 契约一致。

## 未确定项
- GOUJIAO 的在线地址与许可证；origin/hardware/OpenDoge_URDF 许可证缺失。
- deploy README 未随代码更新，易被误读为 49 维 / Kp=20 / action_scale=0.50。
- LainLab fork 与上游的同步频率、rl_sar 组织 fork 是否继续维护。
- BOM/装配文档仍未发布，artifacts 保持无 bom/assembly。
