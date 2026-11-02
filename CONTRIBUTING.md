# 贡献指南（核心数据仓）

这个仓只放**数据、关系、schema 与图片**，不构建网站。网站前端在
[RoboWiki/RoboWiki.github.io](https://github.com/RoboWiki/RoboWiki.github.io)。

## 先跑一次

```bash
python -m pip install -e ".[dev]"
python -m pipeline validate
python -m pytest -q
python tools/id_registry.py --check
```

只改 JSON 时，最少跑 `python -m pipeline validate`。

## 改什么 → 改哪里

| 我要… | 改这个文件 |
|---|---|
| 加/改部件 | `data/catalog/<品类>/<厂商slug>.json` |
| 加/改整机 | `data/robots/<厂商slug>.json` |
| 加/改软件 | `data/software.json` |
| 加/改渠道 | `data/suppliers.json` |
| 加/改优惠 | `data/offers/<厂商slug>.json` |
| 改字段口径/红线 | `schema/semantics.json`（升 version） |
| 加图片 | `assets/parts/<file>`，条目 `image_url` 写 `/parts/<file>` |
| 加新实体 ID | 跑 `tools/id_registry.py` 登记 |

**唯一事实源**：`data/` 与 `schema/`。不要提交网站生成物、页面 HTML、VitePress 产物。

## 四条硬规则

1. **缺失写 `null`**，不猜、不省略 key。
2. **ID 永久**：新增登记，改名 `alias_of`，删除 `removed`；见 [docs/ID-POLICY.md](docs/ID-POLICY.md)。
3. **有图必写 `image_source`**：厂商手册页码 / 商城条目 / 抓取日期；版权归原方。
4. **有仓库必写 `repo_license`**：读不到就写 `null`，不填猜测值。

## 图片

- 放 `assets/parts/`，文件名与条目 `image_url` 的 `/parts/<file>` 对应。
- 不提交厂商原始 PDF、整包抓取缓存、未授权的大文件。
- 收到权利人通知：先下架，后讨论；不要先谈条件。

## 数据发布

维护者打 `data-vYYYY.MM.N` tag，或手动触发 `Data release`。发布物包含
`data/`、`schema/`、`assets/`，附 `MANIFEST.json` 与 `SHA256SUMS.txt`。
下游 pin 版本，不跟 `main` HEAD。详见 [docs/DATA-VERSIONING.md](docs/DATA-VERSIONING.md)。
