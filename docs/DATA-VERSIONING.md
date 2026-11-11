# 数据版本化（DATA-VERSIONING）

`data/` + `schema/` + `assets/` 是本仓的事实源。本仓用 `data-vYYYY.MM.N` 发布只读快照，
站点与外部消费者按版本引用，不跟 `main` HEAD。

实现只有两处，本地与 CI 跑同一份代码：

| 位置 | 作用 |
|---|---|
| [`tools/export_data.py`](../tools/export_data.py) | 打包 + MANIFEST + SHA256 + 自检 |
| [`.github/workflows/data-release.yml`](../.github/workflows/data-release.yml) | 校验 → 导出 → 发 GitHub Release |

## 发布物

| 文件 | 内容 |
|---|---|
| `robowiki-data-<tag>.tar.gz` | `data/`、`schema/`、`assets/` 的只读快照 |
| `MANIFEST.json` | 条目数 + 口径版本 + 生成时间 |
| `SHA256SUMS.txt` | 上面两个文件的 SHA-256 |

附件名规则：`robowiki-data-` + tag 去掉 `data-` 前缀。例：
`data-v2026.11.2` → `robowiki-data-v2026.11.2.tar.gz`。

### MANIFEST 字段

| 字段 | 取自 |
|---|---|
| `parts` | `data/catalog/*/*.json` 条目数（含 C 级线索） |
| `robots` | `data/robots/*.json` 条目数 |
| `software` | `data/software.json` 的 `items` |
| `materials` / `processes` | `data/materials/*.json` 按 `category` 分组计数 |
| `ids` | `data/_id_registry.json` 的 `ids` 数 |
| `semantics_version` | `schema/semantics.json` 的 `version` |
| `assets` | `assets/` 下文件数 |
| `generated_at` | 导出时刻（UTC） |

当前基线（`data-v2026.11.2`）：

```json
{"parts": 418, "robots": 42, "software": 22, "materials": 32, "processes": 9,
 "ids": 953, "semantics_version": "1.1.0", "assets": 690}
```

`parts` 含设备库 69 台；站点部件库只投影非设备条目，所以页面目录是 **349**
（下一版加入 RDK S100 / S100P 后为 420 / 351）。这个差异是预期口径，不是缺失。

## 发布

```bash
python -m pipeline validate
python -m pytest -q
python tools/export_data.py --out dist --tag data-v2026.11.2
```

或打 tag 触发 workflow：

```bash
git tag data-v2026.11.2
git push origin data-v2026.11.2
```

发布前自查：

```bash
git status --porcelain data schema assets   # 必须为空
python -m pipeline validate
python tools/id_registry.py --check
```

导出脚本会自检：归档只含 `data/`、`schema/`、`assets/`；MANIFEST 计数与归档内容一致；
SHA256SUMS 可重算。失败退出码 1，不发布。

## 站点如何消费

站点仓 `data.lock.json` 记录：

```json
{
  "data_version": "data-v2026.11.2",
  "release_asset": "robowiki-data-v2026.11.2.tar.gz",
  "sha256": "<tar.gz 的 SHA-256>",
  "manifest_sha256": "<MANIFEST 的 SHA-256>",
  "counts": {"parts": 418, "materials": 32, "processes": 9, "ids": 953}
}
```

构建流程：

1. `scripts/fetch-data-release.sh` 下载到 `.data/`；
2. `sha256sum -c` 校验；
3. `pipeline build` 读取 `ROBOWIKI_DATA_DIR` / `SCHEMA_DIR` / `ASSETS_DIR`；
4. 页面与 API 响应带 `data-v*` 版本号。

**不要**在站点仓保存数据副本，也不要运行时读 `raw.githubusercontent.com`。

## 版本号

| 版本 | 唯一手写处 | 何时升 |
|---|---|---|
| `semantics.version`（semver） | `schema/semantics.json` | 字段含义/单位/enum/红线变化 |
| `MANIFEST` 计数 | 导出脚本生成 | 条目增减，不升 semantics |
| release tag | git tag | 每次对外快照 |
| 站点 `data.lock.json` | 站点仓 | 每次切换 release |

判据：下游用旧解析代码读新数据会不会读错？会 → major；只是读不到新东西 → minor；
读法完全不变 → patch。只增删条目不改 `semantics.version`。

## 回滚

- 发布不可变：不要移动或覆盖已有 tag。
- 站点回滚只改 `data.lock.json` 指回上一版，重新构建；不改核心仓历史。
- 数据内容有问题：在新 tag 上修复（revert / 新提交），再发一版。
