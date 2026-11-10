# -*- coding: utf-8 -*-
"""导入《RM、RC-供应商名录.xlsx》，按店名合并进 data/suppliers.json。

表结构（两份 sheet）：
  机械加工：店铺 / 链接 / 商品导向 / 加工质量 / 交货准时性 / 发票 / 价格 / 备注
  电控硬件：品类 / 店铺 / 链接 / 发票 / 备注
  踩雷段：  店铺 / 商品导向 / 踩雷点（可多列）

复用 tools/import_suppliers_xlsx.py 的脱敏、信号判定与 shop_type 规则。
只用标准库 + zipfile/XML 读 xlsx（该文件样式 openpyxl 解析会报错）。
"""
from __future__ import annotations

import argparse
import collections
import hashlib
import json
import pathlib
import re
import sys
import zipfile
import xml.etree.ElementTree as ET

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from import_suppliers_xlsx import (  # noqa: E402
    audiences_for, best_for, caution_for, finalize, invoice_signal,
    quality_signal, scrub, services_for, shop_type,
)

SUPPLIERS = ROOT / "data" / "suppliers.json"
ID_MAP = ROOT / "data" / "_supplier_ids.json"
DEFAULT_XLSX = pathlib.Path.home() / "Downloads" / "RM、RC-供应商名录.xlsx"
NS = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"


def read_sheets(path: pathlib.Path) -> dict[str, list[dict[int, str]]]:
    z = zipfile.ZipFile(path)
    shared = [
        "".join(t.text or "" for t in si.iter(NS + "t"))
        for si in ET.fromstring(z.read("xl/sharedStrings.xml")).findall(NS + "si")
    ]

    def col(ref: str) -> int:
        letters = re.match(r"([A-Z]+)", ref).group(1)  # type: ignore[union-attr]
        n = 0
        for ch in letters:
            n = n * 26 + ord(ch) - 64
        return n

    out: dict[str, list[dict[int, str]]] = {}
    for name in ("sheet1.xml", "sheet2.xml"):
        root = ET.fromstring(z.read("xl/worksheets/" + name))
        rows: list[dict[int, str]] = []
        for row in root.findall(".//" + NS + "sheetData/" + NS + "row"):
            vals: dict[int, str] = {}
            for c in row.findall(NS + "c"):
                v = c.find(NS + "v")
                t = c.get("t")
                if v is None:
                    inline = c.find(NS + "is")
                    text = "".join(x.text or "" for x in inline.iter(NS + "t")) if inline is not None else ""
                else:
                    text = shared[int(v.text)] if t == "s" else (v.text or "")
                vals[col(c.get("r", ""))] = text.strip()
            rows.append(vals)
        out[name] = rows
    return out


def clean_name(name: str) -> str:
    name = re.sub(r"\s+", " ", name or "").strip()
    if "同一个公司" in name:
        head = name.split("/")[0].strip()
        return f"{head}（同公司多店）"
    return name[:40]


def sid_for(name: str, used: set[str]) -> str:
    base = "sup-" + hashlib.sha1(("sup:" + name).encode("utf-8")).hexdigest()[:8]
    n, candidate = 1, base
    while candidate in used:
        n += 1
        candidate = "sup-" + hashlib.sha1(f"sup:{name}:{n}".encode("utf-8")).hexdigest()[:8]
    used.add(candidate)
    return candidate


def join_note(*parts: str) -> str:
    seen: list[str] = []
    for part in parts:
        for seg in re.split(r"[；;]", part or ""):
            seg = seg.strip()
            if seg and seg not in seen:
                seen.append(seg)
    return "；".join(seen)


