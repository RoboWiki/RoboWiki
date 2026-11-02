"""核心仓唯一命令入口。

    python -m pipeline validate   数据闸门（CI 默认）
    python -m pipeline all        validate（核心仓没有站点构建）
"""
from __future__ import annotations

import os
import subprocess
import sys

_ENV = {**os.environ, "PYTHONIOENCODING": "utf-8", "PYTHONUTF8": "1"}

STEPS = {
    "validate": ["validate"],
    "all": ["validate"],
}


def _run(module: str) -> int:
    print(f"\n=== {module} ===", flush=True)
    return subprocess.call([sys.executable, "-m", f"pipeline.{module}"], env=_ENV)


def main() -> int:
    args = sys.argv[1:] or ["all"]
    if args[0] in ("-h", "--help", "help"):
        print(__doc__)
        print("可用步骤：" + " / ".join(STEPS))
        return 0
    step = args[0]
    if step not in STEPS:
        print(f"未知步骤 {step!r}，可用：{', '.join(STEPS)}")
        return 2
    for name in STEPS[step]:
        rc = _run(name)
        if rc != 0:
            print(f"\n{name} 失败（退出码 {rc}）")
            return rc
    print("\n完成")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
