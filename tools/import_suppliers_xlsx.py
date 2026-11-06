"""把两份社区 Excel 归一成供应商数据（按分区表头解析，并做脱敏）。

两份表的结构并不一致：
  · 红黑榜：类别 / 店铺 / 掌柜 / 成色 / 主营范围 / 上榜原因 / 链接 / 渠道
  · 供应商名录：同一张 sheet 里按「机械加工 / 标准件 / 电子 / 杂项 / 避雷」
    分了多段，且各段列顺序不同：
      机械加工：商品导向 / 加工质量 / 交货准时性 / 价格 / 发票
      标准件等：商品导向 / 价格 / 发票 / 备注
      避雷：商品导向 / 踩雷点（没有链接）
    旧导入器按固定列号读取，会把「发票」写成「交期」、把「价格」写成「质量」。
    这里按表头识别布局，再逐行归一。

对外数据不包含填写人、掌柜 ID、店铺链接、手机号/QQ/邮箱；只保留
`has_url` 表示「有店可搜」。长备注保留为报告明细，不做原始转发。

输出 `data/suppliers.json`：一家店一条
  {
    id, name, category, services, audiences, best_for, caution,
    listing, grade, channel, signals, quality_raw, punctual_raw, price_raw,
    invoice_raw, notes, reason, reported_at, has_url, tier, origin,
    reports: [{...}], report_count
  }

`audiences` 是检索标签，不是推荐：
  hobbyist   爱好者：小批量、元件、标准件、3D 打印
  competition 竞赛：结构件、急件、钣金/CNC、可开票
  engineering 工程师：精度、工艺能力、稳定交付、可开票
"""
from __future__ import annotations

import collections
import hashlib
import json
import os
import pathlib
import re
from typing import Any, Iterable

from openpyxl import load_workbook

ROOT = pathlib.Path(__file__).resolve().parents[1]
DOWNLOADS = pathlib.Path(os.environ.get("SUPPLIER_XLSX_DIR", pathlib.Path.home() / "Downloads"))
P_LIST = DOWNLOADS / "【红黑榜】电子元件网店红黑榜.xlsx"
P_SUP = DOWNLOADS / "供应 商名录.xlsx"
OUT = ROOT / "data" / "suppliers.json"
ID_MAP_PATH = ROOT / "data" / "_supplier_ids.json"

RE_URL = re.compile(r"https?://\S+")
RE_PHONE = re.compile(r"1[3-9]\d{9}")
RE_QQ = re.compile(r"(?i)(QQ|微信|wechat|vx|v信)\s*[:：]?\s*[\w-]{5,}")
RE_MAIL = re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+")
SCHOOLS = ("哈工大", "哈深", "北理", "深技大", "长春工大", "北工大", "武工大", "昆山",
           "河北轨道", "交大", "华科", "浙大", "电子科大", "西交", "南航", "北航",
           "大连理工", "北信科", "河南科大", "河北科大", "安信工", "大工")
RE_PERSON = re.compile(
    r"(?:" + "|".join(SCHOOLS) + r")[\s　]*[\u4e00-\u9fa5]{2,3}\s*[:：]")

CATEGORY_ALIASES = {
    "机械加工": "机械加工",
    "螺钉": "螺钉紧固",
    "标准件": "标准件",
    "电子": "电子",
    "杂项": "杂项",
    "避雷": "避雷/防护",
    "轴承": "轴承",
}

