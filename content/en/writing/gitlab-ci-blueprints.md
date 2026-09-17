---
title: "GitLab CI for Kubernetes: a blueprint library for many apps and many clusters"
date: 2026-09-17T09:00:00-04:00
draft: false
translationKey: "gitlab-ci-blueprints"
categories: ["Technology"]
tags: ["gitlab-ci", "kubernetes", "devops", "delivery"]
description: "A delivery architecture that survived several apps, two rings and more than one cluster: a versioned blueprint library, thin app pipelines, a fleet repository that is the only thing talking to Kubernetes, and a live ring that releases what preview already ran instead of building again."
aliases: ["/writing/gitlab-ci-template-library/"]
---

Three apps, each with three or four deployable units. Two rings — preview and
live. More than one Kubernetes cluster, run by different teams. The first
version of that delivery was what it always is: a `.gitlab-ci.yml` copied from
the last project, edited until green, and never the same twice. A year later no
two pipelines agreed on what a branch meant, and a fix in one never reached
the others.

What follows is the architecture that replaced it. Names, paths and numbers
are illustrative; the shape is the thing.

## The shape

<figure class="diagram"><svg viewBox="0 0 760 432" role="img" aria-label="App repositories include a blueprint library; the app pipeline bakes images, pushes them to the registry and triggers the fleet pipeline, which applies manifests, sets images and waits for the rollout on each cluster." xmlns="http://www.w3.org/2000/svg" font-family="IBM Plex Sans, system-ui, sans-serif" color="#16233a"><defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="currentColor"/></marker><marker id="arrow-accent" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#1d4e89"/></marker></defs><rect x="290" y="16" width="180" height="52" fill="#eef2f7" stroke="currentColor" stroke-width="1"/><text x="380.0" y="39.0" text-anchor="middle" font-size="12" font-weight="600" fill="currentColor">ci-blueprints</text><text x="380.0" y="54.0" text-anchor="middle" font-size="10.5" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">blueprints/&lt;app&gt;/*.yml</text><text x="482" y="46" text-anchor="start" font-size="10.5" font-weight="400" fill="#5d6b7d">a library: it runs no pipeline of its own</text><rect x="20" y="104" width="110" height="52" fill="#fff" stroke="currentColor" stroke-width="1"/><text x="75.0" y="127.0" text-anchor="middle" font-size="12" font-weight="600" fill="currentColor">orders</text><text x="75.0" y="142.0" text-anchor="middle" font-size="10.5" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">.gitlab-ci.yml</text><line x1="75" y1="102" x2="330" y2="70" stroke="currentColor" stroke-width="1.2" stroke-dasharray="5 4" marker-end="url(#arrow)"/><rect x="150" y="104" width="110" height="52" fill="#fff" stroke="currentColor" stroke-width="1"/><text x="205.0" y="127.0" text-anchor="middle" font-size="12" font-weight="600" fill="currentColor">billing</text><text x="205.0" y="142.0" text-anchor="middle" font-size="10.5" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">.gitlab-ci.yml</text><line x1="205" y1="102" x2="370" y2="70" stroke="currentColor" stroke-width="1.2" stroke-dasharray="5 4" marker-end="url(#arrow)"/><rect x="280" y="104" width="110" height="52" fill="#fff" stroke="currentColor" stroke-width="1"/><text x="335.0" y="127.0" text-anchor="middle" font-size="12" font-weight="600" fill="currentColor">catalog</text><text x="335.0" y="142.0" text-anchor="middle" font-size="10.5" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">.gitlab-ci.yml</text><line x1="335" y1="102" x2="410" y2="70" stroke="currentColor" stroke-width="1.2" stroke-dasharray="5 4" marker-end="url(#arrow)"/><text x="408" y="98" text-anchor="start" font-size="10.5" font-weight="400" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">include · ref: v2.3.0</text><text x="402" y="134" text-anchor="start" font-size="10.5" font-weight="400" fill="#5d6b7d">app repositories — each pipeline is a thin include</text><rect x="20" y="196" width="370" height="70" fill="#fff" stroke="currentColor" stroke-width="1"/><text x="30" y="212" text-anchor="start" font-size="11" font-weight="600" fill="currentColor">orders pipeline (on push to candidate / main)</text><rect x="30" y="226" width="80" height="28" fill="#eef2f7" stroke="#c9d3e0"/><text x="70.0" y="244" text-anchor="middle" font-size="11" font-weight="400" fill="currentColor" font-family="IBM Plex Mono, ui-monospace, monospace">images</text><line x1="111" y1="240" x2="121" y2="240" stroke="currentColor" stroke-width="1.2" marker-end="url(#arrow)"/><rect x="122" y="226" width="80" height="28" fill="#eef2f7" stroke="#c9d3e0"/><text x="162.0" y="244" text-anchor="middle" font-size="11" font-weight="400" fill="currentColor" font-family="IBM Plex Mono, ui-monospace, monospace">release</text><line x1="203" y1="240" x2="213" y2="240" stroke="currentColor" stroke-width="1.2" marker-end="url(#arrow)"/><rect x="214" y="226" width="80" height="28" fill="#eef2f7" stroke="#c9d3e0"/><text x="254.0" y="244" text-anchor="middle" font-size="11" font-weight="400" fill="currentColor" font-family="IBM Plex Mono, ui-monospace, monospace">delivery</text><line x1="295" y1="240" x2="305" y2="240" stroke="currentColor" stroke-width="1.2" marker-end="url(#arrow)"/><rect x="306" y="226" width="74" height="28" fill="#eef2f7" stroke="#c9d3e0"/><text x="343.0" y="244" text-anchor="middle" font-size="11" font-weight="400" fill="currentColor" font-family="IBM Plex Mono, ui-monospace, monospace">alerts</text><polyline points="75,158 75,194" fill="none" stroke="currentColor" stroke-width="1.2" marker-end="url(#arrow)"/><text x="82" y="180" text-anchor="start" font-size="10.5" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">push</text><rect x="560" y="196" width="180" height="50" fill="#fff" stroke="currentColor" stroke-width="1"/><text x="650.0" y="218.0" text-anchor="middle" font-size="12" font-weight="600" fill="currentColor">container registry</text><text x="650.0" y="233.0" text-anchor="middle" font-size="10.5" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">orders/api:&lt;sha&gt;</text><line x1="392" y1="231" x2="558" y2="221" stroke="currentColor" stroke-width="1.2" marker-end="url(#arrow)"/><text x="475" y="214" text-anchor="middle" font-size="10.5" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">docker push :sha, :ring</text><rect x="20" y="316" width="370" height="70" fill="#fff" stroke="currentColor" stroke-width="1"/><text x="30" y="332" text-anchor="start" font-size="11" font-weight="600" fill="currentColor">fleet pipeline (runs only when triggered)</text><rect x="30" y="346" width="74" height="28" fill="#eef2f7" stroke="#c9d3e0"/><text x="67.0" y="364" text-anchor="middle" font-size="11" font-weight="400" fill="currentColor" font-family="IBM Plex Mono, ui-monospace, monospace">apply</text><line x1="105" y1="360" x2="115" y2="360" stroke="currentColor" stroke-width="1.2" marker-end="url(#arrow)"/><rect x="116" y="346" width="90" height="28" fill="#eef2f7" stroke="#c9d3e0"/><text x="161.0" y="364" text-anchor="middle" font-size="11" font-weight="400" fill="currentColor" font-family="IBM Plex Mono, ui-monospace, monospace">set image</text><line x1="207" y1="360" x2="217" y2="360" stroke="currentColor" stroke-width="1.2" marker-end="url(#arrow)"/><rect x="218" y="346" width="110" height="28" fill="#eef2f7" stroke="#c9d3e0"/><text x="273.0" y="364" text-anchor="middle" font-size="11" font-weight="400" fill="currentColor" font-family="IBM Plex Mono, ui-monospace, monospace">rollout status</text><polyline points="254,254 254,314" fill="none" stroke="#1d4e89" stroke-width="1.2" marker-end="url(#arrow-accent)"/><text x="262" y="282" text-anchor="start" font-size="10.5" fill="#1d4e89" font-family="IBM Plex Mono, ui-monospace, monospace">trigger</text><text x="262" y="296" text-anchor="start" font-size="10" font-weight="400" fill="#1d4e89" font-family="IBM Plex Mono, ui-monospace, monospace">ROLLOUT_SET · strategy: depend</text><rect x="560" y="306" width="180" height="40" fill="#fff" stroke="currentColor" stroke-width="1"/><text x="650.0" y="323.0" text-anchor="middle" font-size="12" font-weight="600" fill="currentColor">north</text><text x="650.0" y="338.0" text-anchor="middle" font-size="10.5" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">cluster · namespace per ring</text><rect x="560" y="362" width="180" height="40" fill="#fff" stroke="currentColor" stroke-width="1"/><text x="650.0" y="379.0" text-anchor="middle" font-size="12" font-weight="600" fill="currentColor">south</text><text x="650.0" y="394.0" text-anchor="middle" font-size="10.5" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">cluster · namespace per ring</text><line x1="392" y1="350" x2="558" y2="326" stroke="currentColor" stroke-width="1.2" marker-end="url(#arrow)"/><text x="470" y="330" text-anchor="middle" font-size="10.5" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">kubectl -n <ns></text><line x1="392" y1="362" x2="558" y2="382" stroke="currentColor" stroke-width="1.2" marker-end="url(#arrow)"/><polyline points="650,248 650,304" fill="none" stroke="currentColor" stroke-width="1.2" marker-end="url(#arrow)"/><text x="658" y="280" text-anchor="start" font-size="10.5" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">pull</text><text x="20" y="420" text-anchor="start" font-size="10.5" font-weight="400" fill="#5d6b7d">Dashed: a reference resolved at pipeline creation, not a run. Blue: the hand-off between the two pipelines.</text></svg><figcaption>Three kinds of repository, two pipelines. App repositories include the blueprint library; their pipeline bakes images and hands a rollout set to the fleet pipeline, which is the only thing that talks to the clusters.</figcaption></figure>

