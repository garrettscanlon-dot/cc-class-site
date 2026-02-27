#!/usr/bin/env python3
"""
Pull keyword data from DataForSEO and find low-competition opportunities
for Monday Morning Playbook targeting CS leaders at mid-market B2B SaaS.
"""

import json
import ssl
import sys
from urllib import request, error
from pathlib import Path

try:
    import certifi
    SSL_CONTEXT = ssl.create_default_context(cafile=certifi.where())
except ImportError:
    SSL_CONTEXT = ssl.create_default_context()

API_BASE = "https://api.dataforseo.com"
AUTH = "dHJhdmlzc2VAZ2V0bW9yZXJldmlld3MuY29tOjI0OGUxNDQxMmViNWU5OGI="

COMPETITORS = [
    "gainsight.com",
    "totango.com",
    "churnzero.com",
    "vitally.io",
    "planhat.com",
]

SEED_KEYWORDS = [
    "customer success software",
    "customer success tools",
    "account health scoring",
    "customer success weekly report",
    "churn prediction software",
    "customer success prioritization",
    "cs team productivity tools",
    "customer health score",
    "customer success workflow",
    "account risk management SaaS",
    "customer success automation",
    "customer success platform",
    "csm tools",
    "customer success dashboard",
    "renewal management software",
    "expansion revenue customer success",
    "customer success onboarding",
    "net revenue retention tools",
    "customer churn prevention",
    "customer success reporting",
]


def api_post(endpoint, payload):
    url = f"{API_BASE}{endpoint}"
    data = json.dumps(payload).encode("utf-8")
    req = request.Request(
        url,
        data=data,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Basic {AUTH}",
        },
        method="POST",
    )
    try:
        with request.urlopen(req, timeout=60, context=SSL_CONTEXT) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except error.HTTPError as e:
        body = e.read().decode("utf-8")
        print(f"  API error ({e.code}): {body[:300]}")
        return None
    except error.URLError as e:
        print(f"  Network error: {e.reason}")
        return None


def get_items(result):
    """Extract items from a DataForSEO response."""
    if not result or result.get("status_code") != 20000:
        return []
    tasks = result.get("tasks", [])
    if not tasks:
        return []
    task_result = tasks[0].get("result") or []
    if not task_result:
        return []
    return task_result[0].get("items") or []


def parse_keyword_item(item):
    """Parse a keyword item — handles both top-level and nested formats."""
    kw = item.get("keyword", "")
    info = item.get("keyword_info") or {}
    serp = item.get("serp_info") or {}
    volume = info.get("search_volume") or 0
    return {
        "keyword": kw,
        "volume": volume,
        "cpc": info.get("cpc") or 0,
        "competition": info.get("competition") or 0,
        "competition_level": info.get("competition_level") or "",
        "serp_difficulty": serp.get("se_results_count") or 0,
    }


def get_keyword_suggestions(seeds):
    """Get keyword suggestions with volume and competition data."""
    print(f"Fetching keyword suggestions for {len(seeds)} seed keywords...")
    all_keywords = {}

    for seed in seeds:
        payload = [
            {
                "keyword": seed,
                "location_code": 2840,  # US
                "language_code": "en",
                "include_seed_keyword": True,
                "limit": 50,
            }
        ]
        result = api_post(
            "/v3/dataforseo_labs/google/keyword_suggestions/live", payload
        )
        items = get_items(result)
        added = 0
        for item in items:
            parsed = parse_keyword_item(item)
            kw = parsed["keyword"]
            if kw and parsed["volume"] > 0 and kw not in all_keywords:
                parsed["seed"] = seed
                all_keywords[kw] = parsed
                added += 1
        print(f"  '{seed}' -> {len(items)} results, {added} new keywords")

    print(f"Total unique keywords: {len(all_keywords)}")
    return all_keywords


def get_competitor_keywords():
    """Get keywords that competitors rank for."""
    print("\nFetching competitor keyword data...")
    comp_keywords = {}

    for comp in COMPETITORS:
        payload = [
            {
                "target": comp,
                "location_code": 2840,
                "language_code": "en",
                "limit": 100,
                "order_by": ["keyword_info.search_volume,desc"],
            }
        ]
        result = api_post(
            "/v3/dataforseo_labs/google/keywords_for_site/live", payload
        )
        items = get_items(result)
        count = 0
        for item in items:
            parsed = parse_keyword_item(item)
            kw = parsed["keyword"]
            if kw:
                if kw not in comp_keywords:
                    comp_keywords[kw] = {
                        **parsed,
                        "ranked_by": [],
                    }
                comp_keywords[kw]["ranked_by"].append(comp)
                count += 1
        print(f"  {comp}: {count} keywords")

    return comp_keywords


def score_opportunity(kw_data, comp_keywords):
    """Score keyword opportunity: higher = better bang for buck."""
    kw = kw_data["keyword"]
    volume = kw_data.get("volume", 0)
    competition = kw_data.get("competition", 0)

    # Penalize if many competitors already rank for it
    comp_count = 0
    comp_list = []
    if kw in comp_keywords:
        comp_list = comp_keywords[kw].get("ranked_by", [])
        comp_count = len(comp_list)

    # Score: volume * (1 - competition) * competitor_penalty
    competitor_penalty = max(0.1, 1 - (comp_count * 0.25))
    score = volume * (1 - min(competition, 0.95)) * competitor_penalty

    return {
        **kw_data,
        "competitor_count": comp_count,
        "competitors_ranking": comp_list,
        "opportunity_score": round(score, 1),
    }


def main():
    # Step 1: Get keyword suggestions
    suggestions = get_keyword_suggestions(SEED_KEYWORDS)

    # Step 2: Get competitor keyword landscape
    comp_keywords = get_competitor_keywords()

    # Step 3: Score all keywords
    print("\nScoring keyword opportunities...")
    scored = []
    for kw, data in suggestions.items():
        scored.append(score_opportunity(data, comp_keywords))

    # Sort by opportunity score
    scored.sort(key=lambda x: x["opportunity_score"], reverse=True)

    # Save raw data
    output_path = Path(__file__).resolve().parent.parent / "keywords-raw.json"
    with open(output_path, "w") as f:
        json.dump(scored, f, indent=2)
    print(f"\nRaw data saved to {output_path}")

    # Print top results
    print(f"\n{'='*80}")
    print(f"TOP 30 KEYWORD OPPORTUNITIES")
    print(f"{'='*80}")
    for i, kw in enumerate(scored[:30], 1):
        comps = ", ".join(kw["competitors_ranking"]) if kw["competitors_ranking"] else "none"
        print(
            f"{i:2}. {kw['keyword']:<50} vol={kw['volume']:>6} "
            f"comp={kw['competition']:.2f} score={kw['opportunity_score']:>8.1f} "
            f"rivals=[{comps}]"
        )

    return scored


if __name__ == "__main__":
    scored = main()