SERVICE_RULES = [
    ("CNC/车铣", ("cnc", "车铣", "铣床", "车床", "数控", "机加工", "机加")),
    ("钣金/激光", ("钣金", "折弯", "弯折", "激光切", "激光")),
    ("线切割", ("线切割",)),
    ("3D打印", ("3d打印", "3d", "光固化", "sls", "fdm", "打印")),
    ("焊接", ("焊接", "焊")),
    ("表面处理", ("表面处理", "阳极", "氧化", "喷砂", "电镀")),
    ("包胶/轮", ("包胶", "聚氨酯", "轮", "辊")),
    ("PCB/电路板", ("pcb", "电路板", "贴片", "smt", "打板")),
    ("电子元件", ("元件", "ic", "电阻", "电容", "芯片", "单片机", "模块", "端子", "连接器")),
    ("电机/驱动", ("电机", "舵机", "驱动", "电调")),
    ("紧固件", ("螺钉", "螺丝", "螺母", "紧固")),
    ("轴承", ("轴承", "滑轨", "丝杠")),
    ("传感器", ("传感器", "imu", "雷达", "相机")),
    ("工具/仪表", ("工具", "仪表", "万用表", "电源", "焊台", "刀具")),
    ("材料", ("铝", "碳纤维", "碳板", "玻纤", "亚克力", "板材", "管", "棒")),
]

NEGATIVE = ("差", "不行", "不能用", "翻车", "瞎", "拖延", "拖了", "很慢", "坑", "漏",
            "误差", "不推荐", "态度", "不开票", "开裂", "虚标", "假")
POSITIVE = ("稳定", "精度高", "准确", "首选", "很好", "不错", "质量好", "及时",
            "快", "便宜", "性价比", "免费开", "可开")


def scrub(text: Any, limit: int = 700) -> str | None:
    if text is None:
        return None
    t = str(text).strip()
    if not t:
        return None
    t = RE_URL.sub("（链接已隐去）", t)
    t = RE_MAIL.sub("（邮箱已隐去）", t)
    t = RE_PHONE.sub("（电话已隐去）", t)
    t = RE_QQ.sub("（联系方式已隐去）", t)
    t = RE_PERSON.sub("", t)
    t = re.sub(r"[ \t]{2,}", " ", t)
    t = re.sub(r"\n{3,}", "\n\n", t).strip()
    return t[:limit].strip() or None


def sid(name: str) -> str:
    return "sup-" + hashlib.sha1(name.encode("utf-8")).hexdigest()[:8]


_ID_MAP: dict[str, list[str]] = {}
_NEW_IDS: dict[str, list[str]] = {}
if ID_MAP_PATH.exists():
    try:
        _ID_MAP = {k: list(v) for k, v in json.loads(ID_MAP_PATH.read_text(encoding="utf-8")).items()}
    except Exception:
        _ID_MAP = {}


def take_id(name: str, namespace: str) -> str:
    """优先沿用已有 ID；同名多条按出现顺序分配，避免一次重导入把外链全换掉。"""
    ids = _ID_MAP.get(name)
    if ids:
        return ids.pop(0)
    generated = sid(namespace + name)
    _NEW_IDS.setdefault(name, []).append(generated)
    return generated


def month(value: Any) -> str | None:
    m = re.match(r"(\d{4})-(\d{2})", str(value or ""))
    return f"{m.group(1)}-{m.group(2)}" if m else None


def _text(cells: Iterable[Any], start: int = 0) -> str | None:
    parts = [str(c).strip() for c in list(cells)[start:] if c is not None and str(c).strip()]
    return scrub("；".join(parts)) if parts else None


# ── 信号判定 ──────────────────────────────────────────────────────────
def quality_signal(raw: str | None) -> str:
    t = str(raw or "")
    if any(x in t for x in ("差", "不行", "翻车", "不能用", "精度不太", "误差", "瞎")):
        return "bad"
    if any(x in t for x in POSITIVE):
        return "good"
    return "mixed" if t else "unknown"


def punctual_signal(raw: str | None) -> str:
    t = str(raw or "")
    if any(x in t for x in ("催", "拖", "慢", "延期", "不准时")):
        return "slow"
    if any(x in t for x in ("准确", "准时", "及时", "快", "第二天")):
        return "fast"
    return "mixed" if t else "unknown"


def price_signal(raw: str | None) -> str:
    t = str(raw or "")
    if any(x in t for x in ("低", "便宜", "性价比", "最低")):
        return "low"
    if any(x in t for x in ("贵", "偏高", "高")):
        return "high"
    return "mid" if t else "unknown"


