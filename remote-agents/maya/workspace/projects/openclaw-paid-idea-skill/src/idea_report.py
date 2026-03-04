#!/usr/bin/env python3
"""
OpenClaw Paid Idea Skill - MVP
生成可收费的每日开发方向候选（基于 Hacker News 热门项目）
"""

from __future__ import annotations

import argparse
import json
import sys
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Dict

HN_TOP_URL = "https://hacker-news.firebaseio.com/v0/topstories.json"
HN_ITEM_URL = "https://hacker-news.firebaseio.com/v0/item/{id}.json"
SAMPLE_PATH = Path(__file__).resolve().parent.parent / "examples" / "stories_sample.json"

MONETIZATION_KEYWORDS = {
    "api": 3,
    "automation": 4,
    "workflow": 4,
    "saas": 5,
    "developer": 3,
    "open source": 2,
    "security": 3,
    "productivity": 4,
    "ai": 4,
    "agent": 4,
    "subscription": 5,
}


@dataclass
class Story:
    id: int
    title: str
    url: str
    score: int
    by: str



def fetch_json(url: str):
    with urllib.request.urlopen(url, timeout=12) as resp:
        return json.loads(resp.read().decode("utf-8"))



def monetization_score(title: str) -> int:
    t = title.lower()
    score = 0
    for kw, weight in MONETIZATION_KEYWORDS.items():
        if kw in t:
            score += weight
    return score



def fetch_top_stories(limit: int, offline: bool = False) -> List[Story]:
    if offline:
        return load_sample_stories(limit)

    ids = fetch_json(HN_TOP_URL)[: limit * 3]
    stories: List[Story] = []
    for sid in ids:
        raw = fetch_json(HN_ITEM_URL.format(id=sid))
        if not raw or raw.get("type") != "story" or "title" not in raw:
            continue
        stories.append(
            Story(
                id=raw["id"],
                title=raw["title"],
                url=raw.get("url", f"https://news.ycombinator.com/item?id={raw['id']}"),
                score=int(raw.get("score", 0)),
                by=raw.get("by", "unknown"),
            )
        )
        if len(stories) >= limit:
            break
    return stories



def load_sample_stories(limit: int) -> List[Story]:
    if not SAMPLE_PATH.exists():
        raise FileNotFoundError(f"sample file not found: {SAMPLE_PATH}")
    raw_items = json.loads(SAMPLE_PATH.read_text(encoding="utf-8"))
    stories = [
        Story(
            id=int(item["id"]),
            title=item["title"],
            url=item.get("url", f"https://news.ycombinator.com/item?id={item['id']}"),
            score=int(item.get("score", 0)),
            by=item.get("by", "sample"),
        )
        for item in raw_items
    ]
    return stories[:limit]



def rank_ideas(stories: List[Story], top_n: int) -> List[Dict]:
    ranked = []
    for s in stories:
        m_score = monetization_score(s.title)
        total = s.score + m_score * 10
        ranked.append(
            {
                "id": s.id,
                "title": s.title,
                "url": s.url,
                "hn_score": s.score,
                "monetization_score": m_score,
                "total_score": total,
                "builder_angle": suggest_builder_angle(s.title),
            }
        )
    ranked.sort(key=lambda x: x["total_score"], reverse=True)
    return ranked[:top_n]



def suggest_builder_angle(title: str) -> str:
    t = title.lower()
    if "api" in t:
        return "做成API监控/调用分析工具，按团队席位收费"
    if "security" in t:
        return "做成安全巡检自动化，按主机数收费"
    if "workflow" in t or "automation" in t:
        return "做成自动化模板市场，按模板包月收费"
    if "developer" in t or "open source" in t:
        return "做成开发者增效插件，按高级功能订阅收费"
    if "ai" in t or "agent" in t:
        return "做成垂直Agent工作流，按任务次数收费"
    return "做成细分场景SaaS工具，优先验证高频痛点"



def render_markdown(ideas: List[Dict]) -> str:
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines = [
        f"# OpenClaw 每日可收费开发方向报告 ({ts})",
        "",
        "以下候选用于选择今天的MVP切片（优先可在24小时内上线验证）:",
        "",
    ]
    for idx, idea in enumerate(ideas, 1):
        lines.extend(
            [
                f"## {idx}. {idea['title']}",
                f"- 综合评分: {idea['total_score']} (HN: {idea['hn_score']} + 变现匹配: {idea['monetization_score']})",
                f"- 链接: {idea['url']}",
                f"- 建议切入: {idea['builder_angle']}",
                "",
            ]
        )
    return "\n".join(lines)



def main() -> int:
    parser = argparse.ArgumentParser(description="Generate OpenClaw paid idea report")
    parser.add_argument("--fetch-limit", type=int, default=15, help="how many HN stories to pull")
    parser.add_argument("--top", type=int, default=5, help="how many ideas to keep")
    parser.add_argument("--json", action="store_true", help="output JSON instead of markdown")
    parser.add_argument("--offline", action="store_true", help="use local sample data")
    args = parser.parse_args()

    try:
        stories = fetch_top_stories(limit=args.fetch_limit, offline=args.offline)
        ideas = rank_ideas(stories, top_n=args.top)
    except Exception as e:
        if not args.offline:
            try:
                stories = fetch_top_stories(limit=args.fetch_limit, offline=True)
                ideas = rank_ideas(stories, top_n=args.top)
                print(f"WARN: online fetch failed, fallback to offline sample: {e}", file=sys.stderr)
            except Exception as e2:
                print(f"ERROR: failed to build report: {e}; fallback failed: {e2}", file=sys.stderr)
                return 1
        else:
            print(f"ERROR: failed to build report: {e}", file=sys.stderr)
            return 1

    if args.json:
        print(json.dumps(ideas, ensure_ascii=False, indent=2))
    else:
        print(render_markdown(ideas))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