There are three kinds of repository and only two pipelines:

| Repository | Holds | Its pipeline |
|---|---|---|
| `platform/ci-blueprints` | The library: one folder per app, five YAML files each | None. It is only ever `include`d |
| `orders`, `billing`, … | The application code and a `.gitlab-ci.yml` of a dozen lines | Bakes images, releases, hands off to the fleet pipeline, alerts |
| `platform/fleet` | Kubernetes manifests, `<cluster>/<app>/<ring>/` | Runs only when triggered. Applies, sets images, waits for the rollout |

Nothing in an app repository knows how to reach a cluster. Nothing in the
fleet repository knows how to bake an image. The hand-off between them is a
single JSON variable, and that boundary is what keeps both sides simple.

## The consumer: a dozen lines

{{< snippet file="gitlab-ci-blueprints/orders.gitlab-ci.yml" lang="yaml" >}}

The `ref` is a tag. `main` is for trying a change in one app before you cut
`v2.4.0` and move the others. The file list is explicit on purpose: **the
names are a contract**. Adding a sixth file means every consumer adds a line;
renaming one means every consumer breaks — so files are added, never renamed.

The `SHIP_*` flags are how a new unit, or a new library version, rolls in one
piece at a time. A unit whose flag is off has no job at all, not a skipped one.