def invoice_signal(raw: str | None) -> str:
    t = str(raw or "")
    if any(x in t for x in ("不开", "无票", "税点")):
        return "no" if ("不开" in t or "无票" in t) else "yes"
    if any(x in t for x in ("开票", "发票", "普票", "专票", "税点")):
        return "yes"
    return "no" if t.strip() in ("无", "否") else "unknown"


def services_for(category: str, *texts: str | None) -> list[str]:
    hay = " ".join([category, *[t or "" for t in texts]]).lower()
    out: list[str] = []
    if category == "螺钉紧固":
        out.append("紧固件")
    if category == "轴承":
        out.append("轴承")
    if category == "元件电商":
        out.append("电子元件")
    if category == "避雷/防护":
        out.append("风险记录")
    if "全能" in hay:
        out.extend(["CNC/车铣", "钣金/激光"])
    for label, keys in SERVICE_RULES:
        if label in out:
            continue
        if any(k.lower() in hay for k in keys):
            out.append(label)
    return out[:6] or ["其他"]


def audiences_for(category: str, services: list[str], listing: str | None,
                  signals: dict[str, str]) -> list[str]:
    out: list[str] = []
    if category in ("元件电商", "标准件", "螺钉紧固", "电子", "杂项", "轴承"):
        out.append("hobbyist")
    if any(s in services for s in ("3D打印", "电子元件", "工具/仪表", "材料")):
        out.append("hobbyist")
    if any(s in services for s in ("CNC/车铣", "钣金/激光", "线切割", "3D打印", "PCB/电路板")):
        out.append("competition")
    if any(s in services for s in ("CNC/车铣", "钣金/激光", "线切割", "3D打印",
                                    "PCB/电路板", "表面处理", "焊接")):
        out.append("engineering")
    if listing == "黑榜":
        out = []
    return list(dict.fromkeys(out))


def best_for(audiences: list[str], services: list[str], signals: dict[str, str]) -> str:
    labels = {"hobbyist": "爱好者", "competition": "竞赛", "engineering": "工程"}
    who = " / ".join(labels[a] for a in audiences[:3]) or "谨慎参考"
    what = "、".join(services[:3])
    tail = []
    if signals.get("punctual") == "fast":
        tail.append("交期反馈快")
    if signals.get("invoice") == "yes":
        tail.append("可开票")
    if signals.get("price") == "low":
        tail.append("价格低")
    return f"{who} · {what}" + (f" · {' / '.join(tail)}" if tail else "")


def caution_for(reports: list[dict], listing: str | None) -> str | None:
    if listing == "黑榜":
        text = "；".join(str(r.get("reason") or r.get("notes") or "") for r in reports if r.get("reason") or r.get("notes"))
        return scrub(text, 240) or "社区踩雷记录，下单前务必核对。"
    bad = [str(r.get("notes") or "") for r in reports if any(x in str(r.get("notes") or "") for x in NEGATIVE)]
    return scrub("；".join(dict.fromkeys(bad)), 240) if bad else None


# ── Excel 解析 ────────────────────────────────────────────────────────
def load_listing() -> list[dict]:
    if not P_LIST.exists():
        print(f"! 缺少 {P_LIST}")
        return []
    wb = load_workbook(P_LIST, read_only=True, data_only=True)
    ws = wb.worksheets[0]
    rows = list(ws.iter_rows(values_only=True))[2:]
    out = []
    for r in rows:
        if not r or not r[3]:
            continue
        name = str(r[3]).strip()
        if name in ("店铺完整名(必填)", "") or len(name) < 2:
            continue
        listing = str(r[0] or "").strip()
        if listing not in ("红榜", "黑榜"):
            continue
        fine = scrub(r[7], 80) or "电子元件"
        quality = "good" if listing == "红榜" else "bad"
        out.append({
            "id": take_id(name, "lcb:"),
            "name": name,
            "display_name": scrub(r[4], 40),
            "category": "元件电商",
            "services": services_for("元件电商", fine, str(r[8] or ""), str(r[9] or "")),
            "listing": listing,
            "grade": "全新" if "全新" in str(r[6] or "") else ("拆机" if "拆机" in str(r[6] or "") else None),
            "channel": scrub(r[11], 20),
            "reported_at": month(r[2]),
            "has_url": bool(r[10]),
            "reason": scrub(r[8], 500),
            "notes": scrub(r[9], 500),
            "quality_raw": None, "punctual_raw": None, "price_raw": None, "invoice_raw": None,
            "signals": {"quality": quality, "punctual": "unknown", "price": "unknown", "invoice": "unknown"},
            "tier": "C",
            "origin": "《红黑榜》表：社区匿名填写，已去除填写人、掌柜 ID 与店铺链接",
        })
    wb.close()
    # 同一店铺可能被重复填写多次；保留第一条，避免同一 ID 重复出卡。
    deduped: dict[str, dict] = {}
    for item in out:
        deduped.setdefault(item["name"], item)
    return list(deduped.values())


