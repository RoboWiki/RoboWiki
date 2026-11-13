# OpenDoge V1.1（struct-opendoge-v1）BOM 发现

- 数据文件：`data/boms/struct-opendoge-v1.json`（12 行、26 件、全部无价）
- 结论：**官方没有发布 BOM**。按 `data/boms/README.md` 的严格口径，这台在官方 BOM 发布前应标 `missing`；本次仍落了一个“可核对的器件骨架”，所有行都有官方出处、价格全为 null，请勿当官方 BOM 引用。

## 0. “BOM 不存在”的检索证据（先说结论）

| 检查 | 结果 |
| --- | --- |
| `OpenDoge_origin` README Status 表 | `BOM / assembly docs ⬜ In progress` https://github.com/OpenDogeRobotics/OpenDoge_origin#status |
| `OpenDoge_origin` Roadmap | `[ ] Complete BOM, assembly guide, and v1.0 release`（未勾选）https://github.com/OpenDogeRobotics/OpenDoge_origin#roadmap |
| `OpenDoge_hardware` 仓库根目录 | 只有 `.gitignore`、`OpenDog.SLDASM/`、`README.md`、`datasheets/`、`mechanical/` https://github.com/OpenDogeRobotics/OpenDoge_hardware |
| `OpenDoge_hardware` README | 目录结构里没有 BOM/物料表，只有 CAD 与器件规格书 https://github.com/OpenDogeRobotics/OpenDoge_hardware/blob/main/README.md |
| 全组织递归 tree 检索（origin / hardware / description / deploy / train / OpenDogeWorkspace / GOUJIAO） | 关键词 `bom|物料|清单|采购|装配` 与 `*.xlsx|*.xls|*.csv` 均未命中 BOM 表（唯一 CSV 是 `OpenDog.SLDASM/urdf/OpenDog.SLDASM.csv` 的 URDF 关节表） |

## 1. 应补到 `artifacts.bom` 的官方 URL 建议

现状：`data/robots/opendoge.json` 里 `artifacts` 没有 `bom` 字段（`openness_note` 已写“BOM 与装配文档官方仍标为进行中”）。（本次任务不改 robots 数据）

建议方案（按优先级）：

1. **推荐：不填 `bom`，补 `bom_status: "in_progress"`**，并在 `openness_note` 保留“BOM 未发布”。理由是 `data/boms/README.md` 明确要求“官方未发布 BOM 的整机不建文件、标 missing”，填一个不是 BOM 的链接会让读者误以为有清单。
2. 若页面必须给一个可点的“物料出处”，用 **hardware 仓库根 + datasheets**，这是官方唯一按器件分目录放资料的入口：
   - `https://github.com/OpenDogeRobotics/OpenDoge_hardware`（BOM 位置）
   - `https://github.com/OpenDogeRobotics/OpenDoge_hardware/tree/main/datasheets`（EL05 手册、DM-IMU-L1 手册/固件/例程、CHIWU 原理图、Orange Pi 5 资料）
3. 器件“应有清单”的官方文字出处（本 BOM 12 行的依据）：
   - 规格表：`https://github.com/OpenDogeRobotics/OpenDoge_origin#robot-specification`
   - 电源/急停要求：`https://github.com/OpenDogeRobotics/OpenDoge_deploy/blob/main/docs/调试与上机操作手册.md`
   - 实机硬件问题记录（CHIWU 24 V、USB2CAN、CAN 拓扑）：`https://github.com/OpenDogeRobotics/OpenDoge_deploy/blob/main/docs/上机问题与代码修改记录.md`
4. 可另加字段 `bom_tracker_url: "https://github.com/OpenDogeRobotics/OpenDoge_origin#roadmap"`，让读者自己看进度。

## ① BOM 用到、站内 taxonomy 没有的行业品类

