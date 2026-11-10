# -*- coding: utf-8 -*-
"""校验 data/boms/*.json 的结构、算术与交叉引用。"""
from __future__ import annotations

import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
BOMS = ROOT / "data" / "boms"

CATEGORIES = {
    "actuator", "actuator_driver", "controller", "compute", "sensor",
    "perception", "power", "wiring", "pcb", "structural", "printed_part",
    "fastener", "transmission", "thermal", "interface", "cable_management",
    "consumable", "tooling", "service", "misc",
}
REQUIRED = {"robot_id", "robot_name", "source", "currency", "price_basis",
            "lines", "totals", "unresolved", "completeness"}
LINE_REQUIRED = {"id", "category", "name", "qty", "unit_price", "currency",
                 "subtotal", "catalog_part_id", "supplier_id", "equipment_id"}


def catalog_ids() -> set[str]:
    out: set[str] = set()
    for f in (ROOT / "data" / "catalog").glob("*/*.json"):
        for row in json.loads(f.read_text(encoding="utf-8")):
            if isinstance(row, dict) and row.get("id"):
                out.add(row["id"])
    return out


def supplier_ids() -> set[str]:
    rows = json.loads((ROOT / "data" / "suppliers.json").read_text(encoding="utf-8"))
    return {r["id"] for r in rows if r.get("id")}


def main() -> int:
    errors: list[str] = []
    cat_ids = catalog_ids()
    sup_ids = supplier_ids()
    wanted = set(sys.argv[1:])
    files = sorted(BOMS.glob("*.json"))
    if wanted:
        files = [f for f in files if f.stem in wanted]
    if not files:
        print("data/boms 下没有清单" if not wanted else f"找不到：{sorted(wanted)}")
        return 1
    seen_robots: set[str] = set()

    for path in files:
        name = path.name
        try:
            doc = json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            errors.append(f"{name}: JSON 读不了（{exc}）")
            continue
        if not isinstance(doc, dict):
            errors.append(f"{name}: 顶层必须是对象")
            continue
        missing = REQUIRED - set(doc)
        if missing:
            errors.append(f"{name}: 缺字段 {sorted(missing)}")
            continue
        rid = doc["robot_id"]
        if rid != path.stem:
            errors.append(f"{name}: robot_id={rid} 与文件名不一致")
        if rid in seen_robots:
            errors.append(f"{name}: robot_id 重复")
        seen_robots.add(rid)
        if not str(doc["source"].get("url") or "").startswith("http"):
            errors.append(f"{name}: source.url 缺失或非 http")
        if doc["currency"] not in ("CNY", "USD", "EUR", "JPY", "GBP"):
            errors.append(f"{name}: currency={doc['currency']} 不在允许列表")

        lines = doc["lines"]
        if not lines:
            errors.append(f"{name}: lines 为空")
        line_ids: set[str] = set()
        priced = 0.0
        unpriced = 0
        items = 0
        by_cat: dict[str, float] = {}
        for i, line in enumerate(lines, 1):
            tag = f"{name} line#{i}"
            missing = LINE_REQUIRED - set(line)
            if missing:
                errors.append(f"{tag}: 缺字段 {sorted(missing)}")
                continue
            if line["id"] in line_ids:
                errors.append(f"{tag}: id 重复（{line['id']}）")
            line_ids.add(line["id"])
            if line["category"] not in CATEGORIES:
                errors.append(f"{tag}: category={line['category']} 不在品类别表")
            qty = line["qty"]
            if not isinstance(qty, (int, float)) or qty <= 0:
                errors.append(f"{tag}: qty 必须是正数")
                continue
            items += qty
            price, sub = line["unit_price"], line["subtotal"]
            if price is None:
                unpriced += 1
                if sub is not None:
                    errors.append(f"{tag}: 单价为空但 subtotal 有值")
            else:
                want = round(float(price) * float(qty), 2)
                if sub is None or abs(float(sub) - want) > 0.011:
                    errors.append(f"{tag}: subtotal={sub} 应为 {want}")
                else:
                    priced += float(sub)
                    cat = line["category"]
                    by_cat[cat] = round(by_cat.get(cat, 0.0) + float(sub), 2)
            cid = line.get("catalog_part_id")
            if cid and cid not in cat_ids:
                errors.append(f"{tag}: catalog_part_id={cid} 不在部件目录")
            sid = line.get("supplier_id")
            if sid and sid not in sup_ids:
                errors.append(f"{tag}: supplier_id={sid} 不在供应商库")
            eid = line.get("equipment_id")
            if eid and eid not in cat_ids:
                errors.append(f"{tag}: equipment_id={eid} 不在设备目录")

        totals = doc["totals"] or {}
        checks = {
            "line_count": len(lines),
            "item_count": items,
            "priced_subtotal": round(priced, 2),
            "unpriced_lines": unpriced,
        }
        for key, want in checks.items():
            got = totals.get(key)
            if got is None:
                errors.append(f"{name}: totals.{key} 缺失")
            elif abs(float(got) - float(want)) > 0.011:
                errors.append(f"{name}: totals.{key}={got} 应为 {want}")
        got_cat = totals.get("by_category") or {}
        for cat, amount in got_cat.items():
            if cat not in by_cat or abs(float(amount) - by_cat[cat]) > 0.011:
                errors.append(f"{name}: totals.by_category[{cat}]={amount} 应为 {by_cat.get(cat, 0)}")
        for cat, amount in by_cat.items():
            if cat not in got_cat:
                errors.append(f"{name}: totals.by_category 缺 {cat}={amount}")

    if errors:
        print(f"BOM 校验失败：{len(errors)} 个问题")
        for e in errors:
            print("  ERROR", e)
        return 1
    print(f"BOM 校验通过：{len(files)} 台")
    return 0


if __name__ == "__main__":
    sys.exit(main())
