---
name: programmatic-seo
description: "Generate SEO-optimized landing pages and blog posts from keyword research data. Use this skill when the user wants to create SEO content pages, build landing pages from keywords, generate blog posts for content marketing, do programmatic SEO, create pages from keyword data, or scale content production. Also triggers on phrases like 'create pages from keywords', 'build SEO pages', 'generate content for keywords', 'turn keywords into pages', 'programmatic content', or 'SEO page generator'. Requires keyword data (keywords.md or similar) and the site's existing design system."
---

Generate SEO-optimized landing pages and companion blog posts from keyword research data, using AI-generated images and the site's existing design system. Each keyword cluster gets two pages: a conversion-focused landing page and a long-form blog post.

## Input

The user may provide:
- A keyword research file (e.g., `keywords.md`) with prioritized keyword tiers
- Specific keywords or tiers to target (e.g., "Tier 1 only", "these 3 keywords")
- Content angle or messaging direction
- Whether to generate images or skip them

If the user doesn't specify which keywords, default to **Tier 1 — Own These Now** keywords from `keywords.md`. If no keyword file exists, tell the user to run the `keyword-research` skill first.

## Step 1: Gather Context

Read these files to understand the product, audience, and existing design:
- `keywords.md` — keyword data with tiers, volumes, competition scores
- `persona.md` — buyer persona, pain points, goals, language
- `prd.md` — product features, positioning, value props
- `CLAUDE.md` — project overview and tech stack
- `index.html` — existing design system (CSS variables, nav structure, footer)

Extract:
- **Target keywords** — which keywords to create pages for
- **Buyer language** — how the persona talks about these problems
- **Product positioning** — how the product solves each keyword's problem
- **Design tokens** — CSS variables, fonts, colors, spacing from the existing site
- **Nav/footer structure** — so new pages integrate seamlessly

### Consolidate Keywords into Page Topics

Multiple keywords often map to the same page. Group overlapping keywords into clusters:
- "renewal management software" + "software renewal management" → one page
- "customer churn prediction software" + "churn prediction software" → one page

Each cluster gets one landing page + one blog post. The primary keyword (highest volume) becomes the page slug and H1; secondary keywords appear naturally in body copy.

## Step 2: Plan the Pages

For each keyword cluster, define:

| Field | Landing Page | Blog Post |
|-------|-------------|-----------|
| **Purpose** | Convert visitors → trial/demo | Educate, build authority, earn backlinks |
| **URL** | `/solutions/{keyword-slug}.html` | `/blog/{keyword-slug}-guide.html` |
| **H1** | Primary keyword + benefit | Primary keyword + "Guide" / "Framework" / hook |
| **Length** | ~25-35KB (5-7 sections) | ~25-40KB (2000-3000 words) |
| **Layout** | Full-width sections, 1140px container | Narrow article column, 720px max-width |
| **CTA density** | Hero + mid-page + bottom | Inline CTA box + bottom CTA |

Create the `solutions/` and `blog/` directories if they don't exist.

## Step 3: Generate Images

For each page, generate a hero image using `scripts/generate-image.py`. Run the script for each image:

```bash
python3 scripts/generate-image.py "PROMPT" --output images/{filename}.png
```

### Image Prompts

Craft prompts that match the site's dark, modern aesthetic:

**Landing page heroes** — abstract data visualizations:
```
Dark, modern abstract visualization representing {keyword concept}.
Glowing indigo (#6366f1) and emerald (#34d399) data streams on a near-black
background. Clean geometric shapes suggesting {relevant metaphor}.
Professional SaaS dashboard aesthetic. No text.
```

**Blog post heroes** — wider editorial images:
```
Wide editorial illustration for a blog post about {keyword topic}.
Dark background with subtle gradient. Abstract shapes representing
{concept}. Muted indigo and green accents. Modern, clean, professional.
No text or logos.
```

If image generation fails (API error, quota), continue without images and note which ones need to be generated later.

## Step 4: Build Landing Pages

Each landing page follows this section structure. All styles are inline in a `<style>` block — no external CSS files.