| 品类 | OpenDoge 里的样子 | 站内现状 | 证据 |
| --- | --- | --- | --- |
| 关节模组散热/减振件 | 12 个 EL05 连续跑策略会发热，部署侧配了阻尼/故障降级（无独立散热件） | `thermal` 在 BOM schema 里有，站内 22 品类无散热品类 | https://github.com/OpenDogeRobotics/OpenDoge_deploy/blob/main/docs/上机问题与代码修改记录.md |
| 足端/打印耗材（TPU/橡胶、PLA/PETG/尼龙） | “可 3D 打印也可 CNC”，足端建议 TPU/橡胶 | 无耗材品类 | https://github.com/OpenDogeRobotics/OpenDoge_origin#robot-specification |
| CNC 加工服务 | 机身大型件建议 CNC 铝合金 | 无外协加工/服务品类 | https://github.com/OpenDogeRobotics/OpenDoge_hardware/blob/main/README.md |
| 物理急停 / 断电开关 | 上电前必检项，要求能物理切断电机 24 V | `equipment`、`power` 均无“急停”子类 | 同上调试与上机操作手册 |
| 整机套件/散件包 | 官方无套件；公开教程（GOUJIAO）在教“自己买齐” | 站内无套件商品形态 | https://github.com/OpenDogeRobotics/GOUJIAO |

## ② 高价值、但部件库缺失的件

1. **CHIWU 四路 CAN 转接板（尺物电机驱动板）** —— 12 个电机的唯一通信枢纽，站内无尺物品牌；同类只有达妙 Link4C（`damiao-dm-linkx-4c`）与灵足 USB-CAN HUB（`lingzu-robstride-usb-can-hub`），都不是同一产品。
   - 证据：原理图 PDF + STEP + 例程 https://github.com/OpenDogeRobotics/OpenDoge_hardware/tree/main/datasheets/chiwu
   - 部署侧证据（以两个 USB2CAN 设备出现，4 路 CAN，24 V 供电）：https://github.com/OpenDogeRobotics/OpenDoge_deploy/blob/main/docs/上机问题与代码修改记录.md
2. **Orange Pi 5（RK3588S，非 Plus）** —— 上位机，站内只有 `cont-orange-pi-5-plus-8gb`（5 Plus 是不同板）。官方也没写内存容量。
   - 证据：https://github.com/OpenDogeRobotics/OpenDoge_origin#robot-specification ；CAD `OPi5_pcb_asm-0809.stp`
3. **24 V 动力电源（电池或开关电源）+ 面板电压表 + 降压模块 + 金属开关 + JP30 电源线** —— 整套电源链在官方 CAD 里都是独立零件，站内只有通用 DC-DC（`ti-lm2596`）、船型开关（`generic-rocker-switch`），无一可精确匹配。
   - 证据：`mechanical/V1.1/降压模块.SLDPRT`、`电压表.SLDPRT`、`金属开关.SLDPRT`、`jp30（福来翔-23）线.SLDPRT` https://github.com/OpenDogeRobotics/OpenDoge_hardware/tree/main/mechanical/V1.1
4. **Xbox 兼容 2.4G 手柄（具体型号）** —— 官方只写“Xbox 兼容 2.4G”，站内 `remote_controller` 全是 RC 遥控器（DJI DR16/DT7、RadioLink AT9S），没有游戏手柄类目。
   - 证据：https://github.com/OpenDogeRobotics/OpenDoge_deploy/tree/main/hardware/gamepad
5. **DM-IMU-L1 已在库**（`damiao-dm-imu-l1`）、**EL05 已在库**（`灵足-robstride-el05`）——这两件是全机唯一能精确匹配的，说明 OpenDoge 的缺口集中在“CAN 板 + 电源链 + 上位机”三处。

## ③ 可联动的设备工具（站内已有 equipment 条目）