def load_suppliers() -> list[dict]:
    if not P_SUP.exists():
        print(f"! 缺少 {P_SUP}")
        return []
    wb = load_workbook(P_SUP, data_only=True)
    ws = wb.worksheets[0]
    rows = list(ws.iter_rows(values_only=True))
    out: list[dict] = []
    category = "机械加工"
    layout = "mech"
    skipped = 0
    for r in rows:
        cells = ["" if c is None else str(c).strip() for c in r]
        joined = " ".join(cells)
        if "店铺名" in cells:
            if "交货准时性" in cells:
                layout = "mech"
            elif "踩雷点" in cells:
                layout = "risk"
                category = "避雷/防护"
            else:
                layout = "price"
            continue
        if cells and cells[0] in CATEGORY_ALIASES:
            category = CATEGORY_ALIASES[cells[0]]
        name = cells[1] if len(cells) > 1 else ""
        if not name or name in ("店铺名", "分类"):
            if any(cells[1:]):
                skipped += 1
            continue
        if len(name) < 2:
            continue
        link = cells[2] if len(cells) > 2 else ""
        if layout == "mech":
            orientation, quality, punctual, price, invoice = cells[3], cells[4], cells[5], cells[6], cells[7]
            notes = _text(cells, 8)
        elif layout == "risk":
            orientation, quality, punctual, price, invoice = cells[2], "", "", "", ""
            notes = scrub("；".join(x for x in cells[2:4] if x), 600)
        else:
            orientation, quality, punctual, price, invoice = cells[3], "", "", cells[4], cells[5]
            notes = _text(cells, 6)
        listing = "黑榜" if layout == "risk" or category == "避雷/防护" else None
        sig = {
            "quality": quality_signal(quality or notes),
            "punctual": punctual_signal(punctual),
            "price": price_signal(price),
            "invoice": invoice_signal(invoice),
        }
        services = services_for(category, orientation, notes, quality)
        out.append({
            "id": take_id(name, "sup:"),
            "name": name,
            "display_name": None,
            "category": category,
            "services": services,
            "listing": listing,
            "grade": None,
            "channel": "淘宝" if link else "线下/未知",
            "reported_at": None,
            "has_url": bool(link),
            "reason": notes if listing else None,
            "notes": notes,
            "quality_raw": scrub(quality, 120),
            "punctual_raw": scrub(punctual, 120),
            "price_raw": scrub(price, 80),
            "invoice_raw": scrub(invoice, 80),
            "signals": sig,
            "tier": "B",
            "origin": "《供应商名录》表（社区实战反馈，已去署名与链接）",
        })
    wb.close()
    if skipped:
        print(f"  名录：{skipped} 行有反馈但缺店名，已跳过（无法可靠归属）")
    return out


