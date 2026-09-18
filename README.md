# barrosef.com

Bilingual (EN at `/`, PT at `/pt-br/`) Hugo blog. Theme: PaperMod (submodule —
run `git submodule update --init` after cloning). Deployed to GitHub Pages
by `.github/workflows/deploy.yml` on push to `main`.

## Writing a post (cheat sheet)

1. `make post SLUG=my-post-slug` — scaffolds the EN+PT pair.
2. Write `content/en/posts/my-post-slug.md` and `content/pt-br/posts/my-post-slug.md`.
3. `make serve` — live preview (drafts included) at http://localhost:1313.
4. Set `draft: false` in **both** files; `make check` to verify locally.
5. Push to `main` — live in ~1 minute. CI blocks half-translated pairs.

Run `make test` to exercise the translation checker's own test suite.

## The owner's facts

`data/career.yaml` is the one source for the about page, the homepage hero and
metrics, and the footer email. Every prose field is `{ en, pt-br }`. Roles and
projects are separate lists; a project carries problem / approach / outcome and
the `components` that draw its architecture strip. The phone number is
deliberately not in it.

## Code in articles

Every code block in a post gets a copy button (`layouts/_partials/code-copy.html`).
A block worth fetching lives as a real file under `static/snippets/<post>/` and is
embedded with `{{< snippet file="<post>/<name>" lang="yaml" >}}`: the reader sees
the file name, a *raw* link and the copy button — the site's own gists.

## Social cards (`og:image`)

Every post gets its own 1200×630 card at `static/og/<translationKey>.<lang>.png`,
rendered by `python3 scripts/gen_og_images.py` (Pillow + fontTools; the site's
own Plex fonts) and committed. `head.html` uses it when the file exists, a page's
`image:` front matter overrides it, and everything else falls back to
`static/og-default.png`. CI fails a post without a card; a retitled post needs
the script re-run.

## Configuration knobs (`hugo.toml`)

- `params.analytics.ga4` — GA4 measurement ID (loads only after cookie consent).
- `params.newsletter.kitFormId` — Kit embed form UID (empty hides all forms).
- `params.giscus.*` — from https://giscus.app after enabling repo Discussions.

Categories: Technology/Tecnologia, Barbecue/Churrasco, Jiu-Jitsu, Liberty/Liberdade.
