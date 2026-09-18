---
title: "Hexagonal architecture where it pays: how DOP keeps vendors behind ports"
date: 2026-09-18T08:00:00-04:00
draft: false
translationKey: "hexagonal-architecture-dop"
categories: ["Technology"]
tags: ["dop", "hexagonal-architecture", "go", "architecture-decisions", "cloud"]
description: "DOP's core runs on Cloud Run and on a k3s cluster with no change to the domain. What makes that true is not the folder layout: two adapters per port from day one, one contract suite every adapter passes, and a test that breaks the build when the domain imports infrastructure — with the code."
---

DOP's core has to run in two places that agree on nothing. On Google Cloud
Run, a secret lives in Secret Manager and identity comes from Firebase. On a
k3s cluster, a secret is a Kubernetes Secret and identity comes from whatever
OIDC provider the cluster has. Add the list that grows with the product —
object storage, a message broker, the executor that runs an agent's sandbox,
the git host that receives the pull request — and coupling the domain to any
one of them would mean a rewrite per environment.

Hexagonal architecture — ports and adapters — is the textbook answer. It is
also the pattern that most often ends as the name of a folder: an
`interfaces/` package, one implementation per interface, and a domain that
still knows what a bucket is. This article is about the version of it that
[DOP](https://dop-t.com/) runs: where hexagonal was worth it, what it costs,
and the three disciplines that keep it from decaying. The code is real — the
snippets come from `dop-core`, the platform's Go core, trimmed for reading.

## The shape

<figure class="diagram"><svg viewBox="0 0 760 432" role="img" aria-label="The BFF and the CLI reach the domain hexagon through a gRPC edge; on the other side, infrastructure ports chosen at boot and domain provider ports chosen per request each list their adapters; a composition root band underneath wires both ends." xmlns="http://www.w3.org/2000/svg" font-family="IBM Plex Sans, system-ui, sans-serif" color="#16233a"><defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="currentColor"/></marker><marker id="arrow-accent" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#1d4e89"/></marker></defs><text x="20" y="30" text-anchor="start" font-size="11" font-weight="600" fill="currentColor">who drives the domain</text><rect x="20" y="60" width="140" height="46" fill="#fff" stroke="currentColor" stroke-width="1"/><text x="90.0" y="80.0" text-anchor="middle" font-size="12" font-weight="600" fill="currentColor">dop-api</text><text x="90.0" y="95.0" text-anchor="middle" font-size="10.5" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">Python BFF · REST+SSE</text><rect x="20" y="122" width="140" height="46" fill="#fff" stroke="currentColor" stroke-width="1"/><text x="90.0" y="142.0" text-anchor="middle" font-size="12" font-weight="600" fill="currentColor">dop-cmd</text><text x="90.0" y="157.0" text-anchor="middle" font-size="10.5" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">CLI · v0.7.1</text><rect x="190" y="60" width="80" height="108" fill="#eef2f7" stroke="currentColor" stroke-width="1"/><text x="230.0" y="118.0" text-anchor="middle" font-size="12" font-weight="600" fill="currentColor">gRPC edge</text><text x="230" y="154" text-anchor="middle" font-size="9" font-weight="400" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">internal/app/grpc</text><line x1="162" y1="83" x2="188" y2="90" stroke="currentColor" stroke-width="1.2" marker-end="url(#arrow)"/><text x="175" y="72" text-anchor="middle" font-size="10.5" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">gRPC</text><line x1="162" y1="145" x2="188" y2="138" stroke="currentColor" stroke-width="1.2" marker-end="url(#arrow)"/><line x1="272" y1="114" x2="296" y2="114" stroke="currentColor" stroke-width="1.2" marker-end="url(#arrow)"/><polygon points="320,40 450,40 474,190 450,340 320,340 296,190" fill="#eef2f7" stroke="currentColor" stroke-width="1.2"/><text x="385" y="70" text-anchor="middle" font-size="12" font-weight="600" fill="currentColor">internal/domain</text><text x="385" y="86" text-anchor="middle" font-size="10" font-weight="400" fill="#5d6b7d">model · use cases · ports</text><text x="385" y="116" text-anchor="middle" font-size="10.5" font-weight="400" fill="currentColor" font-family="IBM Plex Mono, ui-monospace, monospace">demand</text><text x="385" y="133" text-anchor="middle" font-size="10.5" font-weight="400" fill="currentColor" font-family="IBM Plex Mono, ui-monospace, monospace">delivery</text><text x="385" y="150" text-anchor="middle" font-size="10.5" font-weight="400" fill="currentColor" font-family="IBM Plex Mono, ui-monospace, monospace">execution</text><text x="385" y="167" text-anchor="middle" font-size="10.5" font-weight="400" fill="currentColor" font-family="IBM Plex Mono, ui-monospace, monospace">resource</text><text x="385" y="184" text-anchor="middle" font-size="10.5" font-weight="400" fill="currentColor" font-family="IBM Plex Mono, ui-monospace, monospace">identity</text><text x="385" y="201" text-anchor="middle" font-size="10.5" font-weight="400" fill="currentColor" font-family="IBM Plex Mono, ui-monospace, monospace">event</text><text x="385" y="218" text-anchor="middle" font-size="10.5" font-weight="400" fill="currentColor" font-family="IBM Plex Mono, ui-monospace, monospace">workflow</text><text x="385" y="235" text-anchor="middle" font-size="10.5" font-weight="400" fill="currentColor" font-family="IBM Plex Mono, ui-monospace, monospace">…</text><text x="385" y="264" text-anchor="middle" font-size="10" font-weight="600" fill="#1d4e89">the PORTS</text><text x="385" y="278" text-anchor="middle" font-size="9.5" font-weight="400" fill="#1d4e89">in the domain's language</text><text x="385" y="292" text-anchor="middle" font-size="9" font-weight="400" fill="#1d4e89" font-family="IBM Plex Mono, ui-monospace, monospace">domain/ports</text><text x="385" y="304" text-anchor="middle" font-size="9" font-weight="400" fill="#1d4e89" font-family="IBM Plex Mono, ui-monospace, monospace">delivery.GitProvider …</text><text x="500" y="30" text-anchor="start" font-size="11" font-weight="600" fill="currentColor">what the domain drives</text><text x="500" y="56" text-anchor="start" font-size="10" font-weight="600" fill="#1d4e89">infrastructure — chosen at boot, one active</text><circle cx="455" cy="70" r="3" fill="#1d4e89"/><text x="500" y="74" text-anchor="start" font-size="10.5" font-weight="400" fill="currentColor" font-family="IBM Plex Mono, ui-monospace, monospace">SecretStore</text><text x="740" y="74" text-anchor="end" font-size="10" font-weight="400" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">memory · k8s · gcp</text><circle cx="458" cy="90" r="3" fill="#1d4e89"/><text x="500" y="94" text-anchor="start" font-size="10.5" font-weight="400" fill="currentColor" font-family="IBM Plex Mono, ui-monospace, monospace">EventBus</text><text x="740" y="94" text-anchor="end" font-size="10" font-weight="400" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">memory · nats</text><circle cx="461" cy="110" r="3" fill="#1d4e89"/><text x="500" y="114" text-anchor="start" font-size="10.5" font-weight="400" fill="currentColor" font-family="IBM Plex Mono, ui-monospace, monospace">IdentityProvider</text><text x="740" y="114" text-anchor="end" font-size="10" font-weight="400" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">firebase · oidc</text><circle cx="464" cy="130" r="3" fill="#1d4e89"/><text x="500" y="134" text-anchor="start" font-size="10.5" font-weight="400" fill="currentColor" font-family="IBM Plex Mono, ui-monospace, monospace">ObjectStore</text><text x="740" y="134" text-anchor="end" font-size="10" font-weight="400" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">fs · gcs</text><circle cx="468" cy="150" r="3" fill="#1d4e89"/><text x="500" y="154" text-anchor="start" font-size="10.5" font-weight="400" fill="currentColor" font-family="IBM Plex Mono, ui-monospace, monospace">SandboxLauncher</text><text x="740" y="154" text-anchor="end" font-size="10" font-weight="400" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">docker · k8s</text><circle cx="471" cy="170" r="3" fill="#1d4e89"/><text x="500" y="174" text-anchor="start" font-size="10.5" font-weight="400" fill="currentColor" font-family="IBM Plex Mono, ui-monospace, monospace">repositories</text><text x="740" y="174" text-anchor="end" font-size="10" font-weight="400" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">postgres</text><text x="500" y="212" text-anchor="start" font-size="10" font-weight="600" fill="#1d4e89">domain providers — per request, several active</text><circle cx="468" cy="226" r="3" fill="#1d4e89"/><text x="500" y="230" text-anchor="start" font-size="10.5" font-weight="400" fill="currentColor" font-family="IBM Plex Mono, ui-monospace, monospace">GitProvider</text><text x="740" y="230" text-anchor="end" font-size="10" font-weight="400" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">github · gitlab</text><circle cx="465" cy="246" r="3" fill="#1d4e89"/><text x="500" y="250" text-anchor="start" font-size="10.5" font-weight="400" fill="currentColor" font-family="IBM Plex Mono, ui-monospace, monospace">AgentProvider</text><text x="740" y="250" text-anchor="end" font-size="10" font-weight="400" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">anthropic · openai</text><circle cx="462" cy="266" r="3" fill="#1d4e89"/><text x="500" y="270" text-anchor="start" font-size="10.5" font-weight="400" fill="currentColor" font-family="IBM Plex Mono, ui-monospace, monospace">Mailer</text><text x="740" y="270" text-anchor="end" font-size="10" font-weight="400" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">smtp · sendgrid</text><circle cx="459" cy="286" r="3" fill="#1d4e89"/><text x="500" y="290" text-anchor="start" font-size="10.5" font-weight="400" fill="currentColor" font-family="IBM Plex Mono, ui-monospace, monospace">SMSer</text><text x="740" y="290" text-anchor="end" font-size="10" font-weight="400" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">twilio · zenvia</text><text x="500" y="318" text-anchor="start" font-size="9.5" font-weight="400" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">internal/adapter/<technology></text><text x="500" y="332" text-anchor="start" font-size="10" font-weight="400" fill="#5d6b7d">one package per vendor</text><rect x="20" y="364" width="720" height="34" fill="#fff" stroke="currentColor" stroke-dasharray="5 4"/><text x="30" y="385" text-anchor="start" font-size="11" font-weight="600" fill="currentColor" font-family="IBM Plex Mono, ui-monospace, monospace">internal/app</text><text x="122" y="385" text-anchor="start" font-size="10.5" font-weight="400" fill="#5d6b7d">the composition root: the only place that knows both ends — a config value picks the adapter for each port</text><text x="20" y="420" text-anchor="start" font-size="10.5" font-weight="400" fill="#5d6b7d">Left: driving adapters reach the domain through gRPC. Right: each port's adapters. Blue dot: a port on the hexagon's edge.</text></svg><figcaption>The three regions of dop-core. The domain declares the ports; the adapters implement them one technology per package; the composition root wires them by configuration. The two families on the right have opposite life cycles.</figcaption></figure>

Three regions. `internal/domain` owns the model and declares the ports — the
vault, the identity provider, the event bus, the executor, the repositories —
in its own vocabulary. `internal/adapter` holds one package per technology:
Secret Manager and a Kubernetes Secret behind the same interface, NATS
JetStream and an in-memory bus behind another, GitHub and GitLab behind a
third. `internal/app` is the composition root: the only place that knows both
ends, where a configuration value picks which adapter fills which port. On
the other side, the gRPC server is the driving adapter; the Python BFF and
the CLI reach the domain through it and through nothing else.

None of that is new. What matters is a distinction the diagram makes and most
hexagonal codebases do not.

## Two families of ports

| | Infrastructure ports | Domain provider ports |
|---|---|---|
| Examples | `SecretStore`, `IdentityProvider`, `ObjectStore`, `EventBus`, repositories | `GitProvider`, `AgentProvider`, `Mailer` |
| Who chooses | The deployment environment | The account's configuration |
| When | Once, at boot | On every request |
| How many active | One | Several at the same time |

They look alike — a Go interface, N implementations — and have opposite life
cycles. An infrastructure port is chosen by the deployment: once, at boot,
one adapter active for the life of the process. A domain provider port is
chosen by the account's data: on every request, several adapters active at
once, because one workspace has a repository on GitHub and another on GitLab
and both have to work. Confusing the two is this design's typical mistake — a
git provider picked by an environment variable works on the demo and fails,
silently, on the first customer with two hosts. The git provider section
below shows what the per-request family looks like in code.

## A port in the domain's language

{{< snippet file="hexagonal-dop/ports_secretstore.go" lang="go" >}}

Four verbs. `SecretRef` is opaque on purpose: the domain never sees a path in
Secret Manager or a namespace in Kubernetes. `SecretValue` cannot print
itself, which is how guarantee 6 survives a careless `%v`. And the guarantees
are written on the port, numbered, because they are what the contract suite
tests — the interface says what the methods are; the comment says what they
promise.

Notice what is not there: versions. Secret Manager has them, a Kubernetes
Secret does not, and a capability that does not map across adapters stays out
of the port. If it is ever needed it comes in as an optional capability the
domain never assumes.

The use case on the other side of the port knows exactly this much:

{{< snippet file="hexagonal-dop/resource_set_credential.go" lang="go" >}}

The domain builds a reference from its own identifiers and calls `Put`. It
orders the vault before the row for a reason it writes down, and it knows
nothing about where the bytes go.

## Two adapters from day one

The first discipline: a port with a single adapter is a guess, and it comes
out shaped like the vendor that inspired it. So the local adapter is not "for
later" — it is written with the port, and it is the proof that the port is
right.

{{< snippet file="hexagonal-dop/secretstore_memory.go" lang="go" >}}

Fifty lines, and it is not a mock: it copies bytes in and out so a caller
cannot mutate the vault by accident, and it passes exactly the same tests as
the GCP one. The in-memory event bus is the same story with more at stake —
it delivers in a goroutine, with backoff, an attempt cap and the same
poison-message policy as JetStream, because a double that delivered
synchronously and perfectly would hide the bugs that only show up with
asynchronous delivery.

The composition root picks between them by configuration:

{{< snippet file="hexagonal-dop/wire.go" lang="go" >}}

`Deps` holds ports, never concrete types, and that `switch` is the only
conditional on a backend in the whole codebase. This is what "chosen at boot,
one active" looks like.

## The contract suite is what makes it true

The second discipline. Two adapters that each pass their own tests are two
adapters; two adapters that pass the *same* tests are substitutable. DOP
keeps one suite per port under `test/contract`, written against the port's
numbered guarantees:

{{< snippet file="hexagonal-dop/contract_secretstore.go" lang="go" >}}

The comment at the top records the trap. The first version of this suite
used fixed account names and passed — against the in-memory double, where
every subtest gets a fresh vault. Against a real backend the same vault
persists between subtests, and the secret left behind by subtest 1 broke
subtest 5. The suite had been written on top of the double and carried an
assumption only the double satisfied; no real adapter would pass, and none
was being run. Unique identifiers per run fixed the suite. Running it against
the real thing is what found the bug — which is the point of the next file:

{{< snippet file="hexagonal-dop/contract_secretstore_test.go" lang="go" >}}

<figure class="diagram"><svg viewBox="0 0 760 318" role="img" aria-label="The SecretStore contract suite fans out to three adapters, memory always, k8s when a cluster answers, GCP behind a build tag; below, two crossed-out arrows show that the domain may not import adapters and adapters' SDKs may not reach the domain." xmlns="http://www.w3.org/2000/svg" font-family="IBM Plex Sans, system-ui, sans-serif" color="#16233a"><defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="currentColor"/></marker><marker id="arrow-accent" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#1d4e89"/></marker></defs><rect x="20" y="40" width="190" height="70" fill="#eef2f7" stroke="currentColor" stroke-width="1"/><text x="115.0" y="72.0" text-anchor="middle" font-size="12" font-weight="600" fill="currentColor">SecretStoreSuite</text><text x="115.0" y="87.0" text-anchor="middle" font-size="10.5" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">the six numbered guarantees</text><text x="115" y="124" text-anchor="middle" font-size="9.5" font-weight="400" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">test/contract/secretstore.go</text><rect x="300" y="30" width="150" height="38" fill="#fff" stroke="currentColor" stroke-width="1"/><text x="375.0" y="46.0" text-anchor="middle" font-size="12" font-weight="400" fill="currentColor">memory</text><text x="375.0" y="61.0" text-anchor="middle" font-size="10.5" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">go test ./...</text><line x1="212" y1="75" x2="298" y2="49" stroke="currentColor" stroke-width="1.2" marker-end="url(#arrow)"/><text x="460" y="53" text-anchor="start" font-size="10.5" font-weight="400" fill="#5d6b7d">always</text><rect x="300" y="76" width="150" height="38" fill="#fff" stroke="currentColor" stroke-width="1"/><text x="375.0" y="92.0" text-anchor="middle" font-size="12" font-weight="400" fill="currentColor">k8s</text><text x="375.0" y="107.0" text-anchor="middle" font-size="10.5" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">-run SecretStore</text><line x1="212" y1="75" x2="298" y2="95" stroke="currentColor" stroke-width="1.2" marker-end="url(#arrow)"/><text x="460" y="99" text-anchor="start" font-size="10.5" font-weight="400" fill="#5d6b7d">when a cluster answers</text><rect x="300" y="122" width="150" height="38" fill="#fff" stroke="currentColor" stroke-width="1" stroke-dasharray="5 4"/><text x="375.0" y="138.0" text-anchor="middle" font-size="12" font-weight="400" fill="currentColor">gcp</text><text x="375.0" y="153.0" text-anchor="middle" font-size="10.5" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">-tags=integration</text><line x1="212" y1="75" x2="298" y2="141" stroke="currentColor" stroke-width="1.2" marker-end="url(#arrow)"/><text x="460" y="145" text-anchor="start" font-size="10.5" font-weight="400" fill="#5d6b7d">when a credential exists (emulator or real GCP)</text><text x="300" y="172" text-anchor="start" font-size="10.5" font-weight="400" fill="#1d4e89">one function, three targets: substitutability in fact, not in intention</text><line x1="20" y1="192" x2="740" y2="192" stroke="#c9d3e0" stroke-dasharray="3 4"/><text x="20" y="214" text-anchor="start" font-size="11" font-weight="600" fill="currentColor">two tests guard the frontier on every go test ./...</text><rect x="20" y="226" width="150" height="40" fill="#eef2f7" stroke="currentColor" stroke-width="1"/><text x="95.0" y="243.0" text-anchor="middle" font-size="12" font-weight="600" fill="currentColor">internal/domain</text><text x="95.0" y="258.0" text-anchor="middle" font-size="10.5" fill="#5d6b7d">declares the ports</text><rect x="320" y="226" width="150" height="40" fill="#fff" stroke="currentColor" stroke-width="1"/><text x="395.0" y="243.0" text-anchor="middle" font-size="12" font-weight="600" fill="currentColor">internal/adapter</text><text x="395.0" y="258.0" text-anchor="middle" font-size="10.5" fill="#5d6b7d">implements them</text><rect x="590" y="226" width="150" height="40" fill="#fff" stroke="currentColor" stroke-width="1"/><text x="665.0" y="243.0" text-anchor="middle" font-size="12" font-weight="600" fill="currentColor">vendor SDKs</text><text x="665.0" y="258.0" text-anchor="middle" font-size="10.5" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">pgx · nats · gcp · k8s</text><line x1="172" y1="246" x2="318" y2="246" stroke="#1d4e89" stroke-width="1.2" stroke-dasharray="5 4" marker-end="url(#arrow-accent)"/><text x="245" y="240" text-anchor="middle" font-size="14" font-weight="700" fill="#1d4e89">✕</text><line x1="472" y1="246" x2="588" y2="246" stroke="#1d4e89" stroke-width="1.2" stroke-dasharray="5 4" marker-end="url(#arrow-accent)"/><text x="530" y="240" text-anchor="middle" font-size="14" font-weight="700" fill="#1d4e89">✕</text><text x="20" y="290" text-anchor="start" font-size="10.5" font-weight="400" fill="#5d6b7d">TestTheDomainDoesNotImportInfrastructure: no file under internal/domain imports an adapter or a vendor SDK.</text><text x="20" y="305" text-anchor="start" font-size="10.5" font-weight="400" fill="#5d6b7d">TestOnlyAppKnowsTheAdapters: outside internal/app, nothing imports internal/adapter.</text></svg><figcaption>What makes the pattern true over time: one contract suite that every adapter passes, and two import tests that break the build when the frontier is crossed.</figcaption></figure>

Same function, three targets: the in-memory adapter always, Kubernetes when
a cluster answers, Secret Manager behind a build tag when a credential
exists. The warning above the GCP test is earned: the emulator is more
permissive than Google in nine documented points, and one of them is the
port's first guarantee.

## When the adapter cannot keep the promise, the adapter pays

`SecretStore` promises read-after-write. The promise was born from the
Kubernetes adapter, where it holds — provided the adapter reads through the
API and not through a mounted volume, which the kubelet syncs about once a
minute. The GCP adapter could not keep it as written. Google is explicit that
only a read *by version number* is strongly consistent, while the `latest`
alias converges "typically within minutes, but may take a few hours". And
`SecretRef` is flat; there is nowhere to keep a version.

The failure mode is the worst one a vault can have. On real GCP a `Get`
right after a `Put` could return `(nil, nil)` — which through the port means
"it does not exist". A credential just written would look absent, silently,
and the caller would conclude the integration was never configured. In the
emulator the same case passes in ten milliseconds.

<figure class="diagram"><svg viewBox="0 0 760 396" role="img" aria-label="Two lanes for SecretStore.Put: the in-memory adapter writes a map and returns; the GCP adapter adds a version, confirms it by number, waits for the latest alias with backoff, destroys older versions and returns, or refuses with KindUnavailable past the ceiling." xmlns="http://www.w3.org/2000/svg" font-family="IBM Plex Sans, system-ui, sans-serif" color="#16233a"><defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="currentColor"/></marker><marker id="arrow-accent" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#1d4e89"/></marker></defs><rect x="20" y="20" width="200" height="46" fill="#eef2f7" stroke="currentColor" stroke-width="1"/><text x="120.0" y="40.0" text-anchor="middle" font-size="12" font-weight="600" fill="currentColor">SecretStore.Put</text><text x="120.0" y="55.0" text-anchor="middle" font-size="10.5" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">promise: read-after-write</text><text x="20" y="100" text-anchor="start" font-size="11" font-weight="600" fill="currentColor">in-memory adapter</text><rect x="20" y="110" width="130" height="40" fill="#fff" stroke="currentColor" stroke-width="1"/><text x="85.0" y="134.0" text-anchor="middle" font-size="12" font-weight="400" fill="currentColor">map[key] = copy</text><line x1="152" y1="130" x2="188" y2="130" stroke="currentColor" stroke-width="1.2" marker-end="url(#arrow)"/><rect x="190" y="110" width="90" height="40" fill="#fff" stroke="currentColor" stroke-width="1"/><text x="235.0" y="134.0" text-anchor="middle" font-size="12" font-weight="400" fill="currentColor">return nil</text><text x="300" y="134" text-anchor="start" font-size="10.5" font-weight="400" fill="#5d6b7d">the promise is free here</text><line x1="20" y1="168" x2="740" y2="168" stroke="#c9d3e0" stroke-dasharray="3 4"/><text x="20" y="192" text-anchor="start" font-size="11" font-weight="600" fill="currentColor">GCP Secret Manager adapter</text><rect x="20" y="204" width="130" height="48" fill="#fff" stroke="currentColor" stroke-width="1"/><text x="85.0" y="225.0" text-anchor="middle" font-size="12" font-weight="400" fill="currentColor">AddSecretVersion</text><text x="85.0" y="240.0" text-anchor="middle" font-size="10.5" fill="#5d6b7d">version n created</text><line x1="152" y1="228" x2="168" y2="228" stroke="currentColor" stroke-width="1.2" marker-end="url(#arrow)"/><rect x="170" y="204" width="130" height="48" fill="#fff" stroke="currentColor" stroke-width="1"/><text x="235.0" y="225.0" text-anchor="middle" font-size="12" font-weight="400" fill="currentColor">confirm v=n</text><text x="235.0" y="240.0" text-anchor="middle" font-size="10.5" fill="#5d6b7d">by number: strong</text><line x1="302" y1="228" x2="318" y2="228" stroke="currentColor" stroke-width="1.2" marker-end="url(#arrow)"/><rect x="320" y="204" width="130" height="48" fill="#fff" stroke="#1d4e89" stroke-width="1"/><text x="385.0" y="225.0" text-anchor="middle" font-size="12" font-weight="400" fill="currentColor">await latest ≥ n</text><text x="385.0" y="240.0" text-anchor="middle" font-size="10.5" fill="#5d6b7d">alias: eventual</text><line x1="452" y1="228" x2="468" y2="228" stroke="currentColor" stroke-width="1.2" marker-end="url(#arrow)"/><rect x="470" y="204" width="130" height="48" fill="#fff" stroke="currentColor" stroke-width="1"/><text x="535.0" y="225.0" text-anchor="middle" font-size="12" font-weight="400" fill="currentColor">destroyOlder</text><text x="535.0" y="240.0" text-anchor="middle" font-size="10.5" fill="#5d6b7d">old material gone</text><line x1="602" y1="228" x2="618" y2="228" stroke="currentColor" stroke-width="1.2" marker-end="url(#arrow)"/><rect x="620" y="204" width="120" height="48" fill="#fff" stroke="currentColor" stroke-width="1"/><text x="680.0" y="232.0" text-anchor="middle" font-size="12" font-weight="400" fill="currentColor">return nil</text><polyline points="340,254 340,272 326,272 326,256" fill="none" stroke="#1d4e89" stroke-width="1.2" marker-end="url(#arrow-accent)"/><text x="350" y="276" text-anchor="start" font-size="9.5" font-weight="400" fill="#1d4e89" font-family="IBM Plex Mono, ui-monospace, monospace">retry · 25 ms → 1 s backoff · ≤ SECRET_PROPAGATION_SECONDS</text><polyline points="430,254 430,298" fill="none" stroke="#1d4e89" stroke-width="1.2" stroke-dasharray="5 4" marker-end="url(#arrow-accent)"/><rect x="355" y="300" width="150" height="40" fill="#fff" stroke="#1d4e89" stroke-width="1"/><text x="430.0" y="317.0" text-anchor="middle" font-size="12" font-weight="600" fill="#1d4e89">KindUnavailable</text><text x="430.0" y="332.0" text-anchor="middle" font-size="10.5" fill="#5d6b7d">past the ceiling</text><text x="515" y="316" text-anchor="start" font-size="9.5" font-weight="400" fill="#5d6b7d">write accepted, read-after-write not confirmed:</text><text x="515" y="330" text-anchor="start" font-size="9.5" font-weight="400" fill="#5d6b7d">an error somebody reads, not a Get saying "absent".</text><text x="20" y="384" text-anchor="start" font-size="10.5" font-weight="400" fill="#5d6b7d">Blue: the step that exists only because the vendor's alias is eventually consistent. Dashed: the way out when it does not converge.</text></svg><figcaption>The same Put through two adapters. In memory the promise costs nothing; on Secret Manager the adapter confirms by version number, waits for the alias, and refuses rather than lie.</figcaption></figure>

Three ways out were on the table. Loosening the guarantee to "eventually
consistent" pushes a reread loop onto every caller, and the caller cannot
tell "not yet" from "never". Caching the value in the process after the
`Put` creates a second place where a credential exists, with its own
invalidation — it trades a consistency problem for a security one. Reading
by version number is the strongly consistent path, but it needs `Put` to
return an identifier the caller keeps; that changes the port, not an adapter,
and it is recorded as a possible evolution rather than rejected.

The decision was that the guarantee holds and the adapter pays:

{{< snippet file="hexagonal-dop/secretstore_gcp_await.go" lang="go" >}}

Confirm the write by version number, then wait for `latest` to catch up
under a ceiling, and if it does not converge, refuse with an explicit error.
Refusing is the part that matters: a `Put` that returns success while the
following `Get` says "not found" produces a silently broken integration; a
`Put` that fails produces an error somebody reads. The residue is written
down too — a `Put` on GCP is slower and can fail on non-convergence,
behaviour the emulator never reproduces, so the local test does not cover
that path.

This is the moment hexagonal earns its keep. The domain never learned that
Secret Manager has an alias, the use case did not change a line, and the
place where the vendor's semantics were absorbed is one function in one
adapter.

## The per-request family: the git provider

A pull request goes to whichever host the repository lives on, and the token
that opens it belongs to the account's integration. The delivery domain
declares what it needs and who resolves it:

{{< snippet file="hexagonal-dop/delivery_gitprovider.go" lang="go" >}}

Two interfaces. `GitProvider` is the delivery domain's vocabulary — open,
rebase, merge, and whether the host has a merge queue of its own that DOP's
queue can orchestrate on top of. `GitProviders` resolves which one serves a
given repository. The resolver is implemented in the composition root,
because that is the only place allowed to know all three ends:

{{< snippet file="hexagonal-dop/app_gitproviders.go" lang="go" >}}

<figure class="diagram"><svg viewBox="0 0 760 278" role="img" aria-label="The delivery domain calls For with account and repo; inside the composition root the repository gives the integration, the integration gives the provider, the vault gives the token; a GitHub or GitLab adapter is returned per call." xmlns="http://www.w3.org/2000/svg" font-family="IBM Plex Sans, system-ui, sans-serif" color="#16233a"><defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="currentColor"/></marker><marker id="arrow-accent" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#1d4e89"/></marker></defs><rect x="20" y="60" width="170" height="60" fill="#eef2f7" stroke="currentColor" stroke-width="1"/><text x="105.0" y="87.0" text-anchor="middle" font-size="12" font-weight="600" fill="currentColor">domain/delivery</text><text x="105.0" y="102.0" text-anchor="middle" font-size="10.5" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">PRs · rebase · merge</text><line x1="192" y1="90" x2="208" y2="90" stroke="currentColor" stroke-width="1.2" marker-end="url(#arrow)"/><text x="105" y="138" text-anchor="middle" font-size="10" font-weight="400" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">→ For(account, repo)</text><rect x="210" y="20" width="330" height="150" fill="#fff" stroke="currentColor" stroke-dasharray="5 4"/><text x="220" y="38" text-anchor="start" font-size="11" font-weight="600" fill="currentColor" font-family="IBM Plex Mono, ui-monospace, monospace">internal/app · gitProviders.For</text><rect x="224" y="52" width="92" height="40" fill="#fff" stroke="currentColor" stroke-width="1"/><text x="270.0" y="69.0" text-anchor="middle" font-size="12" font-weight="400" fill="currentColor">1 · repo</text><text x="270.0" y="84.0" text-anchor="middle" font-size="10.5" fill="#5d6b7d">→ integration id</text><line x1="318" y1="72" x2="336" y2="72" stroke="currentColor" stroke-width="1.2" marker-end="url(#arrow)"/><rect x="338" y="52" width="92" height="40" fill="#fff" stroke="currentColor" stroke-width="1"/><text x="384.0" y="69.0" text-anchor="middle" font-size="12" font-weight="400" fill="currentColor">2 · integration</text><text x="384.0" y="84.0" text-anchor="middle" font-size="10.5" fill="#5d6b7d">→ provider</text><line x1="432" y1="72" x2="450" y2="72" stroke="currentColor" stroke-width="1.2" marker-end="url(#arrow)"/><rect x="452" y="52" width="78" height="40" fill="#fff" stroke="currentColor" stroke-width="1"/><text x="491.0" y="69.0" text-anchor="middle" font-size="12" font-weight="400" fill="currentColor">3 · vault</text><text x="491.0" y="84.0" text-anchor="middle" font-size="10.5" fill="#5d6b7d">→ token</text><text x="360" y="122" text-anchor="middle" font-size="10" font-weight="400" fill="#1d4e89">resolved on EVERY request: two hosts, both work</text><text x="360" y="152" text-anchor="middle" font-size="10" font-weight="400" fill="#5d6b7d">unknown provider → refusal, never a default</text><rect x="590" y="36" width="150" height="44" fill="#fff" stroke="currentColor" stroke-width="1"/><text x="665.0" y="55.0" text-anchor="middle" font-size="12" font-weight="400" fill="currentColor">gitprovider.GitHub</text><text x="665.0" y="70.0" text-anchor="middle" font-size="10.5" fill="#5d6b7d">REST + GraphQL, merge queue</text><rect x="590" y="100" width="150" height="44" fill="#fff" stroke="currentColor" stroke-width="1"/><text x="665.0" y="119.0" text-anchor="middle" font-size="12" font-weight="400" fill="currentColor">gitprovider.GitLab</text><text x="665.0" y="134.0" text-anchor="middle" font-size="10.5" fill="#5d6b7d">REST, merge trains</text><line x1="542" y1="72" x2="588" y2="58" stroke="#1d4e89" stroke-width="1.2" marker-end="url(#arrow-accent)"/><line x1="542" y1="100" x2="588" y2="122" stroke="#1d4e89" stroke-width="1.2" marker-end="url(#arrow-accent)"/><rect x="414" y="200" width="150" height="40" fill="#eef2f7" stroke="currentColor" stroke-width="1"/><text x="489.0" y="217.0" text-anchor="middle" font-size="12" font-weight="400" fill="currentColor">ports.SecretStore</text><text x="489.0" y="232.0" text-anchor="middle" font-size="10.5" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">read HERE, in the core</text><polyline points="522,94 522,198" fill="none" stroke="currentColor" stroke-width="1.2" marker-end="url(#arrow)"/><text x="528" y="150" text-anchor="start" font-size="10.5" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">Get(ref)</text><text x="20" y="200" text-anchor="start" font-size="10.5" font-weight="400" fill="#5d6b7d">the delivery domain never learns GitHub exists;</text><text x="20" y="216" text-anchor="start" font-size="10.5" font-weight="400" fill="#5d6b7d">the git adapter never learns a vault exists;</text><text x="20" y="232" text-anchor="start" font-size="10.5" font-weight="400" fill="#5d6b7d">the resource domain never learns PRs exist.</text><text x="20" y="266" text-anchor="start" font-size="10.5" font-weight="400" fill="#5d6b7d">Blue: the adapter chosen for this call. The vault is read in the composition root and the token is handed over ready.</text></svg><figcaption>A per-request port. The delivery domain asks for a provider by repository; the composition root resolves integration and credential and returns a ready adapter.</figcaption></figure>

Repository → integration → credential → adapter, on every request. The git
adapter receives a ready token and never learns a vault exists; the delivery
domain never learns GitHub exists; the resource domain never learns pull
requests exist. An unknown provider is a refusal, not a default, because
opening a PR in the wrong place is worse than not opening one. The agent
provider port — Anthropic or OpenAI, chosen per account — has exactly the
same shape.

## The frontier is a test

The third discipline is the cheapest and the one most often skipped. A rule
that lives in a README lasts until the first deadline. DOP's lives in the
test suite:

{{< snippet file="hexagonal-dop/architecture_test.go" lang="go" >}}

Parse every file under `internal/domain` for its imports; fail on any adapter
package or vendor SDK. A second test walks everything else under `internal/`
and fails if anything but the composition root imports an adapter. Both run
on every `go test ./...`, so the frontier breaks the build before it breaks
the design.

## What it costs, and where not to bother

Two adapters per port, written and maintained, from the first commit. A
contract suite per port, and the infrastructure to run it against the real
backends, not only the emulators. One more indirection on every
infrastructure call. And a vendor's strongest feature — secret versions,
per-secret IAM, Firebase's custom claims — inaccessible to the domain by
construction. That last one is the price, and it is deliberate.

The same rules say where the pattern does not pay. Two alternatives were
considered for the platform as a whole and rejected: couple to GCP now and
port later — "later" is when the coupling is already spread out, and running
on a local cluster was a development requirement, not an ambition — and a
generic multi-cloud library, which delivers the common denominator of *the
library's* vendors rather than the domain's, and trades one coupling for
another. But inside the boundary, DOP does not put a port in front of Postgres
queries that will only ever run on Postgres, does not abstract the gRPC edge,
and does not wrap the logger. A port is worth having where the second adapter
is real: a second environment, a second host the customer can pick, a test
that has to run with no infrastructure. Where the second adapter is
imaginary, the interface is a folder name.

Hexagonal, in the end, is an accounting rule: the domain pays nothing to a
vendor, and the adapter pays whatever the vendor charges. The three
disciplines are how the books stay honest.
