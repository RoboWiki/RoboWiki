# CI：核心数据仓

核心仓的 CI 只有一条主线，不做站点分层：

```text
PR / push main
  └─ validate   python -m pipeline validate
  └─ test       python -m pytest -q
```

实现文件：`.github/workflows/pr-gate.yml`。

## 为什么简单

本仓没有前端、没有 API、没有容器；所有 PR 都只改数据、schema、图片、校验器或工具。
数据闸门本身只要十几秒，拆层省不下多少时间，反而增加「某层没跑」的风险。

| 检查 | 覆盖 |
|---|---|
| `pipeline validate` | 字段/单位/量程、A 级键集、来源等级、ID 注册表、材料↔工艺↔渠道交叉引用 |
| `pytest` | ID 治理、taxonomy、材料 schema、导出与 schema 一致性 |

## 发布流水线

`Data release` 是独立 workflow，只在打 `data-v*` tag 或手动触发时运行：

1. `pip install -e .`
2. `python -m pipeline validate`
3. `python tools/export_data.py --out dist --tag <tag>`
4. 上传 tar.gz / MANIFEST / SHA256SUMS 到 Release

发布物与站点解耦：站点只认 `data.lock.json` 锁定的 release。

## 新增检查的原则

- 数据规则优先放进 `pipeline/validate.py`，而不是只写在文档或测试里。
- 测试用于锁住「操作入口与闸门口径一致」（如 `tools/id_registry.py` 与
  `validate.check_id_registry`）。
- 不引入需要外部服务、网络或数据库的检查。
- 材料/工艺新增字段时，同时更新 `schema/material.schema.json`、`validate.py` 与
  对应的 `data/materials` 文件；只改其中一处会在 PR 里红。