## From five files to a pipeline

<figure class="diagram"><svg viewBox="0 0 760 374" role="img" aria-label="Five blueprint files, included by a short consumer file, expand into a pipeline with three bake jobs, one release job, two delivery jobs and one alert job." xmlns="http://www.w3.org/2000/svg" font-family="IBM Plex Sans, system-ui, sans-serif" color="#16233a"><defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="currentColor"/></marker><marker id="arrow-accent" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#1d4e89"/></marker></defs><text x="20" y="20" text-anchor="start" font-size="11" font-weight="600" fill="currentColor">the library (blueprints/orders/)</text><rect x="20" y="30" width="180" height="48" fill="#eef2f7" stroke="currentColor" stroke-width="1"/><text x="110.0" y="51.0" text-anchor="middle" font-size="12" font-weight="600" fill="currentColor">routine.yml</text><text x="110.0" y="66.0" text-anchor="middle" font-size="10.5" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">stages · branch→ring · retry</text><rect x="20" y="94" width="180" height="48" fill="#eef2f7" stroke="currentColor" stroke-width="1"/><text x="110.0" y="115.0" text-anchor="middle" font-size="12" font-weight="600" fill="currentColor">images.yml</text><text x="110.0" y="130.0" text-anchor="middle" font-size="10.5" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">.bake hidden job</text><rect x="20" y="158" width="180" height="48" fill="#eef2f7" stroke="currentColor" stroke-width="1"/><text x="110.0" y="179.0" text-anchor="middle" font-size="12" font-weight="600" fill="currentColor">release.yml</text><text x="110.0" y="194.0" text-anchor="middle" font-size="10.5" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">digest, re-tag on main</text><rect x="20" y="222" width="180" height="48" fill="#eef2f7" stroke="currentColor" stroke-width="1"/><text x="110.0" y="243.0" text-anchor="middle" font-size="12" font-weight="600" fill="currentColor">delivery.yml</text><text x="110.0" y="258.0" text-anchor="middle" font-size="10.5" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">.deliver hidden job</text><rect x="20" y="286" width="180" height="48" fill="#eef2f7" stroke="currentColor" stroke-width="1"/><text x="110.0" y="307.0" text-anchor="middle" font-size="12" font-weight="600" fill="currentColor">alerts.yml</text><text x="110.0" y="322.0" text-anchor="middle" font-size="10.5" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">alert on failure / success</text><text x="250" y="20" text-anchor="start" font-size="11" font-weight="600" fill="currentColor">the consumer</text><rect x="250" y="30" width="150" height="304" fill="#fff" stroke="currentColor"/><text x="325" y="52" text-anchor="middle" font-size="11" font-weight="600" fill="currentColor">orders/.gitlab-ci.yml</text><text x="262" y="78" text-anchor="start" font-size="9.5" font-weight="400" fill="currentColor" font-family="IBM Plex Mono, ui-monospace, monospace">include:</text><text x="262" y="93" text-anchor="start" font-size="9.5" font-weight="400" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">  project: ci-blueprints</text><text x="262" y="108" text-anchor="start" font-size="9.5" font-weight="400" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">  ref: v2.3.0</text><text x="262" y="123" text-anchor="start" font-size="9.5" font-weight="400" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">  file:</text><text x="262" y="138" text-anchor="start" font-size="9.5" font-weight="400" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">    - routine.yml</text><text x="262" y="153" text-anchor="start" font-size="9.5" font-weight="400" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">    - images.yml</text><text x="262" y="168" text-anchor="start" font-size="9.5" font-weight="400" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">    - release.yml</text><text x="262" y="183" text-anchor="start" font-size="9.5" font-weight="400" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">    - delivery.yml</text><text x="262" y="198" text-anchor="start" font-size="9.5" font-weight="400" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">    - alerts.yml</text><text x="262" y="213" text-anchor="start" font-size="9.5" font-weight="400" fill="currentColor" font-family="IBM Plex Mono, ui-monospace, monospace">variables:</text><text x="262" y="228" text-anchor="start" font-size="9.5" font-weight="400" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">  SHIP_WORKER: &quot;true&quot;</text><text x="325" y="268" text-anchor="middle" font-size="10" font-weight="400" fill="#5d6b7d">four lines of include,</text><text x="325" y="283" text-anchor="middle" font-size="10" font-weight="400" fill="#5d6b7d">one variable block —</text><text x="325" y="312" text-anchor="middle" font-size="10" font-weight="400" fill="#1d4e89">nothing else.</text><line x1="202" y1="54.0" x2="248" y2="60" stroke="currentColor" stroke-width="1.2" stroke-dasharray="5 4" marker-end="url(#arrow)"/><line x1="202" y1="118.0" x2="248" y2="118.0" stroke="currentColor" stroke-width="1.2" stroke-dasharray="5 4" marker-end="url(#arrow)"/><line x1="202" y1="182.0" x2="248" y2="182.0" stroke="currentColor" stroke-width="1.2" stroke-dasharray="5 4" marker-end="url(#arrow)"/><line x1="202" y1="246.0" x2="248" y2="246.0" stroke="currentColor" stroke-width="1.2" stroke-dasharray="5 4" marker-end="url(#arrow)"/><line x1="202" y1="310.0" x2="248" y2="310.0" stroke="currentColor" stroke-width="1.2" stroke-dasharray="5 4" marker-end="url(#arrow)"/><text x="225" y="46" text-anchor="middle" font-size="10" font-weight="400" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">include</text><text x="470" y="20" text-anchor="start" font-size="11" font-weight="600" fill="currentColor">the pipeline that materialises</text><rect x="470" y="30" width="270" height="48" fill="#fff" stroke="#c9d3e0"/><text x="480" y="46" text-anchor="start" font-size="10" font-weight="400" fill="currentColor" font-family="IBM Plex Mono, ui-monospace, monospace">images · release · delivery · alerts</text><text x="480" y="60" text-anchor="start" font-size="10" font-weight="400" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">candidate → RING=preview</text><text x="480" y="72" text-anchor="start" font-size="10" font-weight="400" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">main      → RING=live</text><rect x="470" y="94" width="86" height="48" fill="#fff" stroke="currentColor" stroke-width="1"/><text x="513.0" y="115.0" text-anchor="middle" font-size="12" font-weight="400" fill="currentColor">bake_api</text><text x="513.0" y="130.0" text-anchor="middle" font-size="10.5" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">UNIT=api</text><rect x="562" y="94" width="86" height="48" fill="#fff" stroke="currentColor" stroke-width="1"/><text x="605.0" y="115.0" text-anchor="middle" font-size="12" font-weight="400" fill="currentColor">bake_web</text><text x="605.0" y="130.0" text-anchor="middle" font-size="10.5" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">UNIT=web</text><rect x="654" y="94" width="86" height="48" fill="#fff" stroke="currentColor" stroke-width="1" stroke-dasharray="5 4"/><text x="697.0" y="115.0" text-anchor="middle" font-size="12" font-weight="400" fill="currentColor">bake_worker</text><text x="697.0" y="130.0" text-anchor="middle" font-size="10.5" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">UNIT=worker</text><text x="740" y="154" text-anchor="end" font-size="10" font-weight="400" fill="#5d6b7d">parallel; worker only if SHIP_WORKER</text><rect x="470" y="158" width="130" height="48" fill="#fff" stroke="currentColor" stroke-width="1"/><text x="535.0" y="179.0" text-anchor="middle" font-size="12" font-weight="400" fill="currentColor">release</text><text x="535.0" y="194.0" text-anchor="middle" font-size="10.5" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">crane · dotenv</text><text x="740" y="186.0" text-anchor="end" font-size="10" font-weight="400" fill="#5d6b7d">one job, all units</text><rect x="470" y="222" width="130" height="48" fill="#fff" stroke="currentColor" stroke-width="1"/><text x="535.0" y="243.0" text-anchor="middle" font-size="12" font-weight="400" fill="currentColor">deliver_north</text><text x="535.0" y="258.0" text-anchor="middle" font-size="10.5" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">CLUSTER=north</text><rect x="610" y="222" width="130" height="48" fill="#fff" stroke="currentColor" stroke-width="1"/><text x="675.0" y="243.0" text-anchor="middle" font-size="12" font-weight="400" fill="currentColor">deliver_south</text><text x="675.0" y="258.0" text-anchor="middle" font-size="10.5" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">CLUSTER=south</text><text x="740" y="282" text-anchor="end" font-size="10" font-weight="400" fill="#5d6b7d">one trigger per cluster</text><rect x="470" y="286" width="130" height="48" fill="#fff" stroke="currentColor" stroke-width="1"/><text x="535.0" y="307.0" text-anchor="middle" font-size="12" font-weight="400" fill="currentColor">alert_failure</text><text x="535.0" y="322.0" text-anchor="middle" font-size="10.5" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">when: on_failure</text><line x1="402" y1="54.0" x2="468" y2="54.0" stroke="currentColor" stroke-width="1.2" marker-end="url(#arrow)"/><text x="435" y="46.0" text-anchor="middle" font-size="10.5" fill="#5d6b7d">expands to</text><line x1="402" y1="118.0" x2="468" y2="118.0" stroke="currentColor" stroke-width="1.2" marker-end="url(#arrow)"/><line x1="402" y1="182.0" x2="468" y2="182.0" stroke="currentColor" stroke-width="1.2" marker-end="url(#arrow)"/><line x1="402" y1="246.0" x2="468" y2="246.0" stroke="currentColor" stroke-width="1.2" marker-end="url(#arrow)"/><line x1="402" y1="310.0" x2="468" y2="310.0" stroke="currentColor" stroke-width="1.2" marker-end="url(#arrow)"/><text x="435" y="110.0" text-anchor="middle" font-size="9.5" font-weight="400" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">× 3 units</text><text x="435" y="238.0" text-anchor="middle" font-size="9.5" font-weight="400" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">× 2 clusters</text><text x="20" y="362" text-anchor="start" font-size="10.5" font-weight="400" fill="#5d6b7d">Dashed: a file pulled in by include. Dashed job: created only when its ship flag is set.</text></svg><figcaption>How five blueprint files become a concrete pipeline. Hidden jobs in the library are extended into one job per unit and one per cluster; the consumer's file only lists includes and flags.</figcaption></figure>

