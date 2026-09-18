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

<figure class="diagram"><svg viewBox="0 0 720 464" role="img" aria-label="The BFF and the CLI reach a navy hexagon labelled internal/domain through a gRPC edge; on the right, ports drawn as sockets on the hexagon's edge connect to rows of adapter chips, grouped as infrastructure ports chosen at boot and domain provider ports chosen per request; a composition root band underneath." xmlns="http://www.w3.org/2000/svg" font-family="IBM Plex Sans, system-ui, sans-serif" color="#16233a"><defs><marker id="h-ink" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1,1 L9,5 L1,9 z" fill="#16233a"/></marker><marker id="h-navy" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1,1 L9,5 L1,9 z" fill="#1d4e89"/></marker><marker id="h-forbid" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1,1 L9,5 L1,9 z" fill="#b3261e"/></marker><marker id="h-muted" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1,1 L9,5 L1,9 z" fill="#5d6b7d"/></marker></defs><rect x="16" y="60" width="190" height="330" rx="10" fill="#eef2f7" stroke="#d5dde8" stroke-width="1"/><text x="32" y="84" text-anchor="start" font-size="12.5" font-weight="600" fill="#5d6b7d">drives the domain</text><rect x="420" y="60" width="284" height="330" rx="10" fill="#eef2f7" stroke="#d5dde8" stroke-width="1"/><text x="436" y="84" text-anchor="start" font-size="12.5" font-weight="600" fill="#5d6b7d">driven by the domain</text><polygon points="258.0,138.5 354.0,138.5 402.0,222.0 354.0,305.5 258.0,305.5 210.0,222.0" fill="#1d4e89" stroke="#173d6e" stroke-width="1.5"/><text x="306" y="192" text-anchor="middle" font-size="14.5" font-weight="600" fill="#fff">internal/domain</text><text x="306" y="211" text-anchor="middle" font-size="11" font-weight="400" fill="#cfe0f5">model · use cases · ports</text><text x="306" y="236" text-anchor="middle" font-size="10.5" font-weight="400" fill="#e8f0fa" font-family="IBM Plex Mono, ui-monospace, monospace">demand · delivery</text><text x="306" y="252" text-anchor="middle" font-size="10.5" font-weight="400" fill="#e8f0fa" font-family="IBM Plex Mono, ui-monospace, monospace">execution · resource</text><text x="306" y="268" text-anchor="middle" font-size="10.5" font-weight="400" fill="#e8f0fa" font-family="IBM Plex Mono, ui-monospace, monospace">identity · …</text><rect x="32" y="104" width="110" height="50" rx="6" fill="#fff" stroke="#b9c5d4" stroke-width="1.2"/><text x="87.0" y="126.0" text-anchor="middle" font-size="13" font-weight="600" fill="#16233a">dop-api</text><text x="87.0" y="143.0" text-anchor="middle" font-size="11" font-weight="400" fill="#5d6b7d">Python BFF</text><rect x="32" y="176" width="110" height="50" rx="6" fill="#fff" stroke="#b9c5d4" stroke-width="1.2"/><text x="87.0" y="198.0" text-anchor="middle" font-size="13" font-weight="600" fill="#16233a">dop-cmd</text><text x="87.0" y="215.0" text-anchor="middle" font-size="11" font-weight="400" fill="#5d6b7d">CLI</text><rect x="150" y="138" width="50" height="56" rx="6" fill="#fff" stroke="#b9c5d4" stroke-width="1.2"/><text x="175.0" y="163.0" text-anchor="middle" font-size="13" font-weight="600" fill="#16233a">edge</text><text x="175.0" y="180.0" text-anchor="middle" font-size="11" font-weight="400" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">gRPC</text><path d="M 142,129 L 150,152" fill="none" stroke="#16233a" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" marker-end="url(#h-ink)"/><path d="M 142,201 L 150,180" fill="none" stroke="#16233a" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" marker-end="url(#h-ink)"/><path d="M 200,166 L 204,214" fill="none" stroke="#1d4e89" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/><rect x="204" y="216" width="12" height="12" rx="2" fill="#fff" stroke="#1d4e89" stroke-width="1.6"/><text x="32" y="262" text-anchor="start" font-size="11.5" font-weight="400" fill="#5d6b7d">The BFF and the CLI reach the</text><text x="32" y="279" text-anchor="start" font-size="11.5" font-weight="400" fill="#5d6b7d">domain only through gRPC —</text><text x="32" y="296" text-anchor="start" font-size="11.5" font-weight="400" fill="#5d6b7d">the one driving adapter.</text><text x="436" y="108" text-anchor="start" font-size="11.5" font-weight="600" fill="#1d4e89">infrastructure · chosen at boot, one active</text><text x="436" y="280" text-anchor="start" font-size="11.5" font-weight="600" fill="#1d4e89">providers · per request, several active</text><path d="M 368.7701149425287,152 C 398.38505747126436,152 398.38505747126436,132 428,132" fill="none" stroke="#1d4e89" stroke-width="1.2" stroke-linecap="round"/><rect x="356.7701149425287" y="147" width="10" height="10" rx="2" fill="#fff" stroke="#1d4e89" stroke-width="1.6"/><text x="436" y="136" text-anchor="start" font-size="11.5" font-weight="600" fill="#16233a" font-family="IBM Plex Mono, ui-monospace, monospace">SecretStore</text><rect x="524" y="121" width="54" height="22" rx="11" fill="#fff" stroke="#b9c5d4" stroke-width="1"/><text x="551.0" y="136" text-anchor="middle" font-size="10.5" font-weight="400" fill="#16233a" font-family="IBM Plex Mono, ui-monospace, monospace">memory</text><rect x="584" y="121" width="35" height="22" rx="11" fill="#fff" stroke="#b9c5d4" stroke-width="1"/><text x="601.5" y="136" text-anchor="middle" font-size="10.5" font-weight="400" fill="#16233a" font-family="IBM Plex Mono, ui-monospace, monospace">k8s</text><rect x="625" y="121" width="35" height="22" rx="11" fill="#fff" stroke="#b9c5d4" stroke-width="1"/><text x="642.5" y="136" text-anchor="middle" font-size="10.5" font-weight="400" fill="#16233a" font-family="IBM Plex Mono, ui-monospace, monospace">gcp</text><path d="M 382.5632183908046,176 C 405.2816091954023,176 405.2816091954023,166 428,166" fill="none" stroke="#1d4e89" stroke-width="1.2" stroke-linecap="round"/><rect x="370.5632183908046" y="171" width="10" height="10" rx="2" fill="#fff" stroke="#1d4e89" stroke-width="1.6"/><text x="436" y="170" text-anchor="start" font-size="11.5" font-weight="600" fill="#16233a" font-family="IBM Plex Mono, ui-monospace, monospace">EventBus</text><rect x="502" y="155" width="54" height="22" rx="11" fill="#fff" stroke="#b9c5d4" stroke-width="1"/><text x="529.0" y="170" text-anchor="middle" font-size="10.5" font-weight="400" fill="#16233a" font-family="IBM Plex Mono, ui-monospace, monospace">memory</text><rect x="562" y="155" width="41" height="22" rx="11" fill="#fff" stroke="#b9c5d4" stroke-width="1"/><text x="582.5" y="170" text-anchor="middle" font-size="10.5" font-weight="400" fill="#16233a" font-family="IBM Plex Mono, ui-monospace, monospace">nats</text><path d="M 396.35632183908046,200 C 412.17816091954023,200 412.17816091954023,200 428,200" fill="none" stroke="#1d4e89" stroke-width="1.2" stroke-linecap="round"/><rect x="384.35632183908046" y="195" width="10" height="10" rx="2" fill="#fff" stroke="#1d4e89" stroke-width="1.6"/><text x="436" y="204" text-anchor="start" font-size="11.5" font-weight="600" fill="#16233a" font-family="IBM Plex Mono, ui-monospace, monospace">IdentityProvider</text><rect x="559" y="189" width="67" height="22" rx="11" fill="#fff" stroke="#b9c5d4" stroke-width="1"/><text x="592.5" y="204" text-anchor="middle" font-size="10.5" font-weight="400" fill="#16233a" font-family="IBM Plex Mono, ui-monospace, monospace">firebase</text><rect x="632" y="189" width="41" height="22" rx="11" fill="#fff" stroke="#b9c5d4" stroke-width="1"/><text x="652.5" y="204" text-anchor="middle" font-size="10.5" font-weight="400" fill="#16233a" font-family="IBM Plex Mono, ui-monospace, monospace">oidc</text><path d="M 407.85057471264366,224 C 417.92528735632186,224 417.92528735632186,234 428,234" fill="none" stroke="#1d4e89" stroke-width="1.2" stroke-linecap="round"/><rect x="395.85057471264366" y="219" width="10" height="10" rx="2" fill="#fff" stroke="#1d4e89" stroke-width="1.6"/><text x="436" y="238" text-anchor="start" font-size="11.5" font-weight="600" fill="#16233a" font-family="IBM Plex Mono, ui-monospace, monospace">SandboxLauncher</text><rect x="552" y="223" width="54" height="22" rx="11" fill="#fff" stroke="#b9c5d4" stroke-width="1"/><text x="579.0" y="238" text-anchor="middle" font-size="10.5" font-weight="400" fill="#16233a" font-family="IBM Plex Mono, ui-monospace, monospace">docker</text><rect x="612" y="223" width="35" height="22" rx="11" fill="#fff" stroke="#b9c5d4" stroke-width="1"/><text x="629.5" y="238" text-anchor="middle" font-size="10.5" font-weight="400" fill="#16233a" font-family="IBM Plex Mono, ui-monospace, monospace">k8s</text><path d="M 394.0574712643678,248 C 411.0287356321839,248 411.0287356321839,304 428,304" fill="none" stroke="#1d4e89" stroke-width="1.2" stroke-linecap="round"/><rect x="382.0574712643678" y="243" width="10" height="10" rx="2" fill="#fff" stroke="#1d4e89" stroke-width="1.6"/><text x="436" y="308" text-anchor="start" font-size="11.5" font-weight="600" fill="#16233a" font-family="IBM Plex Mono, ui-monospace, monospace">GitProvider</text><rect x="524" y="293" width="54" height="22" rx="11" fill="#fff" stroke="#b9c5d4" stroke-width="1"/><text x="551.0" y="308" text-anchor="middle" font-size="10.5" font-weight="400" fill="#16233a" font-family="IBM Plex Mono, ui-monospace, monospace">github</text><rect x="584" y="293" width="54" height="22" rx="11" fill="#fff" stroke="#b9c5d4" stroke-width="1"/><text x="611.0" y="308" text-anchor="middle" font-size="10.5" font-weight="400" fill="#16233a" font-family="IBM Plex Mono, ui-monospace, monospace">gitlab</text><path d="M 380.264367816092,272 C 404.132183908046,272 404.132183908046,338 428,338" fill="none" stroke="#1d4e89" stroke-width="1.2" stroke-linecap="round"/><rect x="368.264367816092" y="267" width="10" height="10" rx="2" fill="#fff" stroke="#1d4e89" stroke-width="1.6"/><text x="436" y="342" text-anchor="start" font-size="11.5" font-weight="600" fill="#16233a" font-family="IBM Plex Mono, ui-monospace, monospace">AgentProvider</text><rect x="538" y="327" width="73" height="22" rx="11" fill="#fff" stroke="#b9c5d4" stroke-width="1"/><text x="574.5" y="342" text-anchor="middle" font-size="10.5" font-weight="400" fill="#16233a" font-family="IBM Plex Mono, ui-monospace, monospace">anthropic</text><rect x="617" y="327" width="54" height="22" rx="11" fill="#fff" stroke="#b9c5d4" stroke-width="1"/><text x="644.0" y="342" text-anchor="middle" font-size="10.5" font-weight="400" fill="#16233a" font-family="IBM Plex Mono, ui-monospace, monospace">openai</text><path d="M 366.4712643678161,296 C 397.235632183908,296 397.235632183908,372 428,372" fill="none" stroke="#1d4e89" stroke-width="1.2" stroke-linecap="round"/><rect x="354.4712643678161" y="291" width="10" height="10" rx="2" fill="#fff" stroke="#1d4e89" stroke-width="1.6"/><text x="436" y="376" text-anchor="start" font-size="11.5" font-weight="600" fill="#16233a" font-family="IBM Plex Mono, ui-monospace, monospace">Mailer</text><rect x="488" y="361" width="41" height="22" rx="11" fill="#fff" stroke="#b9c5d4" stroke-width="1"/><text x="508.5" y="376" text-anchor="middle" font-size="10.5" font-weight="400" fill="#16233a" font-family="IBM Plex Mono, ui-monospace, monospace">smtp</text><rect x="535" y="361" width="67" height="22" rx="11" fill="#fff" stroke="#b9c5d4" stroke-width="1"/><text x="568.5" y="376" text-anchor="middle" font-size="10.5" font-weight="400" fill="#16233a" font-family="IBM Plex Mono, ui-monospace, monospace">sendgrid</text><rect x="16" y="404" width="688" height="44" rx="10" fill="#fff" stroke="#b9c5d4" stroke-width="1" stroke-dasharray="6 5"/><text x="32" y="431" text-anchor="start" font-size="13" font-weight="600" fill="#16233a" font-family="IBM Plex Mono, ui-monospace, monospace">internal/app</text><text x="140" y="431" text-anchor="start" font-size="12" font-weight="400" fill="#5d6b7d">the composition root — knows both ends; configuration picks each adapter</text></svg><figcaption>The three regions of dop-core. The domain declares the ports (the sockets on its edges); each adapter package plugs into one; the composition root does the plugging, by configuration. The two families on the right have opposite life cycles.</figcaption></figure>

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

