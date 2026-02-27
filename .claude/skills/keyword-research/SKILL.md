---
name: keyword-research
description: "Pull keyword data from DataForSEO and find low-competition, high-relevance keyword opportunities for SEO and content marketing. Use this skill when the user wants keyword research, SEO keyword analysis, content keyword ideas, keyword opportunities, search volume data, or competitive keyword gaps. Also triggers on phrases like 'find keywords', 'what should I rank for', 'SEO opportunities', 'keyword data for', 'content marketing keywords', or 'pull keyword data'. Use this even if the user doesn't mention DataForSEO by name — it's the underlying data source."
---

Research keywords using the DataForSEO API and produce a prioritized keyword report as a markdown file. The analysis scores keywords by opportunity (volume vs. competition) and groups them into actionable tiers relative to the user's product and competitors.

## Input

The user may provide:
- A product or topic to research keywords for (e.g., "find keywords for our CS product", "keyword research for project management tools")
- Specific competitor domains to exclude or check against
- Seed keywords or themes to focus on
- A target persona or audience

If the user doesn't specify all of these, infer what you can from the repo's product context files (`persona.md`, `prd.md`, `CLAUDE.md`). Ask the user to fill critical gaps — at minimum you need a topic/product area and ideally a target buyer.

## Step 1: Understand the Product and Audience

Read available context files in the repo:
- `persona.md` — buyer persona, pain points, goals
- `prd.md` — product features, positioning, value props
- `CLAUDE.md` — project overview
- `competitors-summary.md` — existing competitor analysis (if available)

Extract:
- **Product name and category** (what space are we in?)
- **Target buyer** (title, company type — this shapes keyword intent)
- **Core pain points** (these become seed keyword themes)
- **Key differentiators** (these inform which keywords align best)
- **Known competitors** (domains to cross-reference)

## Step 2: Generate Seed Keywords

Based on the product context, create 15–25 seed keywords across these intent categories:

1. **Problem-aware** — keywords describing the pain the product solves (e.g., "customer churn prevention", "account health scoring")
2. **Solution-aware** — keywords describing the category of tool (e.g., "customer success software", "CS platform")
3. **Comparison/evaluation** — keywords from buyers actively comparing options (e.g., "best customer success tools", "gainsight alternatives")
4. **Feature-specific** — keywords matching specific product features (e.g., "renewal management software", "customer health score")
5. **Workflow/process** — keywords about the process the product improves (e.g., "customer success weekly report", "CS team workflow")

Aim for a mix: some broad (higher volume), some specific (lower competition). The goal is to cast a wide net, then filter.

## Step 3: Pull Data from DataForSEO

The user must have a DataForSEO API key. Check for it in:
1. `.env` file — look for `DATAFORSEO_API_KEY` (base64-encoded credentials)
2. Ask the user if not found

The DataForSEO API uses Basic auth with base64-encoded `login:password` credentials. The key in `.env` should already be base64-encoded.

### API Calls to Make

Use Python with `urllib` (no pip dependencies needed) to call the DataForSEO API. Handle SSL via `certifi` if available, fall back to default context.

**API base:** `https://api.dataforseo.com`
**Auth header:** `Authorization: Basic {base64_key}`

#### A. Keyword Suggestions (primary data source)

For each seed keyword, call:
```
POST /v3/dataforseo_labs/google/keyword_suggestions/live
```

Payload:
```json
[{
  "keyword": "seed keyword here",
  "location_code": 2840,
  "language_code": "en",
  "include_seed_keyword": true,
  "limit": 50
}]
```

Response parsing — items are at the top level of each result item:
```python
item["keyword"]                              # the keyword string
item["keyword_info"]["search_volume"]        # monthly volume
item["keyword_info"]["cpc"]                  # cost per click (can be null)
item["keyword_info"]["competition"]          # 0-1 Google Ads competition
item["keyword_info"]["competition_level"]    # LOW/MEDIUM/HIGH
item["serp_info"]                            # may be null — always use `or {}`
```

**Important:** The API may return `null` for nested objects like `keyword_info`, `serp_info`, etc. Always use `item.get("keyword_info") or {}` pattern, never `item.get("keyword_info", {})` since the key may exist with a `None` value.

#### B. Competitor Keywords (cross-reference)

For each competitor domain, call:
```
POST /v3/dataforseo_labs/google/keywords_for_site/live
```