### routine.yml: what a branch means

{{< snippet file="gitlab-ci-blueprints/routine.yml" lang="yaml" >}}

Three decisions live here and nowhere else. **A branch maps to exactly one
ring**, and a branch that maps to nothing creates no pipeline — the `when:
never` at the end of the `workflow:` block is not decoration. **Retries cover
infrastructure and not code**: adding `script_failure` would rerun a genuinely
broken bake three times and hide the defect behind a green badge on the
fourth. And **the shell library is shared with `!reference`**, so the retry
with backoff and the three-state probe are written once. That third state
matters: a network flap during `kubectl get` used to look exactly like
"absent", and a job would carry on with the wrong assumption. Not being able
to tell is its own answer, and the caller stops on it.

### images.yml: one hidden job, one concrete job per unit

{{< snippet file="gitlab-ci-blueprints/images.yml" lang="yaml" >}}

The hidden job does the work; each concrete job is two variables. They run in
parallel, since nothing in `bake_web` depends on `bake_api`. Every image is
pushed twice: as `:<sha>`, which is what will be rolled out and never moves,
and as `:preview`, a floating pointer to "what the preview ring runs now" that
the release step will read.

### delivery.yml: the hand-off

{{< snippet file="gitlab-ci-blueprints/delivery.yml" lang="yaml" >}}