<figure class="diagram"><svg viewBox="0 0 720 392" role="img" aria-label="The SecretStore contract suite fans out to three adapters: memory always, k8s when a cluster answers, GCP behind a build tag; below, three columns for domain, adapter and SDKs, with allowed arrows from adapter to domain and to SDKs, and a red dashed forbidden arrow from domain to adapter." xmlns="http://www.w3.org/2000/svg" font-family="IBM Plex Sans, system-ui, sans-serif" color="#16233a"><defs><marker id="h-ink" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1,1 L9,5 L1,9 z" fill="#16233a"/></marker><marker id="h-navy" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1,1 L9,5 L1,9 z" fill="#1d4e89"/></marker><marker id="h-forbid" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1,1 L9,5 L1,9 z" fill="#b3261e"/></marker><marker id="h-muted" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1,1 L9,5 L1,9 z" fill="#5d6b7d"/></marker></defs><rect x="16" y="44" width="190" height="70" rx="6" fill="#1d4e89" stroke="#173d6e" stroke-width="1.2"/><text x="111.0" y="76.0" text-anchor="middle" font-size="13" font-weight="600" fill="#fff">SecretStoreSuite</text><text x="111.0" y="93.0" text-anchor="middle" font-size="11" font-weight="400" fill="#cfe0f5">six numbered guarantees</text><text x="111" y="132" text-anchor="middle" font-size="10.5" font-weight="400" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">test/contract/secretstore.go</text><path d="M 206,79 L 240,79 L 262,46 L 282,46" fill="none" stroke="#1d4e89" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round" marker-end="url(#h-navy)"/><rect x="284" y="24" width="110" height="44" rx="6" fill="#fff" stroke="#b9c5d4" stroke-width="1.2"/><text x="339.0" y="51.0" text-anchor="middle" font-size="13" font-weight="600" fill="#16233a">memory</text><text x="408" y="51" text-anchor="start" font-size="12" font-weight="400" fill="#5d6b7d">always</text><path d="M 206,79 L 240,79 L 262,98 L 282,98" fill="none" stroke="#1d4e89" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round" marker-end="url(#h-navy)"/><rect x="284" y="76" width="110" height="44" rx="6" fill="#fff" stroke="#b9c5d4" stroke-width="1.2"/><text x="339.0" y="103.0" text-anchor="middle" font-size="13" font-weight="600" fill="#16233a">k8s</text><text x="408" y="103" text-anchor="start" font-size="12" font-weight="400" fill="#5d6b7d">when a cluster answers</text><path d="M 206,79 L 240,79 L 262,150 L 282,150" fill="none" stroke="#1d4e89" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round" marker-end="url(#h-navy)"/><rect x="284" y="128" width="110" height="44" rx="6" fill="#fff" stroke="#b9c5d4" stroke-width="1.2" stroke-dasharray="6 5"/><text x="339.0" y="155.0" text-anchor="middle" font-size="13" font-weight="600" fill="#16233a">gcp</text><text x="408" y="155" text-anchor="start" font-size="12" font-weight="400" fill="#5d6b7d">behind a build tag, when a credential exists</text><text x="284" y="194" text-anchor="start" font-size="12" font-weight="600" fill="#1d4e89">one function, three targets</text><rect x="16" y="226" width="688" height="150" rx="10" fill="#eef2f7" stroke="#d5dde8" stroke-width="1"/><text x="32" y="250" text-anchor="start" font-size="12.5" font-weight="600" fill="#5d6b7d">the frontier, guarded by two tests on every go test ./...</text><rect x="40" y="262" width="150" height="52" rx="6" fill="#fff" stroke="#b9c5d4" stroke-width="1.2"/><text x="115.0" y="285.0" text-anchor="middle" font-size="12.5" font-weight="600" fill="#16233a">internal/domain</text><text x="115.0" y="302.0" text-anchor="middle" font-size="11" font-weight="400" fill="#5d6b7d">declares the ports</text><rect x="290" y="262" width="150" height="52" rx="6" fill="#fff" stroke="#b9c5d4" stroke-width="1.2"/><text x="365.0" y="285.0" text-anchor="middle" font-size="12.5" font-weight="600" fill="#16233a">internal/adapter</text><text x="365.0" y="302.0" text-anchor="middle" font-size="11" font-weight="400" fill="#5d6b7d">implements them</text><rect x="540" y="262" width="150" height="52" rx="6" fill="#fff" stroke="#b9c5d4" stroke-width="1.2"/><text x="615.0" y="285.0" text-anchor="middle" font-size="12.5" font-weight="600" fill="#16233a">SDKs</text><text x="615.0" y="302.0" text-anchor="middle" font-size="11" font-weight="400" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">pgx · nats · gcp · k8s</text><path d="M 440,288 L 538,288" fill="none" stroke="#1d4e89" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" marker-end="url(#h-navy)"/><text x="489" y="280" text-anchor="middle" font-size="10.5" font-weight="400" fill="#1d4e89">allowed</text><path d="M 290,276 L 192,276" fill="none" stroke="#1d4e89" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" marker-end="url(#h-navy)"/><text x="241" y="268" text-anchor="middle" font-size="10.5" font-weight="400" fill="#1d4e89">implements</text><path d="M 192,300 L 290,300" fill="none" stroke="#b3261e" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="6 5" marker-end="url(#h-forbid)"/><text x="241" y="322" text-anchor="middle" font-size="10.5" font-weight="600" fill="#b3261e">never</text><text x="40" y="350" text-anchor="start" font-size="11.5" font-weight="400" fill="#5d6b7d">TestTheDomainDoesNotImportInfrastructure — nothing under internal/domain imports an adapter or an SDK.</text><text x="40" y="366" text-anchor="start" font-size="11.5" font-weight="400" fill="#5d6b7d">TestOnlyAppKnowsTheAdapters — outside internal/app, nothing imports internal/adapter.</text></svg><figcaption>What keeps the pattern true over time. Above: one contract suite runs against every adapter. Below: the import frontier — adapters may know the domain and the SDKs; the domain may know neither — enforced by tests that break the build.</figcaption></figure>

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