### HTML Template Structure

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{Primary Keyword} | Monday Morning Playbook</title>
  <meta name="description" content="{130-155 char description with primary keyword near the front}" />
  <link rel="canonical" href="https://mondaymorningplaybook.com/solutions/{slug}.html" />
  <link href="https://fonts.googleapis.com/css2?family=DM+Sans:ital,wght@0,400;0,500;0,700&family=Instrument+Serif:ital@0;1&display=swap" rel="stylesheet" />
  <style>/* all CSS inline */</style>
</head>
<body>
  <nav>...</nav>
  <main>
    <section class="hero-wrap">...</section>
    <hr class="section-divider" />
    <section><!-- Pain Points --></section>
    <hr class="section-divider" />
    <section><!-- How It Works --></section>
    <hr class="section-divider" />
    <section><!-- Feature Spotlight --></section>
    <hr class="section-divider" />
    <section><!-- Social Proof --></section>
    <hr class="section-divider" />
    <section class="cta-section">...</section>
  </main>
  <footer>...</footer>
  <script>/* intersection observer animations */</script>
</body>
</html>
```

### Required Design Tokens (CSS Custom Properties)

Every page must include these in `:root`:

```css
:root {
  --ink: #0a0a0f;
  --ink-90: #141419;
  --ink-80: #1e1e26;
  --ink-70: #2a2a35;
  --ink-60: #3a3a48;
  --ink-50: #52526a;
  --ink-40: #7a7a95;
  --ink-30: #9e9eb5;
  --ink-20: #c4c4d4;
  --ink-10: #e8e8f0;
  --white: #f5f5f7;
  --accent: #6366f1;
  --accent-dim: #4f46e5;
  --accent-glow: rgba(99,102,241,.15);
  --accent-glow2: rgba(99,102,241,.08);
  --mint: #34d399;
  --mint-dim: rgba(52,211,153,.12);
  --coral: #f87171;
  --coral-dim: rgba(248,113,113,.12);
  --amber: #fbbf24;
  --amber-dim: rgba(251,191,36,.12);
  --radius: 10px;
  --radius-lg: 16px;
  --radius-xl: 24px;
  --font-display: 'Instrument Serif', Georgia, serif;
  --font-body: 'DM Sans', -apple-system, BlinkMacSystemFont, sans-serif;
}
```

### Nav Component

```html
<nav>
  <div class="nav-left">
    <a href="/index.html" class="logo">Monday Morning Playbook</a>
    <ul class="nav-links">
      <li><a href="/index.html#features">Features</a></li>
      <li><a href="/index.html#roi">ROI Calculator</a></li>
      <li><a href="/blog/customer-churn-prevention-guide.html">Blog</a></li>
    </ul>
  </div>
  <div class="nav-right">
    <a href="/demo.html" class="btn btn-ghost">See a Demo</a>
    <a href="/index.html#cta" class="btn btn-primary">Start Free Trial</a>
  </div>
</nav>
```

Nav CSS: sticky, `backdrop-filter: blur(20px) saturate(180%)`, 64px height, semi-transparent dark background.

### Landing Page Sections

**1. Hero Section**
- Eyebrow badge with pulsing dot indicator
- H1 (64px, serif font) — must contain the primary keyword
- Subtitle (19px) — benefit-focused, references the persona's pain
- Two buttons: primary "Start Free Trial" + ghost "See a Demo"
- Hero image with float animation and glow shadow
- Background: radial gradient overlays (accent-glow + coral-glow)

**2. Pain Points (3-column grid)**
- Section label (uppercase, 12px, accent color)
- Section title (42px, serif) with `<em>` emphasis
- 3 cards with colored icons (coral, amber, accent), title, description
- Cards: dark background, border, hover lift effect

**3. How It Works (3 steps)**
- Numbered circles (72px, accent border) with connecting line
- Step title + description beneath each number
- Responsive: collapses to single column on mobile

**4. Feature Spotlight (2-column)**
- Left: text explaining the feature
- Right: visual mockup (health dashboard, data table, etc.)
- Use coral/amber/mint color coding for status indicators in mockups

**5. Social Proof**
- Large stat number (64px, mint color) + context label
- Blockquote with author name + role
- Left accent border on quote

**6. Bottom CTA**
- Large title (48px) + subtitle + button pair
- Radial gradient background glow

### Footer Component

```html
<footer>
  <div class="footer-inner">
    <span class="footer-brand">Monday Morning Playbook</span>
    <ul class="footer-links">
      <li><a href="/index.html#how">How It Works</a></li>
      <li><a href="/index.html#features">Features</a></li>
      <!-- Add links to other solution/blog pages -->
      <li><a href="#">Privacy</a></li>
      <li><a href="#">Terms</a></li>
    </ul>
    <span class="footer-copy">&copy; 2026 Monday Morning Playbook</span>
  </div>
