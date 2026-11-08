from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_validate_passes():
    r = subprocess.run(
        [sys.executable, "-m", "pipeline", "validate"],
        capture_output=True, text=True, encoding="utf-8", cwd=str(ROOT),
        env={**__import__("os").environ, "PYTHONIOENCODING": "utf-8", "PYTHONUTF8": "1"},
    )
    assert r.returncode == 0, r.stdout[-3000:] + r.stderr[-2000:]


def test_counts_are_stable():
    from pipeline.load import load_parts

    parts = load_parts()
    assert len(parts) == 300
    robots = []
    for p in sorted((ROOT / "data" / "robots").glob("*.json")):
        robots.extend(json.loads(p.read_text(encoding="utf-8")))
    assert len(robots) == 16
    sw = json.loads((ROOT / "data" / "software.json").read_text(encoding="utf-8"))
    assert len(sw["items"]) == 22
    sups = json.loads((ROOT / "data" / "suppliers.json").read_text(encoding="utf-8"))
    assert len(sups) == 208


def test_asset_provenance_distinguishes_missing_from_explicit_null():
    """`repo_license: null` 表示「查过、没有」，与「没填」是两回事。

    规则文案写着「读不到就写 null」，如果实现把 null 也当缺失报警，
    贡献者会陷入「写 null 被警告、不写也被警告」的死循环。
    """
    from pipeline.validate import check_asset_provenance

    missing = [{"id": "a", "specs": {"repo_urls": ["https://example.com/r"]}}]
    explicit = [{"id": "b", "specs": {"repo_urls": ["https://example.com/r"], "repo_license": None}}]
    declared = [{"id": "c", "specs": {"repo_urls": ["https://example.com/r"], "repo_license": "MIT"}}]

    assert any("repo_license" in msg for msg in check_asset_provenance(missing))
    assert check_asset_provenance(explicit) == []
    assert check_asset_provenance(declared) == []

    # 图片出处同理：缺键要报，显式 null 不报（表示已核、查不到）。
    assert any("image_source" in msg for msg in check_asset_provenance(
        [{"id": "d", "specs": {"image_url": "https://example.com/i.png"}}]))
    assert check_asset_provenance(
        [{"id": "e", "specs": {"image_url": "https://example.com/i.png", "image_source": None}}]) == []


def test_recipe_fields_only_checked_when_present():
    """方案包三件套：没写不报警，写了就必须写对。

    21 台整机目前只有仓库与 URDF，强制要求 BOM 只会逼人编数据；
    但一旦写了 part_id、qty、artifacts，就得能被机器核对。
    """
    from pipeline.validate import check_recipe_fields

    # 三样全缺：不报错也不警告
    assert check_recipe_fields([{"id": "r1"}]) == ([], [])

    # BOM 结构错误
    errors, _ = check_recipe_fields([{ "id": "r2", "bom": [
        {"name": "M3508"},                       # 缺 qty
        {"name": "C620", "qty": 0},              # qty 非正
        {"qty": 2},                              # 缺 name
        "not-an-object",                         # 类型错误
    ]}])
    assert len(errors) == 4, errors

    # part_id 不在部件库：只警告，不阻断（可能是还没收录的件）
    errors, warns = check_recipe_fields([{"id": "r3", "bom": [
        {"name": "自定义结构件", "qty": 1, "part_id": "no-such-part"},
    ]}])
    assert errors == []
    assert any("no-such-part" in w for w in warns)

    # 步骤 order 重复
    errors, _ = check_recipe_fields([{"id": "r4", "steps": [
        {"order": 1, "title": "接线"},
        {"order": 1, "title": "上电"},
        {"title": "调参"},                        # 缺 order 允许
    ]}])
    assert len(errors) == 1 and "order" in errors[0]

    # artifacts：非 http 链接报错，未知键警告，null 合法
    errors, warns = check_recipe_fields([{"id": "r5", "artifacts": {
        "urdf": "https://example.com/a.urdf",
        "cad": None,
        "firmware": "/local/fw.bin",
        "weird": "https://example.com/w",
    }}])
    assert len(errors) == 1 and "firmware" in errors[0]
    assert any("weird" in w for w in warns)