# ── 归并 ──────────────────────────────────────────────────────────────
def shop_type(category: str, services: list[str], listing: str | None) -> str:
    """把原始分类/能力收敛成用户能直接理解的店铺类型。"""
    if category == "避雷/防护":
        for service, label in (("钣金/激光", "钣金 / 激光切割"), ("CNC/车铣", "CNC / 车铣"),
                               ("电子元件", "电子元件 / 模块"), ("轴承", "轴承 / 传动"),
                               ("3D打印", "3D打印 / 手板")):
            if service in services:
                return label
        return "踩雷记录"
    if category in ("元件电商", "电子"):
        return "电子元件 / 模块"
    if category in ("标准件", "螺钉紧固"):
        if "轴承" in services:
            return "轴承 / 传动"
        if "紧固件" in services:
            return "标准件 / 紧固件"
        return "标准件 / 五金"
    if category == "轴承":
        return "轴承 / 传动"
    if category == "机械加工":
        has_cnc = "CNC/车铣" in services
        has_sheet = "钣金/激光" in services
        if has_cnc and has_sheet:
            return "CNC / 钣金综合"
        if has_sheet:
            return "钣金 / 激光切割"
        if has_cnc:
            return "CNC / 车铣"
        if "3D打印" in services:
            return "3D打印 / 手板"
        if any(x in services for x in ("线切割", "焊接", "表面处理")):
            return "线切割 / 焊接 / 表面处理"
        return "机械加工 / 其他"
    if category == "杂项":
        if "工具/仪表" in services:
            return "工具 / 仪表"
        if "材料" in services:
            return "材料 / 耗材"
        if "包胶/轮" in services:
            return "包胶 / 轮"
        return "杂项 / 耗材"
    return category or "其他"


def finalize(records: list[dict]) -> list[dict]:
    """逐条生成面向决策的派生字段；保留来源行，避免合并时吞掉历史 ID。"""
    out = []
    for r in records:
        services = r.get("services") or services_for(
            r.get("category") or "", r.get("process"), r.get("notes"), r.get("quality_raw"))
        listing = r.get("listing")
        signals = r.get("signals") or {
            "quality": quality_signal(r.get("quality_raw") or r.get("notes")),
            "punctual": punctual_signal(r.get("punctual_raw")),
            "price": price_signal(r.get("price_raw")),
            "invoice": invoice_signal(r.get("invoice_raw")),
        }
        audiences = audiences_for(r.get("category") or "", services, listing, signals)
        report = {
            "listing": listing,
            "grade": r.get("grade"),
            "channel": r.get("channel"),
            "reported_at": r.get("reported_at"),
            "quality_raw": r.get("quality_raw"),
            "punctual_raw": r.get("punctual_raw"),
            "price_raw": r.get("price_raw"),
            "invoice_raw": r.get("invoice_raw"),
            "notes": r.get("notes"),
            "reason": r.get("reason"),
        }
        r.update({
            "shop_type": shop_type(r.get("category") or "", services, listing),
            "services": services or ["其他"],
            "audiences": [] if listing == "黑榜" else audiences,
            "best_for": "" if listing == "黑榜" else best_for(audiences, services, signals),
            "caution": caution_for([report], listing),
            "signals": signals,
            "reports": [report],
            "report_count": 1,
            "notes": scrub(r.get("notes"), 900),
            "reason": scrub(r.get("reason"), 600),
        })
        out.append(r)
    return sorted(out, key=lambda x: (x.get("listing") != "红榜", x.get("listing") != "黑榜",
                                      x.get("category") or "", x["name"]))


def main() -> None:
    listing = load_listing()
    sourced = load_suppliers()
    merged = finalize(listing + sourced)
    OUT.write_text(json.dumps(merged, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"供应商 {len(merged)} 家（红黑榜 {len(listing)} 条 / 名录 {len(sourced)} 条）")
    print("分类：", collections.Counter(x["category"] for x in merged).most_common())
    print("受众：", collections.Counter(a for x in merged for a in x["audiences"]).most_common())
    print("服务：", collections.Counter(s for x in merged for s in x["services"]).most_common(12))
    print("带优惠/发票：", sum(1 for x in merged if x["signals"].get("invoice") == "yes"))
    print("黑榜：", sum(1 for x in merged if x["listing"] == "黑榜"))


if __name__ == "__main__":
    main()