</footer>
```

### Animation System

Include this JavaScript at the bottom of every page:

```javascript
const observer = new IntersectionObserver((entries) => {
  entries.forEach(e => { if (e.isIntersecting) { e.target.classList.add('in-view'); observer.unobserve(e.target); } });
}, { threshold: 0.15 });
document.querySelectorAll('.anim-fade-up').forEach(el => observer.observe(el));
```

Animation classes: `.anim-fade-up` with stagger delays `.anim-d1` through `.anim-d5` (0.1s increments).

### Responsive Breakpoint

All pages need a `@media (max-width: 768px)` block that:
- Hides `.nav-links`
- Collapses grids to single column
- Reduces hero title to 38px, section titles to 30px
- Reduces horizontal padding to 20px

## Step 5: Build Blog Posts

Blog posts use a narrower, article-focused layout (720px max-width).

### Blog HTML Template

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{Keyword}: {Compelling Hook} ({Year}) | Monday Morning Playbook</title>
  <meta name="description" content="{150 char description with keyword}" />
  <link rel="canonical" href="https://mondaymorningplaybook.com/blog/{slug}-guide.html" />
  <!-- same Google Fonts link -->
  <style>/* all CSS inline */</style>
</head>
<body>
  <nav><!-- same nav --></nav>
  <main>
    <img src="../images/{blog-hero}.png" alt="{descriptive alt text}" class="blog-hero-image" />
    <div class="blog-header">
      <div class="blog-meta">
        <span class="blog-category">Customer Success</span>
        <span class="blog-date">{Month Day, Year}</span>
      </div>
      <h1 class="blog-title">{Primary Keyword}: {Hook}</h1>
      <p class="blog-intro">{1-2 sentence intro with keyword}</p>
    </div>
    <div class="article">
      <!-- H2/H3 sections with rich content -->
      <!-- Inline CTA box mid-article -->
      <!-- Related links grid at bottom -->
    </div>
  </main>
  <footer><!-- same footer --></footer>
</body>
</html>
```

### Blog-Specific CSS

```css
.blog-hero-image { width:100%; max-height:420px; object-fit:cover; }
.blog-header { max-width:720px; margin:0 auto; padding:48px 24px 0; }
.blog-meta { display:flex; align-items:center; gap:16px; margin-bottom:20px; }
.blog-category { font-size:12px; text-transform:uppercase; letter-spacing:1.5px;
  color:var(--accent); background:var(--accent-glow2); padding:4px 12px;
  border-radius:20px; font-weight:600; }
.blog-date { font-size:14px; color:var(--ink-40); }
.blog-title { font-family:var(--font-display); font-size:48px; line-height:1.15;
  color:var(--white); margin-bottom:20px; }
.blog-intro { font-size:19px; color:var(--ink-20); line-height:1.7;
  padding-bottom:32px; border-bottom:1px solid var(--ink-70); margin-bottom:40px; }
.article { max-width:720px; margin:0 auto; padding:0 24px 80px; }
.article h2 { font-family:var(--font-display); font-size:34px; color:var(--white);
  margin:56px 0 20px; }
.article h3 { font-size:24px; font-weight:700; color:var(--ink-10);
  margin:40px 0 16px; }
.article p { font-size:17px; line-height:1.8; color:var(--ink-20); margin-bottom:20px; }
.article a { color:var(--accent); text-decoration:underline;
  text-underline-offset:3px; }
.article blockquote { border-left:3px solid var(--accent); padding:16px 24px;
  margin:32px 0; background:var(--ink-90); border-radius:0 var(--radius) var(--radius) 0; }
.article ul, .article ol { padding-left:24px; margin-bottom:20px; }
.article li { font-size:17px; line-height:1.8; color:var(--ink-20); margin-bottom:8px; }
```

