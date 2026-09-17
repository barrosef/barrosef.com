# About page — CV and projects — Design Spec

**Date:** 2026-09-16
**Status:** Built locally for the owner's validation; not yet pushed.
**Supersedes:** the thin `/about/` prose page from the professional-site spec (2026-08-19).

## Purpose

Give a recruiter or executive one page that answers "who is this, what has he done, what does he build" — the rich `/about/` ↔ `/pt-br/sobre/`. The homepage stays a summary but stops being empty. Articles come later; this page does not depend on them.

## Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Location | Rich `/about/`; homepage stays a summary | Owner's choice over "homepage becomes the page" and "separate /cv/ + /projects/" |
| Languages | EN and PT-BR from day one | CI enforces the mirror; a half-built page is not validatable |
| Contact | Email, LinkedIn, GitHub public; **phone stays private** | Owner's choice |
| Positioning | Breadth and adaptability across stacks, teams and sectors; justice-sector work in the body, not the headline | Owner's 2026-08-21 decision — do not re-argue |
| Source of truth | `data/career.yaml`, every prose field `{ en, pt-br }` | One file feeds the about page, the homepage hero, the metrics band and the footer email. `params.profile` in `hugo.toml` is retired. Shape mirrors the career-source tool's model (roles ≠ projects; a project has problem / approach / outcome) so that tool can emit this file later |
| Project visuals | Generated architecture strip from `components[]`; no screenshots | Spartacus screenshots show children's data; DOP's cockpit shot carries an emulator-mode banner. Screenshots are a later swap-in |
| The one visual device | Year ruler 2003 → today above the timeline, one segment per role, labelled with `short` | Twenty-three unbroken years read at a glance before any bullet. Everything else stays quiet text |
| Print | `@media print` turns the page into the CV | What a recruiter does with it; no separate PDF pipeline yet |

## Page structure

1. **Identity** (navy) — photo, name, headline, positioning sentence, location · email · LinkedIn · GitHub, sector chips.
2. **Rail + body** (white) — sticky section rail (Profile · Experience · Projects · Skills · Education) with a scroll-spy; horizontal strip on mobile.
3. **Experience** — year ruler, then the timeline: period, title, company (with an EN gloss for Brazilian institutions), sector, highlights, stack chips.
4. **Projects** — DOP and Spartacus: architecture strip on the left; tagline, problem, approach, where it stands, stack, repo link on the right.
5. **Skills** grouped as the CV header groups them; **Education & certifications**; the personal paragraph from the page body.
6. **Closing** (navy) — one question and the two buttons.

## Also fixed

`data/practice.yaml` still used `title_pt` keys after the `pt → pt-br` locale rename, so the PT homepage's capability cards rendered empty. Now `{ en, pt-br }` like `career.yaml`. The footer's six social icons overflowed a 390px viewport; it wraps now.

## Revision 2026-09-16 (same day)

- Owner is no longer at Sogni Sports (ended 2025-10). Current role since 2025-11: **independent consultant** — AI-assisted software development, cloud infrastructure, IT product development. The homepage kicker and the three capability cards now state the consulting offer; the hero role line reads "Independent consultant · Brasnorte, MT — Brazil · Previously Sogni Sports, BEE4, Totem".
- Two client projects added, **Factor** (last-mile logistics: driver app + payroll pipeline) and **Pipe365 Mobile** (WhatsApp customer-service app), marked `client: true`: product name only, no client company named, no repo links, a "Client engagement · private code" label instead.
- `company` and `short` in `roles[]` may be bilingual maps; `layouts/_partials/l10n.html` resolves either shape.
- Ruler labels hide via a container query when a segment is narrower than 44px (the current consulting segment).

## Revision 2026-09-17

- **The year ruler is gone; a horizontal timeline replaces it.** One stake per role on a shared axis, oldest on the left, cards alternating above and below the axis (each card is wider than its column, positioned absolutely and centred on its dot), the start year under each dot, the current role's dot breathing (reduced-motion respected). A card is a button: selecting it shows that role in the panel below, one at a time once the script runs (`.tl-js`); arrow keys move along the axis. Without JS, on a phone (< 900px) and in print, every role is listed — on a phone the list itself carries a vertical spine with dots.
- **Clients are named on the consulting role**, one high-level line each, no project detail: CSP Tech, Tecnomapas, Connsoft, Factor Logistics. `roles[].clients[]` in `career.yaml`.
- **Projects are grouped**: "Own products" (DOP, Spartacus) and "Client work" (Factor for Factor Logistics, Pipe365 Mobile for Connsoft) via `kind: own | client`; the client's name is shown after the title.

## Revision 2026-09-17 (afternoon) — the about section

- `/about/` is now a **section** with a hub and four sub-pages: **Career** (`/about/career/` ↔ `/pt-br/sobre/carreira/`, everything the about page used to be), **Jiu-Jitsu**, **Barbecue**, **Libertarianism** — the last three "coming soon" pages (`soon: true`, `layout: soon`). Layouts: `hub.html`, `career.html` (was `about.html`), `soon.html`; partials `about-nav.html` (tabs: Overview + sub-pages by weight) and `about-header.html` (compact identity strip on sub-pages).
- The header's About item is a CSS-only dropdown (hover / focus-within) built from nested menu entries in `hugo.toml`; hidden under 900px, where the tabs do the job.
- Projects list **own products only** (DOP, Spartacus); Factor and Pipe365 were removed from `career.yaml`. Client work stays as one-line citations on the consulting role.
- Fixed in passing: `layouts/list.html` still tested `eq $lang "pt"` after the `pt-br` rename, so the PT writing index grouped nothing under Tecnologia.

## Facts the owner should check

- `profile.location` is "Brasnorte, MT — Brazil" (confirmed by the owner, 2026-09-16).
- Project periods come from first commits (Spartacus 2025-11, DOP 2026-05); Spartacus is described as in production on the strength of the July 2026 Play Store testing marathon.
- Metrics: 23 years, 7 sectors, 2 teams (MP-MT and Sogni Sports). No number was invented; a "states integrated with PJe" figure was dropped because the CV does not give one.

## Verification

`make check` (build + translation mirror) passes. Reviewed at 1360px and 390px in both languages; all text pairs meet WCAG AA (lowest: ruler labels at 4.6:1). Printed via headless Chromium: header, rail and closing hidden; identity, ruler and timeline survive.