Payload:
```json
[{
  "target": "competitor.com",
  "location_code": 2840,
  "language_code": "en",
  "limit": 100,
  "order_by": ["keyword_info.search_volume,desc"]
}]
```

Same response structure as above. Note: this endpoint returns broad keywords the domain has *any* presence for, including very generic terms. Filter to only CS/product-relevant keywords when cross-referencing.

#### Response Parsing Helper

All DataForSEO responses follow this structure:
```python
result["tasks"][0]["result"][0]["items"]  # list of keyword items
```

But any level can be null/empty, so always guard:
```python
def get_items(result):
    if not result or result.get("status_code") != 20000:
        return []
    tasks = result.get("tasks", [])
    if not tasks:
        return []
    task_result = tasks[0].get("result") or []
    if not task_result:
        return []
    return task_result[0].get("items") or []
```

Run seed keyword suggestions and competitor lookups in sequence (not parallel) to avoid rate limits.

## Step 4: Score and Categorize Keywords

### Opportunity Score

Calculate: `volume × (1 - competition) × competitor_penalty`

- `competition` is the Google Ads competition index (0–1)
- `competitor_penalty`: if N of the known competitors rank for this keyword, apply `max(0.1, 1 - N × 0.25)` — so 4+ competitors ranking = 90% penalty

### Categorize by Theme

Group keywords into themes aligned with the product's value proposition. The themes should emerge from the product context — not be hardcoded. Common patterns:

- **Core problem keywords** — the pain point the product solves
- **Product category keywords** — what the tool "is"
- **Feature-specific keywords** — individual capabilities
- **Process/workflow keywords** — the job the buyer is trying to do
- **Competitor/comparison keywords** — evaluation-stage queries

### Priority Tiers

- **Tier 1 — Own Now:** Low competition (< 0.25), high relevance, volume ≥ 40. Create dedicated pages.
- **Tier 2 — Content Targets:** Medium competition (0.10–0.50), good volume. Write blog posts and guides.
- **Tier 3 — Long-term SEO:** High volume but high CPC/competition. Earn with organic content over time; don't buy ads.

## Step 5: Write the Report

Save to `keywords.md` in the project root (or a user-specified path).

Use this structure:

```markdown
# Keyword Research — {Product Name}

> **Date:** {YYYY-MM-DD}
> **Source:** DataForSEO (Google Ads data, US market)
> **Seed keywords:** {count} | **Total keywords analyzed:** {count}
> **Competitors analyzed:** {list}

---

## How to Read This Report

- **Volume:** Monthly US search volume
- **Competition:** Google Ads competition index (0–1). Lower = easier
- **CPC:** Cost-per-click for Google Ads. High = strong commercial intent
- **Opportunity Score:** `volume × (1 - competition)`. Higher = better bang for buck

---

## Priority Tiers

### Tier 1 — Own These Now
{table of low-competition, high-relevance keywords}

### Tier 2 — Content Marketing Targets
{table of medium-competition keywords}

### Tier 3 — Long-Term SEO Targets
{table of high-value head terms}

---

## Detailed Breakdown by Theme

### {Theme 1} ({count} keywords)
{Why this theme matters for the product}
{table}

### {Theme 2} ...

---

## Recommended Actions

{3-5 specific, actionable recommendations based on the data}

---

## Key Takeaways

{3-5 bullet summary of the most important findings}
```

### Table Format

```markdown
| Keyword | Volume | Competition | CPC | Score |
|---------|-------:|:-----------:|----:|------:|
| example keyword | 260 | 0.44 (MEDIUM) | $13.97 | 145.6 |
```

## Quality Standards

- **Relevance filter:** Every keyword in the report should be something the target persona would plausibly search. Generic terms ("software", "tools") that happen to have high volume but no product relevance should be excluded.
- **Actionable recommendations:** Each recommended action should name the specific keyword, its metrics, and the specific content to create. "Write a blog post about X" beats "target long-tail keywords."
- **Honest about limitations:** If a keyword category has near-zero search volume, say so — don't hype it. But explain whether that's a risk or an opportunity (category creation).
- **CPC context:** High CPC means commercial intent (buyers, not browsers). Note when a low-volume keyword has high CPC — that's a valuable signal.

## After Writing

Tell the user where the file was saved and give a 3–5 bullet summary of the top findings — the keywords they should act on first and why. Also save the raw scored data as `keywords-raw.json` for future reference.
