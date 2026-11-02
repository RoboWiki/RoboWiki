"""抓 GitHub Contributors 快照（贡献者页的数据源）。

为什么用快照而不是前端实时请求：
    · 前端调 API 会被限速（匿名 60 次/小时），而且首屏要多等一次网络
    · 快照进 git，谁都能看到「这一版页面基于哪次抓取」
    · 与本站「数据可追溯」的口径一致：页面上的数字有生成时间戳

取法：优先用已登录的 gh CLI（额度高），失败再退回匿名 REST。
拆仓后 GitHub API 只数默认分支，数不到 ccc / ccc_dt 上的工作；
因此再用本地双仓的全分支提交做校正，按作者+时间+标题去重。
"""
from __future__ import annotations

import json
import os
from pathlib import Path
import pathlib
import subprocess
import urllib.request
from datetime import datetime, timezone, timedelta

ROOT = pathlib.Path(__file__).resolve().parents[1]
OWNER, REPO = "RoboWiki", "RoboWiki.github.io"
OUT = ROOT / "data" / "contributors_snapshot.json"
CST = timezone(timedelta(hours=8))


def via_gh() -> list[dict]:
    r = subprocess.run(
        ["gh", "api", f"repos/{OWNER}/{REPO}/contributors?per_page=100"],
        capture_output=True, text=True, encoding="utf-8")
    if r.returncode != 0:
        raise RuntimeError(r.stderr[:200])
    return json.loads(r.stdout)


def via_rest() -> list[dict]:
    req = urllib.request.Request(
        f"https://api.github.com/repos/{OWNER}/{REPO}/contributors?per_page=100",
        headers={"User-Agent": "RoboWiki-build",
                 "Accept": "application/vnd.github+json"})
    with urllib.request.urlopen(req, timeout=25) as resp:
        return json.loads(resp.read().decode())



def _repo_paths() -> list[Path]:
    paths = [ROOT]
    site = os.environ.get("ROBOWIKI_SITE_REPO")
    site_path = Path(site) if site else ROOT.parent / REPO
    if site_path.exists() and (site_path / ".git").exists():
        paths.append(site_path)
    return paths


def local_commit_counts() -> dict[str, dict[str, set[tuple[str, str, str]]]]:
    """按作者名数双仓全分支提交；同一提交在拆分迁移后可能换 SHA，用
    作者邮箱 + 作者时间 + 标题做指纹去重。"""
    out: dict[str, dict[str, set[tuple[str, str, str]]]] = {}
    for repo in _repo_paths():
        try:
            r = subprocess.run(
                ["git", "log", "--all", "--format=%an%x00%ae%x00%at%x00%s"],
                capture_output=True, text=True, encoding="utf-8", cwd=str(repo))
        except Exception:
            continue
        for line in (r.stdout or "").splitlines():
            parts = line.split("\x00")
            if len(parts) != 4:
                continue
            name, email, ts, subject = (x.strip() for x in parts)
            if not name:
                continue
            out.setdefault(name.lower(), {}).setdefault(repo.name, set()).add(
                (email.lower(), ts, subject))
    return out


def _git_stats(counts: dict[str, dict[str, set[tuple[str, str, str]]]],
               login: str) -> tuple[int, dict[str, int]]:
    repos = counts.get(login.lower()) or {}
    unique = len(set().union(*repos.values())) if repos else 0
    return unique, {name: len(fps) for name, fps in repos.items()}


def main() -> None:
    try:
        raw = via_gh()
        src = "GitHub Contributors（gh api）+ 双仓全分支 git 统计"
    except Exception:
        raw = via_rest()
        src = "GitHub Contributors（REST，匿名）+ 双仓全分支 git 统计"

    people = []
    for it in raw:
        if not isinstance(it, dict) or "login" not in it:
            continue
        kind = it.get("type", "User")
        login = str(it["login"])
        # bot 不算贡献者：部署工作流以 github-actions[bot] 身份提交，
        # 但它没有「核了什么」，列上来只会稀释名单
        if kind.lower() != "user" or login.endswith("[bot]"):
            continue
        people.append({
            "login": it["login"],
            "avatar": it.get("avatar_url"),
            "url": it.get("html_url"),
            "contributions": int(it.get("contributions", 0)),
            "bot": kind.lower() != "user",
        })
    people.sort(key=lambda p: p["contributions"], reverse=True)

    # 保留已有的 baseline（初始贡献）与角色，刷新时不覆盖
    old = {}
    if OUT.exists():
        try:
            prev = json.loads(OUT.read_text(encoding="utf-8"))
            old = {(c.get("login") or "").lower(): c for c in prev.get("contributors", [])}
        except Exception:
            old = {}
    git_counts = local_commit_counts()
    for p_ in people:
        p_["api_contributions"] = p_["contributions"]
        g, by_repo = _git_stats(git_counts, p_["login"])
        if g:
            p_["git_commits"] = g
            p_["git_repos"] = by_repo
            p_["contributions"] = max(p_["contributions"], g)
        prev = old.get(p_["login"].lower(), {})
        p_["baseline"] = prev.get("baseline", 0)
        p_["contribution_total"] = p_["baseline"] + p_["contributions"]
        if prev.get("role"):
            p_["role"] = prev["role"]

    # 手工登记过、但 API 里没有的人（例如只在非默认分支提交的）也要保留
    logins = {p_["login"].lower() for p_ in people}
    for low, prev in old.items():
        if low in logins or low.endswith("[bot]"):
            continue
        if low not in logins:
            keep = dict(prev)
            g, by_repo = _git_stats(git_counts, low)
            keep["contributions"] = max(int(keep.get("contributions") or 0), g)
            if g:
                keep["git_commits"] = g
                keep["git_repos"] = by_repo
            keep["contribution_total"] = int(keep.get("baseline") or 0) + keep["contributions"]
            people.append(keep)

    people.sort(key=lambda p: p.get("contribution_total") or p["contributions"], reverse=True)
    total_c = sum(p.get("contribution_total") or p["contributions"] for p in people)
    data = {
        "repo": f"{OWNER}/{REPO}",
        "source": src,
        "updated_at": datetime.now(CST).strftime("%Y-%m-%d %H:%M"),
        "total": len(people),
        "total_contributions": total_c,
        "contributors": people,
    }
    OUT.write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"贡献者 {data['total']} 人 / 累计 {total_c} 次 -> {OUT.name}")


if __name__ == "__main__":
    main()