`strategy: depend` makes the parent wait for the child and fail if it fails —
the app pipeline's badge tells the truth about the rollout, not just the bake.
One delivery job per cluster is the whole multi-cluster story: same fleet
repository, same variables, different `CLUSTER`.

`ROLLOUT_SET` is the contract across the boundary: which unit, which
container name inside the pod, which image. The fleet side needs nothing else
to update a deployment.

## Live is a release, not a rebuild

<figure class="diagram"><svg viewBox="0 0 760 274" role="img" aria-label="Two lanes: the candidate branch bakes, pushes and rolls out to the preview ring; the main branch skips the bake, re-tags the preview digest as live and rolls that out." xmlns="http://www.w3.org/2000/svg" font-family="IBM Plex Sans, system-ui, sans-serif" color="#16233a"><defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="currentColor"/></marker><marker id="arrow-accent" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#1d4e89"/></marker></defs><text x="20" y="40" text-anchor="start" font-size="11" font-weight="600" fill="currentColor">branch candidate → preview ring</text><text x="20" y="170" text-anchor="start" font-size="11" font-weight="600" fill="currentColor">branch main → live ring</text><line x1="20" y1="126" x2="740" y2="126" stroke="#c9d3e0" stroke-dasharray="3 4"/><rect x="60" y="50" width="140" height="50" fill="#fff" stroke="currentColor" stroke-width="1"/><text x="130.0" y="72.0" text-anchor="middle" font-size="12" font-weight="600" fill="currentColor">bake</text><text x="130.0" y="87.0" text-anchor="middle" font-size="10.5" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">3 units</text><line x1="202" y1="75" x2="228" y2="75" stroke="currentColor" stroke-width="1.2" marker-end="url(#arrow)"/><rect x="230" y="50" width="140" height="50" fill="#fff" stroke="currentColor" stroke-width="1"/><text x="300.0" y="72.0" text-anchor="middle" font-size="12" font-weight="600" fill="currentColor">push</text><text x="300.0" y="87.0" text-anchor="middle" font-size="10.5" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">:&lt;sha&gt; · :preview</text><line x1="372" y1="75" x2="398" y2="75" stroke="currentColor" stroke-width="1.2" marker-end="url(#arrow)"/><rect x="400" y="50" width="140" height="50" fill="#fff" stroke="currentColor" stroke-width="1"/><text x="470.0" y="72.0" text-anchor="middle" font-size="12" font-weight="600" fill="currentColor">trigger</text><text x="470.0" y="87.0" text-anchor="middle" font-size="10.5" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">set :&lt;sha&gt;</text><line x1="542" y1="75" x2="568" y2="75" stroke="currentColor" stroke-width="1.2" marker-end="url(#arrow)"/><rect x="570" y="50" width="140" height="50" fill="#fff" stroke="currentColor" stroke-width="1"/><text x="640.0" y="72.0" text-anchor="middle" font-size="12" font-weight="600" fill="currentColor">roll out</text><text x="640.0" y="87.0" text-anchor="middle" font-size="10.5" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">preview</text><rect x="60" y="180" width="140" height="50" fill="#fff" stroke="currentColor" stroke-width="1" stroke-dasharray="5 4"/><text x="130.0" y="202.0" text-anchor="middle" font-size="12" font-weight="400" fill="#5d6b7d">no bake</text><text x="130.0" y="217.0" text-anchor="middle" font-size="10.5" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">stage skipped</text><rect x="230" y="180" width="140" height="50" fill="#fff" stroke="#1d4e89" stroke-width="1"/><text x="300.0" y="202.0" text-anchor="middle" font-size="12" font-weight="600" fill="#1d4e89">release</text><text x="300.0" y="217.0" text-anchor="middle" font-size="10.5" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">crane tag</text><rect x="400" y="180" width="140" height="50" fill="#fff" stroke="currentColor" stroke-width="1"/><text x="470.0" y="202.0" text-anchor="middle" font-size="12" font-weight="600" fill="currentColor">trigger</text><text x="470.0" y="217.0" text-anchor="middle" font-size="10.5" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">set @digest</text><rect x="570" y="180" width="140" height="50" fill="#fff" stroke="currentColor" stroke-width="1"/><text x="640.0" y="202.0" text-anchor="middle" font-size="12" font-weight="600" fill="currentColor">roll out</text><text x="640.0" y="217.0" text-anchor="middle" font-size="10.5" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">live</text><line x1="202" y1="205" x2="228" y2="205" stroke="currentColor" stroke-width="1.2" stroke-dasharray="5 4" marker-end="url(#arrow)"/><line x1="372" y1="205" x2="398" y2="205" stroke="currentColor" stroke-width="1.2" marker-end="url(#arrow)"/><line x1="542" y1="205" x2="568" y2="205" stroke="currentColor" stroke-width="1.2" marker-end="url(#arrow)"/><polyline points="300.0,102 300.0,178" fill="none" stroke="#1d4e89" stroke-width="1.2" marker-end="url(#arrow-accent)"/><text x="308.0" y="144" text-anchor="start" font-size="10.5" fill="#1d4e89" font-family="IBM Plex Mono, ui-monospace, monospace">same digest</text><text x="308.0" y="158" text-anchor="start" font-size="10" font-weight="400" fill="#1d4e89" font-family="IBM Plex Mono, ui-monospace, monospace">:preview → :live</text><text x="20" y="262" text-anchor="start" font-size="10.5" font-weight="400" fill="#5d6b7d">The live ring never bakes. It releases the image that already ran in preview, by digest, and rolls that out.</text></svg><figcaption>Preview bakes; live releases. The main branch re-tags the preview digest and rolls it out — the bytes that ran in preview are the bytes that go live.</figcaption></figure>

