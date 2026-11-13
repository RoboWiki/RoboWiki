# 架构：核心数据仓

> 定位：面向机器人部件的可追溯工程知识库。核心是参数可追溯的部件库；选型台是试验工具；Issue 收集部件实测与评价；再逐步打通机械 / 硬件 / 嵌入式 / 算法与系统集成的全链路。

一句话：**本仓只负责「事实」**——部件、整机、材料、工艺、软件、渠道、关系与图片；
网站与部署都在 [RoboWiki/RoboWiki.github.io](https://github.com/RoboWiki/RoboWiki.github.io)。

> 本文取代拆仓前的同名文档。历史裁定见 [ADR-006](ADR-006-split-repos-2026-11-02.md)；
> ADR-002/003 中「不物理拆仓」的部分已被取代，其余 ID、来源、许可、发布物结论继续有效。

## 两仓契约

| 仓 | 负责 | 不负责 |
|---|---|---|
| `RoboWiki/RoboWiki`（本仓） | `data/`、`schema/`、`assets/`、校验、数据发布 | 页面、API、UGC、部署 |
| `RoboWiki/RoboWiki.github.io` | VitePress、FastAPI、控制台、Docker/Caddy、分享与 PWA | 数据副本、schema 修改、产品图副本 |

**契约是 release，不是 main。** 站点通过 `data.lock.json` 锁定 `data-vYYYY.MM.N`，
下载 tar.gz 后校验 `SHA256SUMS.txt` 再构建；运行时不会读 `raw.githubusercontent.com`。

## 目录

```
data/
  catalog/<category>/<vendor>.json   部件（A/B 进目录，C 仅线索）
  robots/<vendor>.json               整机
  materials/<group>.json             材料 + 加工工艺
  software.json / suppliers.json     软件 / 渠道
  offers/<vendor>.json               优惠
  taxonomy.json / semantics.json     品类与口径注册表
  _id_registry.json                  永久 ID 账本（只追加）
schema/                              JSON Schema 与口径说明
assets/parts/                        产品图（版权归原方，逐条 image_source）
pipeline/                            校验与入库，不生成页面
tools/                               ID 注册表、数据导出
docs/                                ID、版本化、CI、ADR
```

## 写路径

```
站内表单 / 控制台提案
        │  (站点仓 API: submissions → review)
        ▼
   outbox worker ──► 本仓 PR（proposal/<id> 分支）
        │
        ▼
   人工合并 main ──► tag data-v* ──► Data release
        │                              │
        ▼                              ▼
  站点更新 data.lock ◄──── tar.gz + MANIFEST + SHA256
```

- **目录字段只由 release 写。** 站点后台不会直接改 `parts`；提案通过只入 outbox。
- 直接 PR 仍是最短路径，适用于批量导入、结构调整和口径修改。
- 合并 ≠ 生效：站点必须更新 `data.lock.json` 并重新构建，页面才会切换。

## 数据分层

| 层 | 规则 |
|---|---|
| A | 逐项核对厂商手册/官方文档；同品类 A 级字段键集一致 |
| B | 公开商品页或第三方整理；不冒充 A，不在页面显示「已核对」 |
| C | 转述线索；默认不参与推荐/对比，站点与 API 不投影进目录 |

- 缺失写 `null`，不省略 key；不猜、不用同类填补。
- 扭矩统一到输出端，`tau_basis` / `inertia_basis` 必填；改口径升 `semantics.version`。
- 图片必须有 `image_source`；收到权利人通知先下架。
- ID 永久：新增登记，改名 `alias_of`，删除墓碑；见 [ID-POLICY](ID-POLICY.md)。

## 校验与发布

```bash
python -m pipeline validate        # 数据闸门：口径、量程、ID、材料/工艺交叉引用
python -m pytest -q                # 数据治理与 taxonomy 测试
python tools/export_data.py --out dist --tag data-vYYYY.MM.N
```

发布 workflow 会重复校验，再调同一个导出脚本；`MANIFEST.json` 记录
parts / robots / software / materials / processes / ids / assets 与 `semantics_version`。
下游按 tag + SHA-256 + MANIFEST 三件套引用，流程见 [DATA-VERSIONING](DATA-VERSIONING.md)。

## 本仓不做什么

- 不构建站点、不跑 VitePress、不提供 API 或数据库。
- 不存 UGC（评价、评论、投票、举报）；它们属于站点仓 Postgres。
- 不存厂商原始 PDF、整包抓取缓存或未授权大文件。
- 不在运行时被站点直接读取；所有消费都经过 release。

## 规模与演进

- 构建时间、图片体积、CDN 是站点仓的问题；本仓只保证数据可校验、可打包、可复现。
- 数据量增长时优先拆 `data/materials`、`data/robot_ecosystem` 等独立发布物，
  而不是引入服务。
- 只有出现「第二个按版本消费数据的独立方」且同步成本真实发生时，才考虑再拆数据子仓；
  ADR-006 已记录当前拆分边界。
