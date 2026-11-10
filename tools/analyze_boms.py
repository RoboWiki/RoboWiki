# -*- coding: utf-8 -*-
"""从 data/boms/*.json 生成 docs/BOM-ANALYSIS.md。"""
from __future__ import annotations

import collections
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[1]
BOMS = ROOT / "data" / "boms"
OUT = ROOT / "docs" / "BOM-ANALYSIS.md"
INSIGHTS = ROOT / "data" / "boms" / "_insights.md"

BOM_TO_SITE = {
    "actuator": "actuator / servo",
    "actuator_driver": "motor_driver",
    "controller": "controller_low.mcu",
    "compute": "controller_high.sbc",
    "sensor": "imu / sensor",
    "perception": "camera / lidar",
    "power": "power / battery / charger",
    "wiring": "connector.cable / terminal",
    "pcb": "open_hw.control / module",
    "structural": "structural.plate",
    "printed_part": "structural.printed（新增）",
    "fastener": "structural.fastener",
    "transmission": "structural.bearing / belt / gear / shaft",
    "thermal": "open_hw.accessory（暂）",
    "interface": "remote_controller / power.switch",
    "cable_management": "connector.cable",
    "consumable": "材料库 / 设备耗材",
    "tooling": "设备库（工具 / 仪表）",
    "service": "采购库（加工 / 打样）",
    "misc": "open_hw.accessory",
}


def money(value: float | None, currency: str) -> str:
    return "—" if value is None else f"{value:,.2f} {currency}"


def main() -> None:
    docs = []
    for path in sorted(BOMS.glob("*.json")):
        docs.append(json.loads(path.read_text(encoding="utf-8")))
    boms = [d for d in docs if (d.get("completeness") or {}).get("bom_published") is not False]
    provisional = [d for d in docs if (d.get("completeness") or {}).get("bom_published") is False]

    full = []
    for f in sorted((ROOT / "data" / "robots").glob("*.json")):
        for robot in json.loads(f.read_text(encoding="utf-8")):
            if robot.get("openness") == "full":
                full.append(robot)
    covered = {b["robot_id"] for b in boms}
    provisional_ids = {b["robot_id"] for b in provisional}

    bom_cats = collections.Counter()
    shared = collections.defaultdict(set)
    catalog_hits = 0
    catalog_total = 0

    for doc in boms:
        for line in doc["lines"]:
            bom_cats[line["category"]] += 1
            key = re.sub(r"[^0-9a-z\u4e00-\u9fff]+", "", line["name"].lower())
            if key:
                shared[key].add(doc["robot_id"])
            if line.get("unit_price") is not None:
                catalog_total += 1
                if line.get("catalog_part_id"):
                    catalog_hits += 1

    lines: list[str] = []
    lines.append("# 全开源整机 BOM 分析")
    lines.append("")
    lines.append("由 `tools/analyze_boms.py` 从 `data/boms/*.json` 生成；价格按各机官方 BOM 原币种统计，不换算、不估补。")
    lines.append("")
    lines.append(f"- 方案库全开源整机：{len(full)} 台")
    lines.append(f"- 官方 BOM 已结构化：{len(boms)} 台")
    if provisional:
        lines.append("- 官方 BOM 未发布、仅有器件骨架：" + "、".join(d["robot_name"] for d in provisional))
    missing = [r for r in full if r["id"] not in covered and r["id"] not in provisional_ids]
    if missing:
        lines.append("- 缺 BOM：" + "、".join(f"{r.get('vendor_cn') or r.get('vendor')} {r.get('model')}" for r in missing))
    lines.append("")
    lines.append("## 逐机概览")
    lines.append("")
    lines.append("| 整机 | BOM 行 | 件数 | 已标价合计 | 缺价行 | 站内匹配 |")
    lines.append("| --- | ---: | ---: | ---: | ---: | ---: |")
    for doc in sorted(boms, key=lambda d: d["robot_name"]):
        t = doc["totals"]
        priced = sum(1 for x in doc["lines"] if x.get("unit_price") is not None)
        matched = sum(1 for x in doc["lines"] if x.get("catalog_part_id"))
        share = f"{matched}/{priced}" if priced else "0/0"
        lines.append(
            f"| {doc['robot_name']} | {t.get('line_count', len(doc['lines']))} | {t.get('item_count', 0):g} | "
            f"{money(t.get('priced_subtotal'), doc['currency'])} | {t.get('unpriced_lines', 0)} | {share} |"
        )
    lines.append("")
    lines.append("## BOM 品类分布")
    lines.append("")
    lines.append("| BOM 品类 | 行数 | 站内落点 |")
    lines.append("| --- | ---: | --- |")
    for cat, count in bom_cats.most_common():
        lines.append(f"| `{cat}` | {count} | {BOM_TO_SITE.get(cat, '缺')} |")
    lines.append("")
    lines.append("## 跨机型共用件")
    lines.append("")
    multi = [(k, v) for k, v in shared.items() if len(v) >= 2]
    multi.sort(key=lambda kv: (-len(kv[1]), kv[0]))
    if multi:
        lines.append("| 件（规范化名称） | 使用机型数 | 机型 |")
        lines.append("| --- | ---: | --- |")
        for key, robots in multi[:40]:
            names = ", ".join(sorted(robots))
            lines.append(f"| {key} | {len(robots)} | {names} |")
    else:
        lines.append("暂未发现跨机型完全同名的条目。")
    lines.append("")
    lines.append("## 站内目录覆盖")
    lines.append("")
    pct = (catalog_hits / catalog_total * 100) if catalog_total else 0
    lines.append(f"- 已标价 BOM 行：{catalog_total}；精确匹配到站内部件：{catalog_hits}（{pct:.1f}%）")
    lines.append("- 未匹配的条目按 `data/boms/_discoveries/*.md` 的候选清单处理；只有确认厂商型号与参数后才进目录。")
    lines.append("")
    lines.append("## 发现与缺口")
    lines.append("")
    if missing:
        lines.append("### 缺 BOM 的全开源整机")
        lines.append("")
        for r in missing:
            lines.append(f"- `{r['id']}` {r.get('vendor_cn') or r.get('vendor')} {r.get('model')}")
        lines.append("")
    gap_cats = [c for c in bom_cats if c not in BOM_TO_SITE]
    if gap_cats:
        lines.append("### BOM 惯例品类中站内没有落点的")
        lines.append("")
        lines.append("、".join(f"`{c}`" for c in gap_cats))
        lines.append("")
    lines.append("详细候选见 `data/boms/_discoveries/`。")
    lines.append("")
    if INSIGHTS.exists():
        lines.append("---")
        lines.append("")
        lines.append(INSIGHTS.read_text(encoding="utf-8").strip())
        lines.append("")

    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"写出 {OUT.relative_to(ROOT)}（{len(boms)} 台）")


if __name__ == "__main__":
    main()
