# 数据工具

这里放**数据采集、清洗、图片处理、ID 注册、发布**相关脚本。站点渲染工具在
[RoboWiki/RoboWiki.github.io](https://github.com/RoboWiki/RoboWiki.github.io)。

## 常用

| 脚本 | 用途 |
|---|---|
| `id_registry.py` | 永久 ID 注册表：`--check` / `--alias` / `--tombstone` |
| `export_data.py` | 打 `data/` + `schema/` + `assets/` 发布物（tar.gz + MANIFEST + SHA256SUMS） |
| `fetch_part_images.py` | 拉取/补齐产品图到 `assets/parts/` |
| `apply_images.py` | 把图片映射写回条目 `image_url` / `image_source` |
| `import_from_inbox.py` | 把 inbox 里认领的图导入 `assets/parts/` |
| `build_catalog.py` / `build_motors.py` | 历史数据构建脚本 |

## 路径约定

- 数据：`data/`
- schema：`schema/`
- 产品图：`assets/parts/`
- 旧脚本里若出现 `console/public/parts`，是拆分前路径；现已统一为 `assets/parts`。

`data/raw/`、`data/_inventory/*.jsonl` 是本地采集缓存，**不进仓库、不进发布物**；
需要时从原始归档重建。

## 注意

这些脚本里有一部分是**一次性历史脚本**（`fix_*`、`apply_absorbed_*`、`fill_*`），
保留是为了可追溯，不保证在最新数据上仍可直接运行。改数据优先走手工 PR + `pipeline validate`。
