# RoboWiki Data

> RoboWiki：面向机器人部件的可追溯工程知识库。以参数可追溯的部件库为核心，选型台作为试验工具，社区共建每个部件的实测与评价；再逐步打通机械—硬件—嵌入式—算法与系统集成的制作全链路。本仓是这个知识库的数据底座。
>
> 部件库与采购是当前主线；选型台为试验版，四层 + 系统集成是全链路骨架，按阶段补。

**RoboWiki 的唯一数据事实源：部件、整机、材料、工艺、软件、渠道、评分快照与产品图。**

站点代码在 [RoboWiki/RoboWiki.github.io](https://github.com/RoboWiki/RoboWiki.github.io)，线上地址 <https://robowiki.org.cn/>。

```
413 条目录数据（部件库 338 + 设备库 75） · 32 种材料 + 9 种工艺
42 台整机 · 22 个软件 · 234 家渠道 · 699 张产品图
```

## 仓库职责

| 目录 | 内容 |
|---|---|
| `data/` | 唯一事实源：`catalog/`、`robots/`、`materials/`、`offers/`、`software.json`、`suppliers.json`、`taxonomy.json`、评分/实测快照与注册表 |
| `schema/` | 数据契约：字段、类型、枚举、口径与 `semantics.version` |
| `assets/parts/` | 随条目托管的产品图；版权归原厂/原商城，出处逐条写在 `image_source` |
| `pipeline/` | `validate` 数据闸门，以及评分 / 实测快照的导入逻辑 |
| `tools/` | ID 注册表、发布导出与一次性数据整理脚本 |
| `docs/` | 数据治理、版本化、ID 规则与架构决策 |
| `tests/` | 数据闸门、语义、分类与发布物测试 |

**站点仓不保存数据副本。** 它通过 `data.lock.json` 锁定本仓的 `data-v*` release，构建时下载并校验 SHA-256。

## 快速开始

```bash
python -m pip install -e ".[dev]"

python -m pipeline validate       # 数据闸门：字段、口径、ID、分类
python -m pytest                  # 核心测试
python tools/id_registry.py --check
```

发布物试跑（产物写到 `dist/`，不要提交）：

```bash
python tools/export_data.py --out .tmp-data-export --tag data-v2026.11.11.2
```

## 数据发布

打 `data-v*` tag，或在 Actions 里手动触发 **Data release**。流程会先跑数据闸门，再产出：

| 附件 | 内容 |
|---|---|
| `robowiki-data-<version>.tar.gz` | `data/` + `schema/` + `assets/` 的只读快照 |
| `MANIFEST.json` | 条目数、ID 数、semantics 版本、图片数与生成时间 |
| `SHA256SUMS.txt` | 上面两个文件的 SHA-256 |

下游必须 pin 版本并记录 `MANIFEST.json`，不要跟 `main` 的 HEAD。
站点侧更新 `data.lock.json` 后，Pages 会重新下载、校验并构建。

## 三条硬规则

1. **缺失写 `null`**：不猜、不省略 key。`null` 表示厂商没公布，不是 0。
2. **ID 永久**：新增登记；改名留 `alias_of`；删除留 `removed`。见 [docs/ID-POLICY.md](docs/ID-POLICY.md)。
3. **有图必写 `image_source`，有仓库必写 `repo_license`**；读不到就写 `null`。

补充口径：

- 扭矩、转速一律指输出端（含减速箱）；原始值和换算过程保留在 `specs` / `notes`。
- 来源等级 `A/B/C`：A 逐项核对厂商手册，B 公开网页，C 转述线索；C 不进推荐与对比。
- 同一品类 / 子类的 A 级字段键集必须一致，数据闸门会拦。

## 贡献

- 纠参数、补数据：直接改对应 JSON 后提 PR；先跑 `python -m pipeline validate`。
- 新增型号：先在 `data/_id_registry.json` 登记 ID，再补 `data/catalog/<category>/`。
- 写实测 / 评分：走站点仓库的 issue 表单或互动端，快照由 `pipeline/ingest_*` 聚合，**不要手改快照**。
- 产品图：放进 `assets/parts/`，并在条目里写 `image_source` 与 `last_checked`。

完整流程见 [CONTRIBUTING.md](CONTRIBUTING.md)。

## 许可证

本仓代码与整理成果按 **AGPL-3.0** 发布，全文见 [LICENSE](LICENSE)。
厂商手册、商品图与第三方仓库的权利归原方，详见 [NOTICE.md](NOTICE.md) 与条目字段。