| 设备 | 站内 id | 联动理由与证据 |
| --- | --- | --- |
| Makera Carvera 桌面 CNC | `carvera` | 官方建议机身大型结构件用 CNC 铝合金提升刚性 |
| 拓竹 P1S / A1 | `bambulab-p1s` / `bambulab-a1` | 409 个零件的打印主力；官方建议打印后用 STEP 导 STL |
| 创想 Ender-3 V3 | `creality-ender-3-v3` | 低成本入门打印方案 |
| 正点原子 DL16 逻辑分析仪 | `alientek-dl16` | 4 路 CAN 1 Mbps 波形/帧排查（部署侧有一传三 CAN、丢包 10% 的实测记录） |
| 优利德 UT210E 钳形表 | `uni-t-ut210e` | 12 个 EL05 的 24 V 总电流与单腿电流分配 |
| 正点原子 DP100 / ISDT MP305A 可调电源 | `alientek-dp100` / `isdt-mp305a` | 上电顺序 dry → damping → low-gain 需要限流电源；也可给 CHIWU 单独 24 V |
| 优利德 UT61E 万用表 | `uni-t-ut61e` | 对照面板电压表核对 24 V 母线压降 |

证据：https://github.com/OpenDogeRobotics/OpenDoge_deploy/blob/main/docs/调试与上机操作手册.md

## ④ 可联动的采购库渠道

- 官方没有指定任何供应商/店铺，也没有购买链接（与 SO-101 完全相反），这是采购库“无官方渠道可挂”的典型：只能落到品类页 + 通用渠道。
- 可参考的三方渠道（非官方，仅作补充，入采购库前需核实）：
  - 灵足 RobStride 官网（EL05 原厂）https://www.robstride.com/
  - 达妙 DAMIAO（DM-IMU-L1 原厂仓库，站内条目 `damiao-dm-imu-l1` 的 url）https://gitee.com/kit-miao/dm-imu
  - 香橙派官方产品页（Orange Pi 5）http://www.orangepi.org/html/hardWare/computerAndMicrocontrollers/details/Orange-Pi-5.html
- 公开教学口径（**非官方 BOM，不得写入 BOM**）：GOUJIAO 教程写“EL05 约 400 元/个，12 个约 4800 元，加打印件总成本约 8000 元”。
  https://github.com/OpenDogeRobotics/GOUJIAO/blob/main/content/docs/02-hardware/actuators.mdx
  https://github.com/OpenDogeRobotics/GOUJIAO/blob/main/content/docs/02-hardware/hardware-architecture.mdx

## ⑤ 适合 RoboWiki 定位的其他发现

1. **“链路完整、BOM 缺失”是 OpenDoge 最大的反差**：CAD/URDF/MJCF/训练/部署/浏览器仿真全通，唯独 BOM 与装配文档缺失，且官方自己标了 ⬜。适合在方案页做成“资料完整度”徽标案例：机械/固件/仿真 ✅，BOM ❌。
2. **电压规格站内为空，但官方文档有 24 V**：`opendoge.json` 的 `voltage_V` / `voltage_range_V` 为 null，而部署手册明确“电机独立 24 V 动力电”“CHIWU 的 24 V 不要与电机动力电共开关”。这是可补的硬参数（本次不改 robots 数据）。
3. **BOM 口径提醒**：README 说 “CHIWU 4×CAN”，部署日志里却是 `/dev/USB2CAN0` + `/dev/USB2CAN1` 两个 SOULDE 设备——很可能是一块板出两个 USB-CAN 设备（各 2 路）。页面若写“4 路 CAN 模块”应同时给出这个细节，否则用户按“一块 USB-CAN 就能跑”买会踩坑。
4. **12 个 EL05 是成本主体**：按站内 EL05 参考价 `¥299`（2026-10-31 历史值）估 12 个约 ¥3.6k，而公开教程按 ~¥400/个说 ¥4.8k。两套口径差 30%，正好可以做成“参考价 vs 外部实付”对照（BOM 本身仍不填价）。
5. **许可分裂**：train/deploy/站点 Apache-2.0、description BSD、hardware 仓未见明确 LICENSE。做硬件复刻页时必须提示“CAD 许可未明示”，这是全开源方案里少见的许可空洞。
   证据：https://github.com/OpenDogeRobotics/OpenDoge_origin#license
6. **实物已走起来、RL 还在调**：README 写“PD 站立 OK、RL 行走仍在调”，并给出高频抖动/CAN 回包时序/IMU 噪声三类问题的实测记录。这类“真实失败记录”对 RoboWiki 复刻者价值极高，建议在方案页直接外链 hardware issue log。
