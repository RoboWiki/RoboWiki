# ADR-006：拆分核心数据仓与站点仓（2026-11-02）

> 状态：**已裁定 · 执行中** · 取代 ADR-002（单仓裁定）与 ADR-003（单仓最终架构）中
> “不物理拆仓”的部分；ADR-002/003 的其他结论（ID、来源、许可、发布物）继续有效。

## 背景

ADR-002/003 在 2026-10-30 裁定“暂不拆仓”，触发条件是：体量近 1GB、出现第二个按版本
消费数据的独立方、贡献者 >10 且数据/站点人员不重叠、数据与站点发布节奏解耦。

2026-11-02 维护者决定提前拆分，理由是：

1. 下一阶段要把 RoboWiki 作为**公共流量入口**，数据要能被 bot、小程序、合作方 API
   等多个消费者复用；
2. 数据仓需要独立版本（`data-v*`）、独立许可证与独立审核权限；
3. 图片进核心仓后，数据发布物可以自足，不再依赖站点仓的 `console/public/parts`。

这不是“体量触发”，而是**产品方向触发**；记录在此，避免以后误读 ADR-002。

## 裁定

- `RoboWiki/RoboWiki`：核心数据仓。
  - `data/`、`schema/`、`assets/parts/`
  - `pipeline/` 只做校验与入库，不生成站点
  - `tools/export_data.py` 发布 `data-vYYYY.MM.N`
  - 许可证：AGPL-3.0（维护者选择；2026-11-08 由 GPL-3.0 改为 AGPL-3.0）
- `RoboWiki/RoboWiki.github.io`：前端站点仓。
  - `wiki/`、`console/`、`backend/`、站点构建脚本
  - 不再保存 `data/`、`schema/`、产品图副本
  - `data.lock.json` 锁定核心仓 release
  - 构建时下载 release，校验 `MANIFEST.json` 与 `SHA256SUMS.txt`

## 契约

1. 核心仓 `main` 不是契约，**release 才是**；前端只认 `data-v*`。
2. 发布物包含 `data/`、`schema/`、`assets/`；`MANIFEST.json` 记录条数与
   `semantics_version`、图片数。
3. 前端构建失败时回退到上一个锁定版本，不允许运行时读 `raw.githubusercontent.com`。
4. 跨仓通知用 `repository_dispatch`，同时保留定时重建兜底；token 过期不应导致站点静默过期。
5. 数据问题进核心仓 issue；页面/样式/交互进站点仓 issue。

## 迁移步骤

1. 核心仓用 `git filter-repo` 按目录保历史切分（已完成本地切分）。
2. 站点仓把 `DATA_DIR`/`SCHEMA_DIR`/`ASSETS_DIR` 改为环境变量可指向 release（已提交）。
3. 核心仓发布首个 `data-v2026.11.0`。
4. 站点仓加 `data.lock.json`，删除 `data/`、`schema/`、`console/public/parts` 副本。
5. 启用 `Data release` + `repository_dispatch` + 定时兜底。
6. 观察 2 个赛季；若跨仓同步成为故障源，回退到单仓不丢数据（release 可重建站点）。

## 风险

- 两仓漂移：用 release + lockfile + 契约测试兜住。
- 图片版权：逐条 `image_source`，收到通知先下架。
- 贡献摩擦：数据贡献者不需要懂前端；站点贡献者不需要懂 schema。
- 许可证：AGPL-3.0 对数据复用不如 CC 宽松；维护者已知悉并选择。
