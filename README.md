# RoboWiki Data

**RoboWiki 的核心数据仓：部件、整机、软件、渠道、关系与图片来源。**

网站前端在 [RoboWiki/RoboWiki.github.io](https://github.com/RoboWiki/RoboWiki.github.io)，线上地址 <https://robowiki.github.io/>。

```
329 个部件 · 21 台整机 · 22 个软件 · 207 家渠道 · 419 张产品图
```

## 这个仓负责什么

- `data/`：唯一事实源（部件、整机、软件、渠道、评分/评测快照、注册表）。
- `schema/`：数据契约（字段、口径、枚举、语义版本）。
- `assets/parts/`：随条目托管的产品图；版权归原厂/原商城，出处逐条写在 `image_source`。
- `pipeline/`：数据校验与数据入库，不生成网站页面。
- `tools/`：ID 注册表、数据发布导出。
- `docs/`：数据治理、版本化、ID 规则、架构决策。

**网站仓不保存数据副本。** 它从本仓的 release 取数据，按 `data.lock.json` 锁定版本。

## 数据发布契约

打 `data-vYYYY.MM.N` tag，或手动触发 `Data release`，会生成：

| 附件 | 内容 |
|---|---|
| `robowiki-data-<tag>.tar.gz` | `data/` + `schema/` + `assets/` 的只读快照 |
| `MANIFEST.json` | 条目数、ID 数、semantics 版本、图片数、生成时间 |
| `SHA256SUMS.txt` | 上面两个文件的 SHA-256 |

下游应 pin 版本并记录 `MANIFEST.json`；不要跟 `main` 的 HEAD。

## 本地校验

```bash
python -m pip install -e ".[dev]"
python -m pipeline validate       # 数据闸门
python -m pytest                  # 核心测试
python tools/id_registry.py --check
```

发布物试跑：

```bash
python tools/export_data.py --out dist --tag data-2026.11.02
```

## 三条硬规则

1. **缺失写 `null`**，不猜、不省略 key。
2. **ID 永久**：新增登记，改名留 `alias_of`，删除留 `removed`；见 [docs/ID-POLICY.md](docs/ID-POLICY.md)。
3. **有图必写 `image_source`，有仓库必写 `repo_license`**；读不到就写 `null`。

贡献方式见 [CONTRIBUTING.md](CONTRIBUTING.md)。

## 许可证

本仓代码与整理成果按 **GPL-3.0** 发布，全文见 [LICENSE](LICENSE)。
厂商手册、商品图、第三方仓库的权利归原方，逐条见 [NOTICE.md](NOTICE.md) 与条目字段。
