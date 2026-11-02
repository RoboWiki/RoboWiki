"""核心仓路径的唯一入口。

data/、schema/、assets/ 都在本仓；下游前端通过环境变量指向解压后的
数据发布物（见 docs/DATA-VERSIONING.md）。

只改这里，不在各脚本里散落 os.environ。
"""
from __future__ import annotations

import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _resolve(env_name: str, default: Path) -> Path:
    raw = os.environ.get(env_name)
    path = Path(raw) if raw else default
    if not path.is_absolute():
        path = ROOT / path
    return path.resolve()


DATA_DIR = _resolve("ROBOWIKI_DATA_DIR", ROOT / "data")
SCHEMA_DIR = _resolve("ROBOWIKI_SCHEMA_DIR", ROOT / "schema")
ASSETS_DIR = _resolve("ROBOWIKI_ASSETS_DIR", ROOT / "assets" / "parts")
