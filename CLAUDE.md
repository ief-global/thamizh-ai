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
- **A repo description is not a citation.** Every paper the site cites lives in
  `src/data/papers.json` with the record it was verified against and the date. Render it with the
  `Paper` component. Adding a citation means checking the ACL Anthology or arXiv record first, not
  after.

## The two mechanisms that stop this site going stale

1. **`src/data/status.json` is the only place a measured number lives.** Tests, tool count, sweep
   results, dates. Never type one into prose. When `CODE-STATUS.md` changes, change this file in the
   same session.
2. **Every page passes `derivesFrom` to the layout**, naming the design-repo document behind it.

`src/data/tokenization.json` is our own measurement, not a quotation. Regenerate it with
`scripts/measure-tokens.py` rather than editing it, and update `measured_on` when you do.

**Four data files are generated. Do not hand-edit any of them.**

| File | Script | Copies from |
|---|---|---|
| `src/data/grammar.json` | `scripts/sync-grammar.py` | `thamizh-mcp/data/grammar/` — நூற்பா, cited verbatim |
| `src/data/sources.json` | `scripts/sync-sources.py` | `thamizh-mcp/data/sources.json` — the source registry |
| `src/data/glossary.json` | `scripts/sync-glossary.py` | `thamizh-mcp-design/Glossary.md` — the quick-reference table |
| `src/data/tokenization.json` | `scripts/measure-tokens.py` | measured here, with `tiktoken` |

`src/data/papers.json` is hand-maintained and is the exception, because a citation cannot be synced
from anywhere. Each entry records what it was verified against and when.

Each script exits quietly when the sibling repo is missing, so a CI build never depends on a
checkout it does not have. Re-run all three syncs after pulling either sibling repo.

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

## Deployment

Cloudflare Workers static assets, deployed by **GitHub Actions** on push to `main`
(`.github/workflows/deploy.yml`), using `CLOUDFLARE_API_TOKEN` and `CLOUDFLARE_ACCOUNT_ID` secrets.

**We do not use Cloudflare's Git integration, on purpose.** The Cloudflare account that owns the
`thamizh-ai.org` zone is not the identity used for GitHub work, and connecting it would add a second
GitHub identity to the `ief-global` org for no benefit. Pushing from Actions keeps them apart. If
someone reconnects the Cloudflare Git integration, disconnect it: both would deploy on every push.

Settings live in `wrangler.jsonc`, **not** in the dashboard: `assets.directory` is the output
directory the dashboard never asks for. Verify a config change with `npx wrangler deploy --dry-run`
before pushing. Do not deploy from a laptop.

**Custom domains are `thamizh-ai.org` and `www.thamizh-ai.org` only.** `api.` is reserved for the
REST and MCP head and was deliberately detached from this Worker after briefly serving the site.

**Every page carries a canonical URL pointing at `https://thamizh-ai.org`**, computed in
`Base.astro`. The workers.dev deployment and every preview build serve the same pages, and without
canonicals they compete with the apex in search. That matters more than usual here, because the
outreach letters cite the apex by name.

## Gotchas

- **`const DRAFT` in `Base.astro`** shows or hides the draft banner. One switch, so it cannot be
  half-done. It comes off when Saran has read the Tamil, not before.
- `LayerStack.astro` carries a `ready` set: a layer whose page does not exist yet renders as plain
  text rather than a dead link. Add the id when the page ships. Check `dist/` for dead internal
  links before pushing; CI fails on one anyway.
- `build.format: 'file'`, so `src/pages/ta/index.astro` builds to `/ta.html`. Cloudflare's
  `html_handling: auto-trailing-slash` serves that at `/ta`. Keep the two settings in step: changing
  Astro's `trailingSlash` or `format` without changing `wrangler.jsonc` silently breaks every URL.
- Contact address for the site is **thamizh@ief-global.org** (created 2026-08-19). Use it on
  `/about` and in anything a scholar or an institution would reply to.
