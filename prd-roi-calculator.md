# PRD — ROI Calculator Section

## Overview
An interactive ROI calculator embedded in the Monday Morning Playbook landing page that lets CS leaders (the buyer persona) quantify the time, revenue, and cost savings their team would realize by adopting the product. The calculator uses live sliders/inputs with real-time output — no form submission, no email gate.

---

## Problem It Solves (for the Buyer)
Alex Rivera (VP of CS) needs to justify the purchase to the CFO. "It saves time" isn't enough — they need dollar amounts. The calculator translates the persona's specific pain points into concrete financial outcomes:
- Time wasted assembling data every Monday → hours and salary dollars recovered
- At-risk accounts caught too late → churn revenue prevented
- Expansion signals buried → additional pipeline surfaced

---

## Placement
New section on the existing landing page, inserted between **Social Proof** and the **CTA section**.

---

## Inputs (User-Adjustable via Sliders)

| Input | Default | Range | Rationale |
|-------|---------|-------|-----------|
| Number of CSMs | 8 | 1–50 | Team size drives all time-savings math |
| Avg. fully-loaded CSM salary | $95,000 | $50K–$200K | Converts time saved into dollar value |
| Hours spent on Monday data assembly (per CSM) | 1.0 | 0.5–3.0 (0.25 steps) | The core pain point from the persona |
| Total portfolio MRR managed by team | $400K | $50K–$10M | Basis for churn and expansion calculations |
| Annual gross churn rate | 12% | 2%–30% | Needed to calculate churn prevention value |
| Monday Morning Playbook annual cost | $12,000 | Fixed / editable | Allows buyer to see net ROI; transparent pricing |

---

## Outputs (Real-Time, Ungated)

### Primary Output
- **Net Annual ROI** — total savings minus product cost, displayed as a large headline number
- **ROI multiple** — e.g., "7.2x return"

### Breakdown Cards

| Output | Formula | What it tells the buyer |
|--------|---------|------------------------|
| **Time Saved** | CSMs × hours_saved × 50 weeks | Total hours recovered per year |
| **Time Savings ($)** | hours_saved_total × (salary / 2,080) | Dollar value of recovered CSM time |
| **Churn Revenue Prevented** | portfolio_MRR × 12 × churn_rate × 15% catch-rate improvement | Revenue saved by catching at-risk accounts earlier (conservative 15% improvement on their current catch rate) |
| **Expansion Revenue Surfaced** | portfolio_MRR × 12 × 2% | Additional pipeline from earlier signal detection (conservative 2% of ARR) |
| **Total Annual Value** | time_savings + churn_prevented + expansion_surfaced | Gross benefit |
| **Net ROI** | total_value − product_cost | Bottom-line impact |

---

## UX Behavior
- All outputs update instantly as sliders move (no "Calculate" button)
- Sliders show their current numeric value and update a live label
- Output section uses the existing color system: blue for primary numbers, green for positive deltas
- Smooth number transitions (CSS or lightweight JS counter) when values change
- On mobile, sliders stack vertically; output cards stack below

---

## Section Layout

```
┌─────────────────────────────────────────────────┐
│  Section Label: "ROI Calculator"                │
│  Title: "See what Monday Morning Playbook       │
│          is worth for your team"                │
│  Subtitle: "Adjust the inputs to match your     │
│             team — results update instantly."   │
│                                                 │
│  ┌──────────────────┐  ┌──────────────────────┐ │
│  │  INPUTS           │  │  OUTPUTS             │ │
│  │                   │  │                      │ │
│  │  [Slider] CSMs    │  │  NET ANNUAL ROI      │ │
│  │  [Slider] Salary  │  │  $XXX,XXX    (7.2x)  │ │
│  │  [Slider] Hours   │  │                      │ │
│  │  [Slider] ARR     │  │  ┌────┐ ┌────┐ ┌───┐│ │
│  │  [Slider] Churn   │  │  │Time│ │Chrn│ │Exp││ │
│  │  [Slider] Cost    │  │  │Save│ │Prev│ │Rev││ │
│  │                   │  │  └────┘ └────┘ └───┘│ │
│  └──────────────────┘  └──────────────────────┘ │
└─────────────────────────────────────────────────┘
```

---

## Technical Requirements
- Vanilla JS only — no frameworks or libraries
- All calculation logic inline in `<script>` block
- CSS within existing `<style>` block
- Slider inputs use native `<input type="range">` with synced numeric display
- Numbers formatted with commas and appropriate currency symbols
- Responsive: two-column on desktop, single-column stacked on mobile
- Accessible: sliders have `<label>` elements, output uses `aria-live="polite"` for screen readers

---

## Assumptions & Constraints
- Conservative multipliers (15% churn improvement, 2% expansion) to maintain credibility; overpromising kills trust with this buyer
- Product cost shown transparently — the persona values no enterprise-only gating
- No email capture or gating — results are fully visible immediately
- All math is client-side; no backend calls

---

## Out of Scope
- PDF export of results
- Saving/sharing calculator results via URL
- Custom scenario comparison (side by side)

---

## Decisions Log

| # | Question | Decision |
|---|----------|----------|
| 1 | Gated or ungated? | Ungated — matches persona's preference for transparency |
| 2 | Placement | New section on landing page between Social Proof and CTA |
| 3 | Interactivity | Live sliders with real-time output updates |

---

## Open Questions
*None — all questions resolved.*