def raw_record(cells: dict[int, str], layout: str, source: str) -> dict | None:
    name = clean_name(cells.get(2 if layout == "ec" else 1, ""))
    if not name or len(name) < 2 or "店铺名" in name or name.startswith("～"):
        return None
    if len(name) > 30 and "（同公司多店）" not in name:
        print("  skip 异常店名:", name[:60])
        return None
    link = cells.get(2, "")
    if layout == "risk":
        orientation = cells.get(2, "")
        notes = join_note(*(cells.get(k, "") for k in range(3, 8)))
        quality = punctual = invoice = price = ""
        positive = any(x in notes for x in ("不错", "很好", "推荐", "公道", "可以试试", "好"))
        negative = any(x in notes for x in ("差", "坑", "拖", "慢", "不", "翻车", "假", "糊", "断", "错", "投诉", "推诿", "异常", "卡", "滑", "没"))
        listing = "红榜" if positive and not negative else "黑榜"
    elif layout == "ec":
        orientation = cells.get(1, "")
        notes = cells.get(5, "")
        link = cells.get(3, "")
        quality = punctual = ""
        invoice = cells.get(4, "")
        price = ""
        listing = None
    else:
        orientation = cells.get(3, "")
        quality = cells.get(4, "")
        punctual = cells.get(5, "")
        invoice = cells.get(6, "")
        price = cells.get(7, "")
        notes = join_note(*(cells.get(k, "") for k in range(8, 10)))
        listing = None
    notes = scrub(notes, 900)
    if invoice and not re.search(r"票|税|开", invoice):
        notes = join_note(notes or "", invoice)
        invoice = ""
    quality = scrub(quality, 120)
    punctual = scrub(punctual, 120)
    price = scrub(price, 80)
    invoice = scrub(invoice, 80)
    category = "元件电商" if layout == "ec" else ("避雷/防护" if layout == "risk" and listing == "黑榜" else "机械加工")
    services = services_for(category, orientation, notes, quality or "")
    if layout != "ec" and not (layout == "risk" and listing == "黑榜"):
        cnc = any(x in services for x in ("CNC/车铣", "钣金/激光", "线切割", "3D打印"))
        if not cnc and any(x in services for x in ("紧固件", "轴承")):
            category = "标准件"
        elif not cnc:
            category = "杂项"
    qtext = " ".join(x for x in (quality, notes) if x)
    signals = {
        "quality": "bad" if listing == "黑榜" else (quality_signal(qtext) if qtext else "unknown"),
        "punctual": "slow" if listing == "黑榜" else ("mixed" if punctual else "unknown"),
        "price": "unknown" if not price else ("low" if any(x in price for x in ("低", "实惠", "便宜")) else ("high" if any(x in price for x in ("高", "贵")) else "mid")),
        "invoice": invoice_signal(invoice),
    }
    return {
        "name": name,
        "display_name": None,
        "category": category,
        "services": services,
        "listing": listing,
        "grade": None,
        "channel": "淘宝" if re.search(r"https?://|tb\.cn|tmall|taobao", link) else "线下/未知",
        "reported_at": None,
        "has_url": bool(re.search(r"https?://|tb\.cn|tmall|taobao", link)),
        "reason": notes if listing == "黑榜" else None,
        "notes": notes,
        "quality_raw": quality,
        "punctual_raw": punctual,
        "price_raw": price,
        "invoice_raw": invoice,
        "signals": signals,
        "tier": "B",
        "origin": source,
    }


def parse_new(path: pathlib.Path) -> list[dict]:
    sheets = read_sheets(path)
    src = "《RM、RC 供应商名录》表（社区实战反馈，已去署名与链接）"
    rows = sheets["sheet1.xml"]
    layout = "mech"
    out: list[dict] = []
    for i, cells in enumerate(rows, 1):
        if i == 1:
            continue
        if cells.get(1) == "店铺名":
            layout = "risk" if cells.get(3) == "踩雷点" else "general"
            continue
        if i > 188:
            layout = "general"
        rec = raw_record(cells, layout, src)
        if rec:
            out.append(rec)
    for cells in sheets["sheet2.xml"][1:]:
        rec = raw_record(cells, "ec", src)
        if rec:
            out.append(rec)
    return out


REPORT_FIELDS = ("listing", "grade", "quality_raw", "punctual_raw",
                 "price_raw", "invoice_raw", "notes", "reason")


def report_empty(report: dict) -> bool:
    return not any(report.get(k) for k in REPORT_FIELDS)


def merge_report(target: dict, incoming: dict) -> None:
    report = incoming.get("reports", [{}])[0]
    existing = target.setdefault("reports", [])
    if not report_empty(report):
        signature = tuple(str(report.get(k) or "") for k in REPORT_FIELDS)
        known = {tuple(str(x.get(k) or "") for k in REPORT_FIELDS) for x in existing}
        if signature not in known:
            existing.append(report)
    target["report_count"] = len(existing)
    for key in ("quality_raw", "punctual_raw", "price_raw", "invoice_raw"):
        if not target.get(key) and incoming.get(key):
            target[key] = incoming[key]
    for key, value in incoming.get("signals", {}).items():
        if target.get("signals", {}).get(key) in (None, "unknown"):
            target.setdefault("signals", {})[key] = value
    if incoming.get("listing") == "黑榜":
        target["listing"] = "黑榜"
        target["audiences"] = []
        target["best_for"] = ""
    target["has_url"] = bool(target.get("has_url") or incoming.get("has_url"))
    target["services"] = list(dict.fromkeys((target.get("services") or []) + (incoming.get("services") or [])))
    target["shop_type"] = shop_type(target.get("category") or "", target["services"], target.get("listing"))
    target["caution"] = caution_for(existing, target.get("listing"))
    if target.get("listing") != "黑榜" and not target.get("best_for"):
        target["audiences"] = audiences_for(target.get("category") or "", target["services"], target.get("listing"), target.get("signals") or {})
        target["best_for"] = best_for(target.get("audiences") or [], target["services"], target.get("signals") or {})



