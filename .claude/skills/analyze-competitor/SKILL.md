---
name: analyze-competitor
description: "Perform a structured competitive analysis on any company or product. Use this skill when the user wants to analyze a competitor, compare against a rival, research a competing product, do competitive intelligence, or build a competitive brief. Triggers on company names, product URLs, or phrases like 'analyze competitor', 'competitive analysis', 'how do we compare to X', 'research X as a competitor', or 'what are X's strengths and weaknesses'. Also use when the user asks to update or add to an existing competitors summary."
---

Research a competitor and produce a structured competitive brief as a markdown file. The analysis compares the competitor against the user's own product, which is defined by files in the repo (persona.md, prd.md, CLAUDE.md).

## Input

The user provides a company name, product name, or URL. Examples:

- `/analyze-competitor Gainsight`
- `/analyze-competitor https://www.hubspot.com`
- `analyze Intercom as a competitor`

Extract the company/product name from whatever the user gives you. If they give a URL, use it directly. If they give a name, construct the likely homepage URL (e.g., `https://www.{name}.com`).

## Step 1: Understand Your Own Product

Before researching the competitor, read the repo's product context files to understand what you're comparing against. These files define the target buyer, pain points, value proposition, and positioning:

- `persona.md` — buyer persona, goals, pain points, buying criteria
- `prd.md` — product requirements, features, positioning
- `CLAUDE.md` — project overview and goals

Read all three. Extract:
- **Your product name and one-line description**
- **Target buyer** (title, company size, industry)
- **Core value proposition** (the main thing your product does better)
- **Key differentiators** (speed, simplicity, pricing, workflow, etc.)
- **Named competitors** (any rivals explicitly called out)

This context shapes every section of the competitive brief. The strengths, weaknesses, and messaging gaps are all *relative to your product* — not absolute judgments.

## Step 2: Research the Competitor

Run three parallel research tracks. Use WebFetch and WebSearch together — websites often don't render fully, so search results fill the gaps.

### Track A: Website Intelligence
Fetch the competitor's homepage and extract:
- Tagline / hero headline
- How they describe themselves (positioning statement)
- Key features listed
- Target audience signals (who the site speaks to)
- Integration mentions
- Any pricing visible on the homepage

If the homepage fetch is thin (heavy JS rendering), also try `/pricing`, `/features`, or `/product` pages.

### Track B: Pricing Research
Search the web for `"{company name}" pricing plans cost {current year}`. Look for:
- Published tier names and prices
- Per-seat vs. per-customer vs. flat-rate model
- Entry-level price point
- Enterprise pricing signals (custom quotes, "talk to sales")
- Third-party pricing data (Vendr, G2, Capterra, GetApp)

### Track C: Strengths & Weaknesses
Search for `"{company name}" reviews pros cons strengths weaknesses {current year}`. Look for:
- Implementation time (how long to get started)
- Common complaints from users
- What users love most
- Comparison articles against similar products
- Analyst recognition (Gartner, Forrester, G2 Leader status)

Run all three tracks in parallel to save time.

## Step 3: Write the Competitive Brief

Create the output file at `competitors/{company-name}.md` (lowercase, hyphenated). Create the `competitors/` directory if it doesn't exist.

Use this exact structure:

```markdown
# Competitor Brief — {Company Name}

> **Date:** {YYYY-MM-DD}
> **Website:** {URL}
> **Analyzed relative to:** {Your Product Name}

---

## Positioning

{Their tagline in quotes.} {1-2 sentences describing how they position themselves — what category they claim, what buyer they target, what transformation they promise.}

## Pricing

- **Model:** {per-seat / per-customer / flat-rate / custom quote}
- **Entry price:** {lowest published price or estimate}
- **Mid-tier:** {if available}
- **Enterprise:** {if available}
- **Free trial/plan:** {yes/no, details}
- **Source:** {where the pricing data came from}

{1-2 sentences of pricing commentary — how it compares to your product's approach.}

## Key Features

- {Feature 1}
- {Feature 2}
- {Feature 3}
- {etc.}

## Strengths (relative to {Your Product Name})

- {Strength 1 — what they do better or have that you don't}
- {Strength 2}
- {Strength 3}

## Weaknesses (relative to {Your Product Name})

- {Weakness 1 — where your product wins}
- {Weakness 2}
- {Weakness 3}

## Messaging Gaps to Exploit

{These are specific holes in the competitor's messaging that your product can own. Not generic weaknesses — specific things they fail to say, claim, or address that matter to your buyer.}

- {Gap 1}
- {Gap 2}
- {Gap 3}

## Sources

- [{Source title}]({URL})
- [{Source title}]({URL})
```

## Quality Standards

The brief should be useful to a product marketer or founder making positioning decisions. That means:

- **Be specific, not generic.** "Their implementation takes 6-8 weeks" beats "They have a longer setup process." Include numbers, quotes from reviews, and concrete details wherever possible.
- **Relative, not absolute.** Every strength and weakness is framed relative to your product. "Stronger Salesforce integration than us" not just "Strong Salesforce integration."
- **Messaging gaps are actionable.** Each gap should suggest a specific claim or angle your product can own. "They never mention time-to-value in their hero copy — we should lead with 'results in week one'" is useful. "They could improve their messaging" is not.
- **Cite your sources.** Every claim should trace back to a URL in the Sources section. Include all URLs used during research — the competitor's site, review sites, pricing aggregators, comparison articles.
- **Keep it scannable.** Bullet points over paragraphs. The reader should get the key insights in 60 seconds.

## After Writing

Tell the user where the file was saved and give a 3-4 bullet summary of the most important findings — the things that would change how they position or sell against this competitor.
