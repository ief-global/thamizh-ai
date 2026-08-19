# CLAUDE.md — thamizh-ai (the public site)

The website for [thamizh-ai.org](https://thamizh-ai.org). Astro, static, no backend.
It is the public reading of two other repos and **it is a view, never a fork**:

- [`ief-global/thamizh-mcp`](https://github.com/ief-global/thamizh-mcp) — the server (the *what*)
- [`ief-global/thamizh-mcp-design`](https://github.com/ief-global/thamizh-mcp-design) — design,
  decisions, glossary, provenance (the *why*). **Authoritative. If it and this site disagree, it wins.**

The plan this repo is built from is `WEBSITE-PLAN.md` in the design repo. Read it before adding a page.

## Git identity — use everywhere, no exceptions
Commit as **Saran Saravanan <saravanan3@duck.com>**, GitHub **ssaravanan3**.
NEVER commit under the legacy `asaravanan75@gmail.com`. Verify: `git log --format='%an <%ae>' -1`.

## Branch workflow — same as the other two repos
`main` = stable, deployed. `develop` = integration. Work on **`develop`** → push → open PR
`develop → main` → **Saran merges**. Do not commit straight to `main`.

## Accuracy guardrails — these are not style preferences

This site is public, quotable, and read by people who will fact-check the Tamil. The rules that
govern the design repo govern this one, and two more besides.

- **NEVER write a நூற்பா number from memory or from a secondary source.** Look it up in the code
  repo's `data/classical/*.json`. TVA renumbers: its 336/319/136 are **337/320/137** in the pinned
  edition. Tholkappiyam numbers restart per இயல் — cite அதிகாரம் › இயல் › நூற்பா. Nannūl is
  continuous 1–462.
- **Never invent a Tamil example.** Every Tamil form on this site must already appear, verified,
  in the design repo or in the live build. A fabricated example on a site about not fabricating
  Tamil would be fatal.
- **Do not use ஜன்னல் as an origin example.** The tool classifies it வடசொல் because of the Grantha
  ஜ, but it is a **Portuguese** loan (*janela*). Its equivalent (→ சாளரம்) is correct and safe.
- **Do not claim we beat frontier models.** The honest claim: models fail on harder items and
  lexical facts, weaker models fail far more, and only our answers are citable and reproducible.
- **Do not quote a "lift %".** The A/B measurement is not finished.
- **Positioning:** "plausibly the first Tamil **சொல்-analysis MCP server**", never "the first Tamil
  NLP tool". There is a rich Tamil NLP ecosystem and we stand on it.
- **Attribute ThamizhiMorph** (Sarveswaran, Dias & Butt 2021, Apache-2.0) wherever the analyser is
  discussed.
- **A repo description is not a citation.** Verify a paper's authors and venue before naming them.

## The two mechanisms that stop this site going stale

1. **`src/data/status.json` is the only place a measured number lives.** Tests, tool count, sweep
   results, dates. Never type one into prose. When `CODE-STATUS.md` changes, change this file in the
   same session.
2. **Every page passes `derivesFrom` to the layout**, naming the design-repo document behind it.

`src/data/tokenization.json` is our own measurement, not a quotation. Regenerate it with
`scripts/measure-tokens.py` rather than editing it, and update `measured_on` when you do.

## Design

Tokens in `src/styles/tokens.css` mirror `BRAND.md` in the design repo. Change that file first.

- **Tamil is the primary typeface**, headings and body included. The Latin UI face is for labels,
  kickers and figures only. Never letter-space or uppercase Tamil; wrap Tamil inside a UI label in
  `.ta`.
- **Fonts are self-hosted** in `public/fonts/`. No Google Fonts CDN: it is a third-party dependency
  and a privacy question for an audience in India.
- **Check `/render-check` after every deploy** and after any font change. Broken Tamil shaping fails
  silently and costs credibility in one screen.
- **Images:** public domain or CC0 only, recorded in `public/img/CREDITS.md` and credited on the page.
  Photography of primary Tamil sources and monuments is welcome. Generic stock imagery, kolam
  borders and AI-brain art are not.
- Three theme states (system, explicit light, explicit dark). Define colours as tokens, never inside
  a media query only.

## Prose

Follow `anti-ai-writing-style.md` in the design repo. The ones that bite most often here: no em
dashes, no "not X, but Y" reframes, short paragraphs, and no hype vocabulary. Scholarly and calm.
Honesty is the brand: say what does not work yet.

## Gotchas

- Nav entries and layer names for pages that are not built yet render as **plain text, not links**
  (`ready` flags in `Base.astro` and `LayerStack.astro`). Flip the flag when the page ships, and
  check `dist/` for dead internal links before pushing.
- `build.format: 'file'`, so `src/pages/ta/index.astro` builds to `/ta.html`.
