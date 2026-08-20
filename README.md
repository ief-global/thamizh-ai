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

**GitHub Actions deploys to Cloudflare on every push to `main`** (`.github/workflows/deploy.yml`).
It builds, refuses to deploy if any internal link is dead, runs `wrangler deploy`, then checks that
the live site answers.

This pushes *from* GitHub *to* Cloudflare, which is the opposite of Cloudflare's Git integration,
and that is deliberate. The Cloudflare account holding the `thamizh-ai.org` zone is not the identity
used for GitHub work here, and connecting it would put a second GitHub identity on the `ief-global`
org for no benefit. A scoped API token keeps the two apart.

### One-time setup

1. In the Cloudflare account that owns the Worker: **My Profile → API Tokens → Create Token →
   "Edit Cloudflare Workers"**. Scope it to that account only, and to the `thamizh-ai.org` zone only.
2. In this repository: **Settings → Secrets and variables → Actions**, add
   `CLOUDFLARE_API_TOKEN` and `CLOUDFLARE_ACCOUNT_ID` (the ID on the Workers & Pages overview).
3. If Cloudflare's own Git integration is connected to this Worker, **disconnect it**, or both will
   deploy on every push.

Rotate the token by replacing the secret. Nothing in the repo changes.

### The Worker's own settings

`wrangler.jsonc` carries what the dashboard does not ask for: `assets.directory` is `./dist`,
`html_handling` is `auto-trailing-slash` so a page serves at `/why` rather than `/why.html`, and
`not_found_handling` is `404-page`. There is no `main`, so this is an assets-only Worker and no
server code runs.

Custom domains on the Worker: **`thamizh-ai.org`** and **`www.thamizh-ai.org`**. `api.` is reserved
for the REST and MCP head later and must not be pointed at this Worker.

Check a deploy-config change before pushing:

```bash
npm run build
npx wrangler deploy --dry-run
```

## Layout## Layout

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