def name_key(name: str) -> str:
    base = re.sub(r"[（(][^）)]*[)）]", "", name or "")
    return re.sub(r"\s+", "", base).strip()


def absorb(target: dict, other: dict) -> None:
    """把同名重复记录合并成一条，报告去重。"""
    reports = target.setdefault("reports", [])
    seen = {tuple(str(r.get(k) or "") for k in REPORT_FIELDS) for r in reports}
    for report in other.get("reports") or []:
        if report_empty(report):
            continue
        sig = tuple(str(report.get(k) or "") for k in REPORT_FIELDS)
        if sig not in seen:
            reports.append(report)
            seen.add(sig)
    target["report_count"] = len(reports)
    for key in ("quality_raw", "punctual_raw", "price_raw", "invoice_raw"):
        if not target.get(key) and other.get(key):
            target[key] = other[key]
    for key, value in (other.get("signals") or {}).items():
        if (target.get("signals") or {}).get(key) in (None, "unknown"):
            target.setdefault("signals", {})[key] = value
    if other.get("listing") == "黑榜" or target.get("listing") == "黑榜":
        target["listing"] = "黑榜"
        target["audiences"] = []
        target["best_for"] = ""
    target["has_url"] = bool(target.get("has_url") or other.get("has_url"))
    target["services"] = list(dict.fromkeys((target.get("services") or []) + (other.get("services") or [])))
    target["shop_type"] = shop_type(target.get("category") or "", target["services"], target.get("listing"))
    target["caution"] = caution_for(reports, target.get("listing"))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("xlsx", nargs="?", default=str(DEFAULT_XLSX))
    ap.add_argument("--write", action="store_true")
    args = ap.parse_args()
    path = pathlib.Path(args.xlsx)
    if not path.exists():
        raise SystemExit(f"找不到 {path}")

    existing = json.loads(SUPPLIERS.read_text(encoding="utf-8"))
    by_name = {row["name"]: row for row in existing}
    used_ids = {row.get("id") for row in existing}
    id_map = json.loads(ID_MAP.read_text(encoding="utf-8")) if ID_MAP.exists() else {}
    new_raw = parse_new(path)
    print("解析记录", len(new_raw), "家；库内", len(existing), "家")

    added, merged, skipped = 0, 0, 0
    for rec in finalize(new_raw):
        name = rec["name"]
        if name in by_name:
            merge_report(by_name[name], rec)
            merged += 1
            continue
        ids = id_map.get(name) or []
        rid = ids[0] if ids else sid_for(name, used_ids)
        rec["id"] = rid
        id_map.setdefault(name, [])
        if rid not in id_map[name]:
            id_map[name].append(rid)
        by_name[name] = rec
        existing.append(rec)
        added += 1

    deduped: dict[str, dict] = {}
    dup = 0
    for row in existing:
        key = name_key(row["name"])
        if key in deduped:
            absorb(deduped[key], row)
            dup += 1
        else:
            deduped[key] = row
    # 空壳短名（只有名字/链接）若是另一家完整店名的子串，并入完整店。
    def empty(row: dict) -> bool:
        return not any(row.get(k) for k in ("quality_raw", "punctual_raw", "price_raw", "invoice_raw", "notes", "reason"))
    keys = list(deduped)
    for short in keys:
        if short not in deduped or not empty(deduped[short]):
            continue
        for long in keys:
            if long == short or long not in deduped:
                continue
            if short and short in long:
                absorb(deduped[long], deduped.pop(short))
                dup += 1
                break
    existing = list(deduped.values())
    for row in existing:
        reports = [r for r in row.get("reports") or [] if not report_empty(r)]
        row["reports"] = reports
        row["report_count"] = len(reports)
        if not reports and not row.get("notes"):
            row.setdefault("signals", {})["quality"] = "unknown"
        row["notes"] = scrub(row.get("notes"), 900)
        row["reason"] = scrub(row.get("reason"), 600)
        for rep in reports:
            rep["notes"] = scrub(rep.get("notes"), 900)
            rep["reason"] = scrub(rep.get("reason"), 600)
    listing_black = sum(1 for x in existing if x.get("listing") == "黑榜")
    print(f"新增 {added} 家 / 合并 {merged} 家 / 去重 {dup} 条 / 黑榜 {listing_black}")
    print("类型:", collections.Counter(x.get("shop_type") for x in existing).most_common(12))
    if args.write:
        SUPPLIERS.write_text(json.dumps(existing, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        ID_MAP.write_text(json.dumps(id_map, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        print("已写回 suppliers.json / _supplier_ids.json")


if __name__ == "__main__":
    main()