{{< snippet file="gitlab-ci-blueprints/release.yml" lang="yaml" >}}

The `main` branch skips the bake stage entirely. Rebuilding from the same
commit would *probably* produce the same image; releasing by digest produces
the same image by definition. The dotenv report is how the digests reach the
delivery jobs — GitLab expands `$API_IMAGE` inside `ROLLOUT_SET` before it
hands the variable to the child pipeline.

## The fleet pipeline

Manifests live per cluster, per app, per ring, with a `common/` folder for the
ConfigMap and Secret every unit reads. Namespaces follow one convention,
`<app>-<ring>`, so nobody has to declare them:

```text
platform/fleet/
└── north/
    └── orders/
        ├── common/
        │   ├── preview/      configmap.yaml  secret.yaml
        │   └── live/
        ├── preview/          api.yaml  web.yaml  worker.yaml
        └── live/
```

{{< snippet file="gitlab-ci-blueprints/fleet.gitlab-ci.yml" lang="yaml" >}}

Four things are doing the real work here.

**It only runs when triggered.** A push to the fleet repository changes files
and nothing else; the cluster changes when an app pipeline says so, with a
rollout set attached.

**`apply` and `set image` do not fight.** The versioned manifest says
`image: …/api:preview`; the live object ends up with `…/api@sha256:…`. The
next `apply` looks like it should revert that — it does not. Client-side apply
patches only the fields that changed between the last-applied manifest and
the new one, and the image line is identical in both, so the digest set by
the pipeline survives. Break that premise by editing the tag in the manifest
and you get a second rollout per delivery.