<figure class="diagram"><svg viewBox="0 0 720 454" role="img" aria-label="Two lanes for SecretStore.Put: the in-memory adapter writes a map and returns; the Secret Manager adapter adds a version, confirms it by number, waits for the latest alias with retries, destroys older versions and returns, or refuses with KindUnavailable past the ceiling." xmlns="http://www.w3.org/2000/svg" font-family="IBM Plex Sans, system-ui, sans-serif" color="#16233a"><defs><marker id="h-ink" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1,1 L9,5 L1,9 z" fill="#16233a"/></marker><marker id="h-navy" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1,1 L9,5 L1,9 z" fill="#1d4e89"/></marker><marker id="h-forbid" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1,1 L9,5 L1,9 z" fill="#b3261e"/></marker><marker id="h-muted" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1,1 L9,5 L1,9 z" fill="#5d6b7d"/></marker></defs><rect x="16" y="16" width="250" height="48" rx="6" fill="#1d4e89" stroke="#173d6e" stroke-width="1.2"/><text x="141.0" y="37.0" text-anchor="middle" font-size="13" font-weight="600" fill="#fff">SecretStore.Put</text><text x="141.0" y="54.0" text-anchor="middle" font-size="11" font-weight="400" fill="#cfe0f5">the promise: read-after-write</text><rect x="16" y="88" width="688" height="88" rx="10" fill="#eef2f7" stroke="#d5dde8" stroke-width="1"/><text x="32" y="112" text-anchor="start" font-size="12.5" font-weight="600" fill="#5d6b7d">in-memory adapter</text><rect x="32" y="122" width="150" height="40" rx="6" fill="#fff" stroke="#b9c5d4" stroke-width="1.2"/><text x="107.0" y="147.0" text-anchor="middle" font-size="12.5" font-weight="400" fill="#16233a">map[key] = copy</text><path d="M 182,142 L 208,142" fill="none" stroke="#16233a" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" marker-end="url(#h-ink)"/><rect x="210" y="122" width="110" height="40" rx="6" fill="#fff" stroke="#b9c5d4" stroke-width="1.2"/><text x="265.0" y="147.0" text-anchor="middle" font-size="12.5" font-weight="400" fill="#16233a">return nil</text><text x="340" y="147" text-anchor="start" font-size="12" font-weight="400" fill="#5d6b7d" font-style="italic">the promise costs nothing here</text><rect x="16" y="192" width="688" height="246" rx="10" fill="#eef2f7" stroke="#d5dde8" stroke-width="1"/><text x="32" y="216" text-anchor="start" font-size="12.5" font-weight="600" fill="#5d6b7d">Secret Manager adapter</text><rect x="32" y="226" width="138" height="52" rx="6" fill="#fff" stroke="#b9c5d4" stroke-width="1.2"/><text x="101.0" y="249.0" text-anchor="middle" font-size="12.5" font-weight="500" fill="#16233a">AddSecretVersion</text><text x="101.0" y="266.0" text-anchor="middle" font-size="11" font-weight="400" fill="#5d6b7d">version n created</text><path d="M 172,252 L 186,252" fill="none" stroke="#16233a" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" marker-end="url(#h-ink)"/><rect x="188" y="226" width="138" height="52" rx="6" fill="#fff" stroke="#b9c5d4" stroke-width="1.2"/><text x="257.0" y="249.0" text-anchor="middle" font-size="12.5" font-weight="500" fill="#16233a">confirm v = n</text><text x="257.0" y="266.0" text-anchor="middle" font-size="11" font-weight="400" fill="#5d6b7d">by number — strong</text><path d="M 328,252 L 342,252" fill="none" stroke="#16233a" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" marker-end="url(#h-ink)"/><rect x="344" y="226" width="138" height="52" rx="6" fill="#1d4e89" stroke="#173d6e" stroke-width="1.2"/><text x="413.0" y="249.0" text-anchor="middle" font-size="12.5" font-weight="600" fill="#fff">await latest ≥ n</text><text x="413.0" y="266.0" text-anchor="middle" font-size="11" font-weight="400" fill="#cfe0f5">alias — eventual</text><path d="M 484,252 L 498,252" fill="none" stroke="#16233a" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" marker-end="url(#h-ink)"/><rect x="500" y="226" width="138" height="52" rx="6" fill="#fff" stroke="#b9c5d4" stroke-width="1.2"/><text x="569.0" y="249.0" text-anchor="middle" font-size="12.5" font-weight="500" fill="#16233a">destroyOlder</text><text x="569.0" y="266.0" text-anchor="middle" font-size="11" font-weight="400" fill="#5d6b7d">old material gone</text><path d="M 640,252 L 654,252" fill="none" stroke="#16233a" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" marker-end="url(#h-ink)"/><rect x="656" y="226" width="34" height="52" rx="6" fill="#fff" stroke="#b9c5d4" stroke-width="1.2"/><text x="673.0" y="257.0" text-anchor="middle" font-size="16" font-weight="600" fill="#16233a">✓</text><path d="M 374,280 L 374,302 L 356,302 L 356,282" fill="none" stroke="#1d4e89" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round" marker-end="url(#h-navy)"/><text x="346" y="306" text-anchor="end" font-size="11" font-weight="400" fill="#1d4e89" font-family="IBM Plex Mono, ui-monospace, monospace">retry · 25 ms → 1 s · ≤ 30 s</text><path d="M 458,280 L 458,338" fill="none" stroke="#1d4e89" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="6 5" marker-end="url(#h-navy)"/><rect x="378" y="340" width="160" height="44" rx="6" fill="#fff" stroke="#1d4e89" stroke-width="1.2"/><text x="458.0" y="359.0" text-anchor="middle" font-size="12.5" font-weight="600" fill="#1d4e89">KindUnavailable</text><text x="458.0" y="376.0" text-anchor="middle" font-size="11" font-weight="400" fill="#5d6b7d">past the ceiling</text><text x="458" y="404" text-anchor="middle" font-size="11.5" font-weight="400" fill="#5d6b7d">write accepted, read-after-write not confirmed:</text><text x="458" y="420" text-anchor="middle" font-size="11.5" font-weight="400" fill="#5d6b7d">an error somebody reads, not a Get saying "absent".</text></svg><figcaption>The same Put through two adapters. In memory the promise is free. On Secret Manager the adapter confirms by version number, waits for the alias to catch up — the highlighted step — and past the ceiling refuses rather than lie.</figcaption></figure>

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

