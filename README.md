# thamizh-ai

The site at **[thamizh-ai.org](https://thamizh-ai.org)** — how and why
[Thamizh MCP](https://github.com/ief-global/thamizh-mcp) is built, written for Tamil scholars,
teachers and developers rather than for engineers only.

A project of the [International Educational Foundation](https://ief-global.org), a nonprofit.

## What this site is, and when it stops

It carries the design and architecture while there is nothing public to use. **When the app goes
live it takes this domain, and this becomes an archive.** That is deliberate: once there is a tool,
the tool should speak for itself, and how we got here is history.

So: old page URLs will redirect to the app rather than 404, the archive is a git tag plus a release
snapshot of `dist/`, and letters to institutions cite the design repo alongside the site, because
`github.com/ief-global/thamizh-mcp-design` is the address that still resolves in five years.

## The three repos

| Repo | Carries |
|---|---|
| [`thamizh-mcp`](https://github.com/ief-global/thamizh-mcp) | The server. Code, tests, pinned classical texts, grammar rule tables. Apache-2.0. |
| [`thamizh-mcp-design`](https://github.com/ief-global/thamizh-mcp-design) | The *why*. Design, decision log, glossary, roadmap, source provenance. **Authoritative.** |
| `thamizh-ai` (this one) | The public reading of both, as a website. A **view**, never a fork. |

If this site and the design repo disagree, **the design repo wins and this site needs fixing.**

## Running it

```bash
npm install
npm run dev      # http://localhost:4321
npm run build    # static output in dist/
```

`astro check` is not wired up yet: it wants `@astrojs/check` and `typescript` as extra
dependencies, and at this size the build catches what matters. Add it when the site grows.

```bash
```

Node 18+ (built on 22). No database, no API, no server runtime. It is static files.

## Deploying

Cloudflare builds this from GitHub. The dashboard asks for two commands and no output directory,
because the output directory lives in [`wrangler.jsonc`](wrangler.jsonc) instead:

| Field | Value | Where |
|---|---|---|
| Build command | `npm run build` | Settings → Build |
| Deploy command | `npx wrangler deploy` | Settings → Build |
| Root directory | leave empty | Settings → Build |
| **Production branch** | **`main`** | Settings → Build → **Branch control** |
| Builds for non-production branches | on, if you want preview URLs per PR | same panel |
| Custom domain | `thamizh-ai.org` | Settings → **Domains & Routes** → Add → Custom Domain |

**Production branch defaults to the repository's default branch**, so check it. If it is set to
`develop`, every integration push goes straight to the live site, which is exactly what the
`develop` → PR → `main` flow exists to prevent.

Turning non-production builds on is worth it here: each PR gets its own URL, so the rendered Tamil
can be checked before merge rather than after.

`wrangler.jsonc` declares `assets.directory: "./dist"`, `html_handling: "auto-trailing-slash"` so a
page is served at `/why` rather than `/why.html`, and `not_found_handling: "404-page"` so a bad URL
gets our own 404. There is no `main`: this is an assets-only Worker, so no server code runs.

Check it locally before pushing a change to the deploy config:

```bash
npm run build
npx wrangler deploy --dry-run
```

## Layout

```
src/
  data/status.json         every measured number on the site, and nothing else has one
  data/tokenization.json   our own tokenizer measurement, produced by scripts/measure-tokens.py
  layouts/Base.astro       page chrome, nav, footer, the "derives from" line
  components/              LayerStack (the D1 diagram and the site's navigation), StatusStrip
  pages/                   one file per page; pages/ta/ is the Tamil mirror
  styles/tokens.css        the BRAND.md palette, mirrored
public/
  fonts/                   Noto Sans Tamil, self-hosted. No third-party font CDN.
  img/CREDITS.md           every image, its licence and its source
scripts/                   sync-grammar.py, sync-sources.py, sync-glossary.py copy verified
                           material out of the sibling repos; measure-tokens.py measures
```

## Two rules that keep this honest

1. **No measured number is typed into prose.** It lives in `src/data/status.json` with the date it
   was verified and a link to `CODE-STATUS.md`. When the server's numbers change, this file changes
   in the same session.
2. **Every page names the document it derives from**, in its own footer.
3. **No நூற்பா, source grade or glossary entry is typed by hand.** The sync scripts copy them out of
   the other two repos, because a transcription drifts within minutes of being read and the drift is
   invisible. Run them, do not edit their output.

## Contributing

Corrections from Tamil scholars and teachers are the most valuable thing this project can receive,
especially a grammar claim that is wrong or cited to the wrong நூற்பா. Please name the verse you
would cite instead. Open an issue here for anything about the site; open one in
[`thamizh-mcp-design`](https://github.com/ief-global/thamizh-mcp-design) for anything about the
linguistics.

Branch flow, same as the other two repos: work on `develop`, PR to `main`.

## Licences

Code Apache-2.0, prose and diagrams CC BY-SA 4.0. See [`LICENSE-CONTENT.md`](LICENSE-CONTENT.md).