**`resource_group` serialises per target.** Two pipelines for the same app
and ring queue instead of racing. The group key includes the app so that
`orders` and `billing` on the same cluster still roll out in parallel.

**A failed rollout explains itself.** `describe` and the last hundred lines
of logs go into the job output before it exits red — the person who opens
the job at 2 a.m. should not need cluster access to see why.

## Telling someone

{{< snippet file="gitlab-ci-blueprints/alerts.yml" lang="yaml" >}}

On failure, always: branch, ring, author, commit, one button. On success, one
line from the rollout job with the digest that went live:

{{< snippet file="gitlab-ci-blueprints/alert-success.sh" lang="bash" >}}

The webhook URL is a masked, protected CI/CD variable on the consumer
project; a project without one simply logs that it skipped the alert.

## Where each setting lives

| Setting | Where | Why there |
|---|---|---|
| Branch → ring | `routine.yml` in the library | One truth for every app |
| Registry credentials | GitLab's own `CI_REGISTRY_*` | Never typed anywhere |
| Kubeconfig per cluster | File-type variable on `platform/fleet`, protected | Only the fleet pipeline can reach a cluster |
| `SLACK_WEBHOOK_URL` | Masked variable on each consumer | Each app owns its channel |
| `SHIP_<UNIT>` | `variables:` in the consumer's file | Visible in the diff that turns a unit on |
| Library version | `ref:` in the consumer's `include` | Upgrades are a reviewed commit, not a surprise |