### Blog Content Structure

Each blog post should be 2000-3000 words with:
1. **Introduction** — hook the reader with the problem (reference persona pain points)
2. **3-7 main sections** (H2s) — each covering a strategy, component, or concept
3. **Subsections** (H3s) — breaking down each main section
4. **Inline CTA** — placed after the 2nd or 3rd H2 section
5. **Conclusion** — summarize key points, link to product
6. **Related Links** — 2-column grid linking to other solution/blog pages

### Inline CTA Box

```html
<div class="inline-cta">
  <h3>Ready to {verb related to keyword}?</h3>
  <p>{1 sentence connecting keyword topic to product}</p>
  <a href="/index.html#cta" class="btn btn-primary btn-large">Start Free Trial</a>
</div>
```

CSS: accent border, dark background, centered text, subtle box-shadow with accent glow.

### Related Links Grid

```html
<div class="related-links">
  <a href="/solutions/{related-slug}.html" class="related-card">
    <span class="related-label">Solution</span>
    <span class="related-title">{Related Page Title}</span>
  </a>
  <a href="/blog/{related-slug}-guide.html" class="related-card">
    <span class="related-label">Guide</span>
    <span class="related-title">{Related Blog Title}</span>
  </a>
</div>
```

## Step 6: SEO Checklist

Before finishing each page, verify:

- [ ] **Title tag** contains primary keyword (under 60 characters)
- [ ] **Meta description** contains primary keyword (130-155 characters)
- [ ] **H1** contains primary keyword exactly once
- [ ] **URL slug** matches the primary keyword
- [ ] **Canonical URL** is set and correct
- [ ] **Secondary keywords** appear naturally in H2s and body copy
- [ ] **Internal cross-links** — each page links to at least 2 other pages on the site
- [ ] **CTA buttons** link to `/index.html#cta` or `/demo.html`
- [ ] **Alt text** on all images is descriptive and keyword-relevant
- [ ] **Mobile responsive** — all grids collapse, text sizes reduce

## Step 7: Update Site Navigation

After creating all pages, update `index.html`:

1. **Nav** — ensure "Blog" link exists in `.nav-links`
2. **Footer** — add links to new solution pages and blog section
3. **Cross-linking** — each new page's footer should link to all other new pages

Also update the footer on any previously existing pages to include the new page links.

## Step 8: Parallelize Page Generation

For efficiency, generate pages in parallel using agent teams. Each agent handles one keyword cluster (1 landing page + 1 blog post). All agents share the same design tokens and component templates.

When spawning agents, provide each with:
- The keyword cluster (primary + secondary keywords, volume, competition)
- The full design system (CSS variables, nav HTML, footer HTML)
- Content direction based on persona and product positioning
- Image file paths (generate images before spawning agents)

## Quality Standards

- **Design consistency** — every page must look like it belongs on the same site. Same fonts, colors, spacing, animation patterns.
- **Keyword natural usage** — keywords should read naturally in sentences. Never stuff keywords unnaturally. The H1 and title tag contain the exact keyword; body copy uses variations.
- **Persona-driven copy** — write for the buyer described in `persona.md`. Use their language, address their pain points, reference their goals.
- **Product honesty** — don't claim features that aren't in `prd.md`. Position the product accurately.
- **Mobile-first** — every layout must work on a 375px viewport.
- **No external dependencies** — all CSS and JS inline. Only external resources are Google Fonts.

## After Writing

1. Tell the user which pages were created and their URLs
2. List any images that failed to generate and need manual creation
3. Summarize the SEO targeting: which keyword each page targets, search volume, and competition level
4. Note any keywords that were skipped and why (e.g., too similar to an existing page)
