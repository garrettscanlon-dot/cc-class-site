# PRD — Monday Morning Playbook Landing Page

## Overview
A marketing landing page for **Monday Morning Playbook**, a customer success tool that gives CS teams a single, ready-to-act briefing every Monday morning. The landing page targets VP/Director-level CS buyers at mid-market B2B SaaS companies who are evaluating alternatives to bloated CS platforms.

---

## Problem Statement
CS leaders know their teams waste the first hour of every Monday assembling data from scattered tools before they can prioritize their week. The landing page must immediately validate this pain point and position Monday Morning Playbook as the fastest path from "data chaos" to "clear weekly priorities."

---

## Goals & Success Metrics

| Goal | Metric | Target |
|------|--------|--------|
| Drive trial signups | Visitor-to-signup conversion rate | 4–6% |
| Communicate value proposition | Time to understand core value (scroll depth / bounce rate) | < 30% bounce |
| Build credibility | Demo requests from qualified leads | 20+ per month |
| SEO / organic traffic | Organic visits from CS-related queries | 500+ monthly within 6 months |

---

## Page Structure & Sections

### 1. Hero
- Headline that names the pain ("Stop wasting Monday mornings pulling data")
- Subheadline with the value prop (weekly digest, prioritized actions, one view)
- Primary CTA: "Start Free Trial"
- Secondary CTA: "See a Demo"
- Hero visual: product screenshot showing the weekly digest UI (priority queue, account health, portfolio stats)

### 2. Pain / Problem Section
- 3 pain point cards validating the buyer's frustrations:
  - "Account health signals scattered across 5+ tools"
  - "Risk assessment is vibes-based, not data-driven"
  - "Churn signals get buried in the week's noise"

### 3. Product Overview / How It Works
- 3-step flow:
  1. **Connect** — OAuth integrations with Looker, Salesforce, Linear, Gong, Slack
  2. **Get your briefing** — Auto-generated Monday digest with prioritized accounts
  3. **Take action** — Smart-ranked priority queue with recommended next steps
- Each step shows a simplified product screenshot or illustration

### 4. Key Features
Feature cards covering core capabilities:
- **Weekly Account Digest** — Auto-generated every Monday at 7 AM
- **Account Health Scoring** — Red / Yellow / Green, signal-driven, consistent across the team
- **Priority Queue** — Smart-ranked actions: renewals, churn risks, expansion signals
- **Slack Digest Draft** — Auto-drafted weekly team update, ready to review and post
- **Integration Hub** — Looker, Salesforce, Linear, Gong, Slack — connected in minutes

### 5. Social Proof
- 2–3 customer quotes from CS leaders
- Logo bar of customer companies
- Key stat callouts ("Teams save 45+ minutes every Monday", "80% of at-risk accounts caught before churn")

### 6. Pricing (or CTA)
- Simple pricing display or "Talk to Sales" CTA
- Emphasis on fast time-to-value and no long implementation

### 7. Footer
- Navigation links, company info, legal
- Secondary CTA: "Start Free Trial"

---

## Technical Requirements
- Single-page static HTML (same architecture as current site)
- Responsive design (mobile + desktop)
- All CSS inline in `<style>` block (no external dependencies)
- Vanilla JS only (no frameworks)
- Smooth scroll navigation from header links to page sections
- Accessible: semantic HTML, sufficient contrast, keyboard-navigable CTAs

---

## Design Direction
- Clean, modern SaaS aesthetic (not enterprise-heavy)
- Same color system as the product UI (blue primary, red/yellow/green for health signals)
- Plenty of whitespace; scannable sections
- Product screenshots or simplified UI mockups as visuals

---

## Out of Scope (v1)
- Blog or content pages
- Actual payment processing
- Backend or authentication
- Multi-page navigation

---

## Decisions Log

| # | Question | Decision |
|---|----------|----------|
| 1 | Single page or multi-page? | Single page — matches current architecture |
| 2 | Pricing on page? | Show simple tiers or defer to "Talk to Sales" CTA |
| 3 | Product screenshots | Use simplified UI mockups inline (no external images) |

---

## Open Questions
*None — all questions resolved.*