## What bit us, so it does not bite you

| Symptom | Cause | Rule |
|---|---|---|
| Rollout green, image unchanged | New unit added to `images.yml` and `ROLLOUT_SET` but the manifest lacks the `unit:` label, so `set image -l` matched nothing | Adding a unit touches **three** places: bake job, rollout-set entry, manifest label |
| Five units rolling out one after another | `resource_group` without the app in its key | The key names exactly what must not overlap |
| A failed command, no error, job continues | `OUT=$(cmd 2>&1)` under `set -e`: the assignment swallows the exit status | Use the command as the condition of an `if`, capture output inside |
| A flaky bake "fixed" by retry | `script_failure` in `default.retry` | Retry infrastructure, never code |
| A step skipped because a Deployment "was absent" — it was not | Network flap indistinguishable from `NotFound` | Three states, stop on the third |
| Clone of a 30 MB repo to run `kubectl apply` | Default `GIT_STRATEGY` on a job that never reads the tree | `GIT_STRATEGY: none` when the working tree is not needed |

None of this is exotic GitLab. It is `include`, hidden jobs, `workflow:`
rules, one multi-project trigger and a JSON variable — arranged so that adding
the fourth app is a folder in the library and a dozen lines in the app, and so
that the live ring only ever runs bytes that preview already ran.