<figure class="diagram"><svg viewBox="0 0 720 290" role="img" aria-label="The delivery domain calls For with account and repository; inside the composition root three steps resolve repository, integration and vault; a GitHub or GitLab adapter is returned per call; the vault is read inside the resolver." xmlns="http://www.w3.org/2000/svg" font-family="IBM Plex Sans, system-ui, sans-serif" color="#16233a"><defs><marker id="h-ink" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1,1 L9,5 L1,9 z" fill="#16233a"/></marker><marker id="h-navy" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1,1 L9,5 L1,9 z" fill="#1d4e89"/></marker><marker id="h-forbid" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1,1 L9,5 L1,9 z" fill="#b3261e"/></marker><marker id="h-muted" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1,1 L9,5 L1,9 z" fill="#5d6b7d"/></marker></defs><rect x="16" y="60" width="160" height="64" rx="6" fill="#1d4e89" stroke="#173d6e" stroke-width="1.2"/><text x="96.0" y="89.0" text-anchor="middle" font-size="13" font-weight="600" fill="#fff">domain/delivery</text><text x="96.0" y="106.0" text-anchor="middle" font-size="11" font-weight="400" fill="#cfe0f5">opens the PR</text><path d="M 176,92 L 206,92" fill="none" stroke="#1d4e89" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" marker-end="url(#h-navy)"/><text x="96" y="146" text-anchor="middle" font-size="11" font-weight="400" fill="#1d4e89" font-family="IBM Plex Mono, ui-monospace, monospace">For(account, repo)</text><rect x="208" y="24" width="320" height="172" rx="10" fill="#eef2f7" stroke="#d5dde8" stroke-width="1"/><text x="224" y="48" text-anchor="start" font-size="12.5" font-weight="600" fill="#5d6b7d">internal/app · gitProviders.For</text><rect x="222" y="56" width="92" height="52" rx="6" fill="#fff" stroke="#b9c5d4" stroke-width="1.2"/><text x="268.0" y="79.0" text-anchor="middle" font-size="12.5" font-weight="600" fill="#16233a">repository</text><text x="268.0" y="96.0" text-anchor="middle" font-size="11" font-weight="400" fill="#5d6b7d">→ integration</text><path d="M 316,82 L 320,82" fill="none" stroke="#16233a" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/><rect x="322" y="56" width="92" height="52" rx="6" fill="#fff" stroke="#b9c5d4" stroke-width="1.2"/><text x="368.0" y="79.0" text-anchor="middle" font-size="12.5" font-weight="600" fill="#16233a">integration</text><text x="368.0" y="96.0" text-anchor="middle" font-size="11" font-weight="400" fill="#5d6b7d">→ provider</text><path d="M 416,82 L 420,82" fill="none" stroke="#16233a" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/><rect x="422" y="56" width="92" height="52" rx="6" fill="#fff" stroke="#b9c5d4" stroke-width="1.2"/><text x="468.0" y="79.0" text-anchor="middle" font-size="12.5" font-weight="600" fill="#16233a">vault</text><text x="468.0" y="96.0" text-anchor="middle" font-size="11" font-weight="400" fill="#5d6b7d">→ token</text><text x="222" y="138" text-anchor="start" font-size="11.5" font-weight="600" fill="#1d4e89">resolved on every request</text><text x="222" y="156" text-anchor="start" font-size="11.5" font-weight="400" fill="#5d6b7d">unknown provider: a refusal,</text><text x="222" y="172" text-anchor="start" font-size="11.5" font-weight="400" fill="#5d6b7d">never a default</text><rect x="548" y="36" width="156" height="52" rx="6" fill="#fff" stroke="#b9c5d4" stroke-width="1.2"/><text x="626.0" y="59.0" text-anchor="middle" font-size="13" font-weight="600" fill="#16233a">GitHub</text><text x="626.0" y="76.0" text-anchor="middle" font-size="11" font-weight="400" fill="#5d6b7d">GraphQL · merge queue</text><rect x="548" y="108" width="156" height="52" rx="6" fill="#fff" stroke="#b9c5d4" stroke-width="1.2"/><text x="626.0" y="131.0" text-anchor="middle" font-size="13" font-weight="600" fill="#16233a">GitLab</text><text x="626.0" y="148.0" text-anchor="middle" font-size="11" font-weight="400" fill="#5d6b7d">REST · merge trains</text><path d="M 528,82 L 546,62" fill="none" stroke="#1d4e89" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" marker-end="url(#h-navy)"/><path d="M 528,110 L 546,134" fill="none" stroke="#1d4e89" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" marker-end="url(#h-navy)"/><text x="632" y="180" text-anchor="middle" font-size="11" font-weight="400" fill="#5d6b7d" font-style="italic">the token arrives ready-made</text><path d="M 468,110 L 468,224" fill="none" stroke="#16233a" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round" marker-end="url(#h-ink)"/><text x="476" y="214" text-anchor="start" font-size="11" font-weight="400" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">Get(ref)</text><rect x="388" y="226" width="160" height="48" rx="6" fill="#fff" stroke="#b9c5d4" stroke-width="1.2"/><text x="468.0" y="247.0" text-anchor="middle" font-size="13" font-weight="600" fill="#16233a">ports.SecretStore</text><text x="468.0" y="264.0" text-anchor="middle" font-size="11" font-weight="400" fill="#5d6b7d">read here, in the core</text><text x="16" y="232" text-anchor="start" font-size="12" font-weight="400" fill="#5d6b7d">The delivery domain never learns GitHub exists.</text><text x="16" y="250" text-anchor="start" font-size="12" font-weight="400" fill="#5d6b7d">The git adapter never learns a vault exists.</text><text x="16" y="268" text-anchor="start" font-size="12" font-weight="400" fill="#5d6b7d">The resource domain never learns PRs exist.</text></svg><figcaption>A per-request port. The delivery domain asks for a provider by repository; the composition root resolves integration and credential and returns a ready adapter — GitHub for one repository, GitLab for the next.</figcaption></figure>

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
