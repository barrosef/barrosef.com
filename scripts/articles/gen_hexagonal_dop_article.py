#!/usr/bin/env python3
"""Generates the hexagonal-architecture article (DOP) in EN and PT-BR with identical SVG figures."""
from pathlib import Path

SITE = Path(__file__).resolve().parents[2] / "content"
ACCENT = "#1d4e89"
MUTED = "#5d6b7d"
HAIR = "#c9d3e0"
TINT = "#eef2f7"
MONO = ' font-family="IBM Plex Mono, ui-monospace, monospace"'

# ---------------------------------------------------------------- helpers
def box(x, y, w, h, title, sub=None, fill="#fff", stroke="currentColor", dash=False, bold=True, tcolor="currentColor", sub_mono=True):
    d = ' stroke-dasharray="5 4"' if dash else ""
    out = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" stroke="{stroke}" stroke-width="1"{d}/>'
    cx = x + w / 2
    if sub:
        out += f'<text x="{cx}" y="{y + h/2 - 3}" text-anchor="middle" font-size="12" font-weight="{600 if bold else 400}" fill="{tcolor}">{title}</text>'
        out += f'<text x="{cx}" y="{y + h/2 + 12}" text-anchor="middle" font-size="10.5" fill="{MUTED}"{MONO if sub_mono else ""}>{sub}</text>'
    else:
        out += f'<text x="{cx}" y="{y + h/2 + 4}" text-anchor="middle" font-size="12" font-weight="{600 if bold else 400}" fill="{tcolor}">{title}</text>'
    return out

def arrow(x1, y1, x2, y2, label=None, lx=None, ly=None, color="currentColor", dash=False, anchor="middle", mono=True):
    d = ' stroke-dasharray="5 4"' if dash else ""
    m = "arrow-accent" if color == ACCENT else "arrow"
    out = f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="1.2"{d} marker-end="url(#{m})"/>'
    if label:
        lx = (x1 + x2) / 2 if lx is None else lx
        ly = (y1 + y2) / 2 - 6 if ly is None else ly
        out += f'<text x="{lx}" y="{ly}" text-anchor="{anchor}" font-size="10.5" fill="{color if color == ACCENT else MUTED}"{MONO if mono else ""}>{label}</text>'
    return out

def elbow(points, label=None, lx=None, ly=None, color="currentColor", dash=False, anchor="middle", head=True):
    d = ' stroke-dasharray="5 4"' if dash else ""
    m = "arrow-accent" if color == ACCENT else "arrow"
    pts = " ".join(f"{x},{y}" for x, y in points)
    mk = f' marker-end="url(#{m})"' if head else ""
    out = f'<polyline points="{pts}" fill="none" stroke="{color}" stroke-width="1.2"{d}{mk}/>'
    if label:
        out += f'<text x="{lx}" y="{ly}" text-anchor="{anchor}" font-size="10.5" fill="{color if color == ACCENT else MUTED}"{MONO}>{label}</text>'
    return out

def label(x, y, text, size=11, color=MUTED, anchor="start", weight=400, mono=False):
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-size="{size}" font-weight="{weight}" fill="{color}"{MONO if mono else ""}>{text}</text>'

DEFS = f'''<defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="currentColor"/></marker><marker id="arrow-accent" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{ACCENT}"/></marker></defs>'''

def figure(w, h, body, caption, aria):
    # No blank lines inside: Goldmark ends an HTML block at the first blank line.
    return (f'<figure class="diagram"><svg viewBox="0 0 {w} {h}" role="img" aria-label="{aria}" '
            f'xmlns="http://www.w3.org/2000/svg" font-family="IBM Plex Sans, system-ui, sans-serif" color="#16233a">'
            f'{DEFS}{body}</svg><figcaption>{caption}</figcaption></figure>')

# ---------------------------------------------------------------- figure 1: the shape
def fig_shape(L):
    b = ""
    # driving side
    b += label(20, 30, L["driving_col"], size=11, weight=600, color="currentColor")
    b += box(20, 60, 140, 46, "dop-api", L["bff_sub"], fill="#fff")
    b += box(20, 122, 140, 46, "dop-cmd", L["cli_sub"], fill="#fff")
    b += box(190, 60, 80, 108, L["edge"], None, fill=TINT, bold=True)
    b += label(230, 154, "internal/app/grpc", size=9, anchor="middle", mono=True)
    b += arrow(162, 83, 188, 90, label="gRPC", lx=175, ly=72)
    b += arrow(162, 145, 188, 138)
    b += arrow(272, 114, 296, 114)
    # the hexagon: the domain
    hx = [(320, 40), (450, 40), (474, 190), (450, 340), (320, 340), (296, 190)]
    pts = " ".join(f"{x},{y}" for x, y in hx)
    b += f'<polygon points="{pts}" fill="{TINT}" stroke="currentColor" stroke-width="1.2"/>'
    b += label(385, 70, "internal/domain", size=12, anchor="middle", color="currentColor", weight=600)
    b += label(385, 86, L["domain_sub"], size=10, anchor="middle")
    pk = ["demand", "delivery", "execution", "resource", "identity", "event", "workflow", "…"]
    for i, p in enumerate(pk):
        b += label(385, 116 + i * 17, p, size=10.5, anchor="middle", color="currentColor", mono=True)
    b += label(385, 264, L["ports_pkg"], size=10, anchor="middle", color=ACCENT, weight=600)
    b += label(385, 278, L["ports_sub"], size=9.5, anchor="middle", color=ACCENT)
    b += label(385, 292, "domain/ports", size=9, anchor="middle", color=ACCENT, mono=True)
    b += label(385, 304, "delivery.GitProvider …", size=9, anchor="middle", color=ACCENT, mono=True)
    # driven side: two families
    b += label(500, 30, L["driven_col"], size=11, weight=600, color="currentColor")
    b += label(500, 56, L["family_a"], size=10, color=ACCENT, weight=600)
    rows_a = [("SecretStore", "memory · k8s · gcp"), ("EventBus", "memory · nats"), ("IdentityProvider", "firebase · oidc"),
              ("ObjectStore", "fs · gcs"), ("SandboxLauncher", "docker · k8s"), ("repositories", "postgres")]
    def edge_x(y):  # the hexagon's right edge: (450,40) → (474,190) → (450,340)
        return 450 + (y - 40) * 0.16 if y < 190 else 474 - (y - 190) * 0.16
    y = 74
    for name, ad in rows_a:
        b += f'<circle cx="{edge_x(y - 4):.0f}" cy="{y - 4}" r="3" fill="{ACCENT}"/>'
        b += label(500, y, name, size=10.5, color="currentColor", mono=True)
        b += label(740, y, ad, size=10, anchor="end", mono=True)
        y += 20
    b += label(500, 212, L["family_b"], size=10, color=ACCENT, weight=600)
    rows_b = [("GitProvider", "github · gitlab"), ("AgentProvider", "anthropic · openai"), ("Mailer", "smtp · sendgrid"), ("SMSer", "twilio · zenvia")]
    y = 230
    for name, ad in rows_b:
        b += f'<circle cx="{edge_x(y - 4):.0f}" cy="{y - 4}" r="3" fill="{ACCENT}"/>'
        b += label(500, y, name, size=10.5, color="currentColor", mono=True)
        b += label(740, y, ad, size=10, anchor="end", mono=True)
        y += 20
    b += label(500, 318, L["adapter_pkg"], size=9.5, mono=True)
    b += label(500, 332, L["adapter_note"], size=10)
    # composition root band
    b += f'<rect x="20" y="364" width="720" height="34" fill="#fff" stroke="currentColor" stroke-dasharray="5 4"/>'
    b += label(30, 385, "internal/app", size=11, weight=600, color="currentColor", mono=True)
    b += label(122, 385, L["root_note"], size=10.5)
    b += label(20, 420, L["legend"], size=10.5)
    return figure(760, 432, b, L["fig1_caption"], L["fig1_aria"])

# ---------------------------------------------------------------- figure 2: the adapter pays
def fig_pays(L):
    b = ""
    # the port, top-left
    b += box(20, 20, 200, 46, "SecretStore.Put", L["promise"], fill=TINT)
    # lane: memory
    b += label(20, 100, L["lane_mem"], size=11, weight=600, color="currentColor")
    b += box(20, 110, 130, 40, "map[key] = copy", None, fill="#fff", bold=False)
    b += arrow(152, 130, 188, 130)
    b += box(190, 110, 90, 40, "return nil", None, fill="#fff", bold=False)
    b += label(300, 134, L["mem_note"], size=10.5)
    b += f'<line x1="20" y1="168" x2="740" y2="168" stroke="{HAIR}" stroke-dasharray="3 4"/>'
    # lane: gcp
    b += label(20, 192, L["lane_gcp"], size=11, weight=600, color="currentColor")
    steps = [("AddSecretVersion", L["s1"]), ("confirm v=n", L["s2"]), ("await latest ≥ n", L["s3"]), ("destroyOlder", L["s4"])]
    W, G = 130, 20
    for i, (t, s_) in enumerate(steps):
        x = 20 + i * (W + G)
        stroke = ACCENT if i == 2 else "currentColor"
        b += box(x, 204, W, 48, t, s_, fill="#fff", bold=False, stroke=stroke, sub_mono=False)
        b += arrow(x + W + 2, 228, x + W + G - 2, 228)
    b += box(620, 204, 120, 48, "return nil", None, fill="#fff", bold=False)
    # the retry loop under step 3 (x 320..450), and the refusal past the ceiling
    b += elbow([(340, 254), (340, 272), (326, 272), (326, 256)], color=ACCENT)
    b += label(350, 276, L["loop"], size=9.5, color=ACCENT, mono=True)
    b += elbow([(430, 254), (430, 298)], color=ACCENT, dash=True)
    b += box(355, 300, 150, 40, "KindUnavailable", L["refuse_sub"], fill="#fff", stroke=ACCENT, bold=True, tcolor=ACCENT, sub_mono=False)
    b += label(515, 316, L["refuse_note1"], size=9.5)
    b += label(515, 330, L["refuse_note2"], size=9.5)
    b += label(20, 384, L["fig2_legend"], size=10.5)
    return figure(760, 396, b, L["fig2_caption"], L["fig2_aria"])

# ---------------------------------------------------------------- figure 3: per-request provider
def fig_provider(L):
    b = ""
    # left: the delivery domain
    b += box(20, 60, 170, 60, "domain/delivery", L["dl_sub"], fill=TINT)
    b += arrow(192, 90, 208, 90)
    b += label(105, 138, "→ For(account, repo)", size=10, anchor="middle", mono=True)
    # the resolver
    b += f'<rect x="210" y="20" width="330" height="150" fill="#fff" stroke="currentColor" stroke-dasharray="5 4"/>'
    b += label(220, 38, "internal/app · gitProviders.For", size=11, weight=600, color="currentColor", mono=True)
    b += box(224, 52, 92, 40, "1 · repo", L["r1"], fill="#fff", bold=False, sub_mono=False)
    b += arrow(318, 72, 336, 72)
    b += box(338, 52, 92, 40, "2 · integration", L["r2"], fill="#fff", bold=False, sub_mono=False)
    b += arrow(432, 72, 450, 72)
    b += box(452, 52, 78, 40, "3 · vault", L["r3"], fill="#fff", bold=False, sub_mono=False)
    b += label(360, 122, L["per_request"], size=10, anchor="middle", color=ACCENT)
    b += label(360, 152, L["refusal"], size=10, anchor="middle")
    # the adapters
    b += box(590, 36, 150, 44, "gitprovider.GitHub", L["gh_sub"], fill="#fff", bold=False, sub_mono=False)
    b += box(590, 100, 150, 44, "gitprovider.GitLab", L["gl_sub"], fill="#fff", bold=False, sub_mono=False)
    b += arrow(542, 72, 588, 58, color=ACCENT)
    b += arrow(542, 100, 588, 122, color=ACCENT)
    # the vault below
    b += box(414, 200, 150, 40, "ports.SecretStore", L["vault_sub"], fill=TINT, bold=False)
    b += elbow([(522, 94), (522, 198)], color="currentColor", label="Get(ref)", lx=528, ly=150, anchor="start")
    # what nobody knows
    b += label(20, 200, L["k1"], size=10.5)
    b += label(20, 216, L["k2"], size=10.5)
    b += label(20, 232, L["k3"], size=10.5)
    b += label(20, 266, L["fig3_legend"], size=10.5)
    return figure(760, 278, b, L["fig3_caption"], L["fig3_aria"])

# ---------------------------------------------------------------- figure 4: one suite, three adapters, two guards
def fig_suite(L):
    b = ""
    b += box(20, 40, 190, 70, "SecretStoreSuite", L["suite_sub"], fill=TINT)
    b += label(115, 124, "test/contract/secretstore.go", size=9.5, anchor="middle", mono=True)
    targets = [("memory", L["t_mem"], "go test ./...", False), ("k8s", L["t_k8s"], "-run SecretStore", False), ("gcp", L["t_gcp"], "-tags=integration", True)]
    for i, (name, cond, cmd, dash) in enumerate(targets):
        y = 30 + i * 46
        b += box(300, y, 150, 38, name, cmd, fill="#fff", bold=False, dash=dash)
        b += arrow(212, 75, 298, y + 19)
        b += label(460, y + 23, cond, size=10.5)
    b += label(300, 172, L["same_fn"], size=10.5, color=ACCENT)
    # the guards
    b += f'<line x1="20" y1="192" x2="740" y2="192" stroke="{HAIR}" stroke-dasharray="3 4"/>'
    b += label(20, 214, L["guards"], size=11, weight=600, color="currentColor")
    b += box(20, 226, 150, 40, "internal/domain", L["g_dom"], fill=TINT, bold=True, sub_mono=False)
    b += box(320, 226, 150, 40, "internal/adapter", L["g_ad"], fill="#fff", bold=True, sub_mono=False)
    b += box(590, 226, 150, 40, "vendor SDKs", "pgx · nats · gcp · k8s", fill="#fff", bold=True)
    b += arrow(172, 246, 318, 246, color=ACCENT, dash=True)
    b += f'<text x="245" y="240" text-anchor="middle" font-size="14" font-weight="700" fill="{ACCENT}">✕</text>'
    b += arrow(472, 246, 588, 246, color=ACCENT, dash=True)
    b += f'<text x="530" y="240" text-anchor="middle" font-size="14" font-weight="700" fill="{ACCENT}">✕</text>'
    b += label(20, 290, L["g_note1"], size=10.5)
    b += label(20, 305, L["g_note2"], size=10.5)
    return figure(760, 318, b, L["fig4_caption"], L["fig4_aria"])

# ---------------------------------------------------------------- figure text
LANG = {
    "en": dict(
        driving_col="who drives the domain", bff_sub="Python BFF · REST+SSE", cli_sub="CLI · v0.7.1", edge="gRPC edge",
        domain_sub="model · use cases · ports", ports_pkg="the PORTS", ports_sub="in the domain's language",
        driven_col="what the domain drives", family_a="infrastructure — chosen at boot, one active",
        family_b="domain providers — per request, several active",
        adapter_pkg="internal/adapter/<technology>", adapter_note="one package per vendor",
        root_note="the composition root: the only place that knows both ends — a config value picks the adapter for each port",
        legend="Left: driving adapters reach the domain through gRPC. Right: each port's adapters. Blue dot: a port on the hexagon's edge.",
        fig1_caption="The three regions of dop-core. The domain declares the ports; the adapters implement them one technology per package; the composition root wires them by configuration. The two families on the right have opposite life cycles.",
        fig1_aria="The BFF and the CLI reach the domain hexagon through a gRPC edge; on the other side, infrastructure ports chosen at boot and domain provider ports chosen per request each list their adapters; a composition root band underneath wires both ends.",
        promise="promise: read-after-write", lane_mem="in-memory adapter", mem_note="the promise is free here",
        lane_gcp="GCP Secret Manager adapter", s1="version n created", s2="by number: strong", s3="alias: eventual", s4="old material gone",
        loop="retry · 25 ms → 1 s backoff · ≤ SECRET_PROPAGATION_SECONDS", refuse_sub="past the ceiling",
        refuse_note1="write accepted, read-after-write not confirmed:", refuse_note2="an error somebody reads, not a Get saying \"absent\".",
        fig2_legend="Blue: the step that exists only because the vendor's alias is eventually consistent. Dashed: the way out when it does not converge.",
        fig2_caption="The same Put through two adapters. In memory the promise costs nothing; on Secret Manager the adapter confirms by version number, waits for the alias, and refuses rather than lie.",
        fig2_aria="Two lanes for SecretStore.Put: the in-memory adapter writes a map and returns; the GCP adapter adds a version, confirms it by number, waits for the latest alias with backoff, destroys older versions and returns, or refuses with KindUnavailable past the ceiling.",
        dl_sub="PRs · rebase · merge", r1="→ integration id", r2="→ provider", r3="→ token",
        per_request="resolved on EVERY request: two hosts, both work", refusal="unknown provider → refusal, never a default",
        gh_sub="REST + GraphQL, merge queue", gl_sub="REST, merge trains", vault_sub="read HERE, in the core",
        k1="the delivery domain never learns GitHub exists;", k2="the git adapter never learns a vault exists;", k3="the resource domain never learns PRs exist.",
        fig3_legend="Blue: the adapter chosen for this call. The vault is read in the composition root and the token is handed over ready.",
        fig3_caption="A per-request port. The delivery domain asks for a provider by repository; the composition root resolves integration and credential and returns a ready adapter.",
        fig3_aria="The delivery domain calls For with account and repo; inside the composition root the repository gives the integration, the integration gives the provider, the vault gives the token; a GitHub or GitLab adapter is returned per call.",
        suite_sub="the six numbered guarantees", t_mem="always", t_k8s="when a cluster answers", t_gcp="when a credential exists (emulator or real GCP)",
        same_fn="one function, three targets: substitutability in fact, not in intention",
        guards="two tests guard the frontier on every go test ./...", g_dom="declares the ports", g_ad="implements them",
        g_note1="TestTheDomainDoesNotImportInfrastructure: no file under internal/domain imports an adapter or a vendor SDK.",
        g_note2="TestOnlyAppKnowsTheAdapters: outside internal/app, nothing imports internal/adapter.",
        fig4_caption="What makes the pattern true over time: one contract suite that every adapter passes, and two import tests that break the build when the frontier is crossed.",
        fig4_aria="The SecretStore contract suite fans out to three adapters, memory always, k8s when a cluster answers, GCP behind a build tag; below, two crossed-out arrows show that the domain may not import adapters and adapters' SDKs may not reach the domain.",
    ),
    "pt-br": dict(
        driving_col="quem aciona o domínio", bff_sub="BFF Python · REST+SSE", cli_sub="CLI · v0.7.1", edge="borda gRPC",
        domain_sub="modelo · casos de uso · ports", ports_pkg="os PORTS", ports_sub="na linguagem do domínio",
        driven_col="o que o domínio aciona", family_a="infraestrutura — escolhidos no boot, um ativo",
        family_b="provedores de domínio — por requisição, vários ativos",
        adapter_pkg="internal/adapter/<tecnologia>", adapter_note="um pacote por fornecedor",
        root_note="a raiz de composição: o único lugar que conhece as duas pontas — a configuração escolhe o adapter de cada port",
        legend="Esquerda: adapters primários chegam ao domínio via gRPC. Direita: os adapters de cada port. Ponto azul: um port na borda do hexágono.",
        fig1_caption="As três regiões do dop-core. O domínio declara os ports; os adapters os implementam, uma tecnologia por pacote; a raiz de composição os liga por configuração. As duas famílias à direita têm ciclos de vida opostos.",
        fig1_aria="O BFF e a CLI chegam ao hexágono do domínio por uma borda gRPC; do outro lado, ports de infraestrutura escolhidos no boot e ports de provedor escolhidos por requisição listam seus adapters; uma faixa de raiz de composição embaixo liga as duas pontas.",
        promise="promessa: read-after-write", lane_mem="adapter em memória", mem_note="aqui a promessa é de graça",
        lane_gcp="adapter GCP Secret Manager", s1="versão n criada", s2="por número: forte", s3="alias: eventual", s4="material antigo destruído",
        loop="retry · backoff 25 ms → 1 s · ≤ SECRET_PROPAGATION_SECONDS", refuse_sub="passado o teto",
        refuse_note1="escrita aceita, read-after-write não confirmado:", refuse_note2="um erro que alguém lê, não um Get dizendo \"não existe\".",
        fig2_legend="Azul: o passo que só existe porque o alias do fornecedor é eventualmente consistente. Tracejado: a saída quando não converge.",
        fig2_caption="O mesmo Put por dois adapters. Em memória a promessa não custa nada; no Secret Manager o adapter confirma por número de versão, espera o alias e recusa em vez de mentir.",
        fig2_aria="Duas raias para SecretStore.Put: o adapter em memória escreve num map e retorna; o adapter GCP cria uma versão, confirma por número, espera o alias latest com backoff, destrói versões antigas e retorna, ou recusa com KindUnavailable passado o teto.",
        dl_sub="PRs · rebase · merge", r1="→ id da integração", r2="→ provedor", r3="→ token",
        per_request="resolvido a CADA requisição: dois hosts, os dois funcionam", refusal="provedor desconhecido → recusa, nunca um default",
        gh_sub="REST + GraphQL, merge queue", gl_sub="REST, merge trains", vault_sub="lido AQUI, no core",
        k1="o domínio de entrega nunca fica sabendo que o GitHub existe;", k2="o adapter git nunca fica sabendo que existe um cofre;", k3="o domínio de recursos nunca fica sabendo que PRs existem.",
        fig3_legend="Azul: o adapter escolhido para esta chamada. O cofre é lido na raiz de composição e o token é entregue pronto.",
        fig3_caption="Um port por requisição. O domínio de entrega pede um provedor por repositório; a raiz de composição resolve integração e credencial e devolve um adapter pronto.",
        fig3_aria="O domínio de entrega chama For com conta e repo; dentro da raiz de composição o repositório dá a integração, a integração dá o provedor, o cofre dá o token; um adapter GitHub ou GitLab é devolvido por chamada.",
        suite_sub="as seis garantias numeradas", t_mem="sempre", t_k8s="quando um cluster responde", t_gcp="quando existe credencial (emulador ou GCP real)",
        same_fn="uma função, três alvos: substituibilidade de fato, não de intenção",
        guards="dois testes guardam a fronteira em todo go test ./...", g_dom="declara os ports", g_ad="os implementa",
        g_note1="TestTheDomainDoesNotImportInfrastructure: nenhum arquivo sob internal/domain importa um adapter ou SDK de fornecedor.",
        g_note2="TestOnlyAppKnowsTheAdapters: fora de internal/app, nada importa internal/adapter.",
        fig4_caption="O que mantém o padrão verdadeiro ao longo do tempo: uma suíte de contrato que todo adapter passa, e dois testes de import que quebram o build quando a fronteira é cruzada.",
        fig4_aria="A suíte de contrato do SecretStore se abre em três adapters, memória sempre, k8s quando um cluster responde, GCP atrás de uma build tag; abaixo, duas setas cortadas mostram que o domínio não pode importar adapters e os SDKs dos adapters não chegam ao domínio.",
    ),
}

def snip(name, lang="go"):
    return f'{{{{< snippet file="hexagonal-dop/{name}" lang="{lang}" >}}}}'

# ---------------------------------------------------------------- the article, EN
EN = """---
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

§FIG1§

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

§SNIP:ports_secretstore.go§

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

§SNIP:resource_set_credential.go§

The domain builds a reference from its own identifiers and calls `Put`. It
orders the vault before the row for a reason it writes down, and it knows
nothing about where the bytes go.

## Two adapters from day one

The first discipline: a port with a single adapter is a guess, and it comes
out shaped like the vendor that inspired it. So the local adapter is not "for
later" — it is written with the port, and it is the proof that the port is
right.

§SNIP:secretstore_memory.go§

Fifty lines, and it is not a mock: it copies bytes in and out so a caller
cannot mutate the vault by accident, and it passes exactly the same tests as
the GCP one. The in-memory event bus is the same story with more at stake —
it delivers in a goroutine, with backoff, an attempt cap and the same
poison-message policy as JetStream, because a double that delivered
synchronously and perfectly would hide the bugs that only show up with
asynchronous delivery.

The composition root picks between them by configuration:

§SNIP:wire.go§

`Deps` holds ports, never concrete types, and that `switch` is the only
conditional on a backend in the whole codebase. This is what "chosen at boot,
one active" looks like.

## The contract suite is what makes it true

The second discipline. Two adapters that each pass their own tests are two
adapters; two adapters that pass the *same* tests are substitutable. DOP
keeps one suite per port under `test/contract`, written against the port's
numbered guarantees:

§SNIP:contract_secretstore.go§

The comment at the top records the trap. The first version of this suite
used fixed account names and passed — against the in-memory double, where
every subtest gets a fresh vault. Against a real backend the same vault
persists between subtests, and the secret left behind by subtest 1 broke
subtest 5. The suite had been written on top of the double and carried an
assumption only the double satisfied; no real adapter would pass, and none
was being run. Unique identifiers per run fixed the suite. Running it against
the real thing is what found the bug — which is the point of the next file:

§SNIP:contract_secretstore_test.go§

§FIG4§

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

§FIG2§

Three ways out were on the table. Loosening the guarantee to "eventually
consistent" pushes a reread loop onto every caller, and the caller cannot
tell "not yet" from "never". Caching the value in the process after the
`Put` creates a second place where a credential exists, with its own
invalidation — it trades a consistency problem for a security one. Reading
by version number is the strongly consistent path, but it needs `Put` to
return an identifier the caller keeps; that changes the port, not an adapter,
and it is recorded as a possible evolution rather than rejected.

The decision was that the guarantee holds and the adapter pays:

§SNIP:secretstore_gcp_await.go§

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

§SNIP:delivery_gitprovider.go§

Two interfaces. `GitProvider` is the delivery domain's vocabulary — open,
rebase, merge, and whether the host has a merge queue of its own that DOP's
queue can orchestrate on top of. `GitProviders` resolves which one serves a
given repository. The resolver is implemented in the composition root,
because that is the only place allowed to know all three ends:

§SNIP:app_gitproviders.go§

§FIG3§

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

§SNIP:architecture_test.go§

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
"""

# ---------------------------------------------------------------- the article, PT-BR
PT = """---
title: "Arquitetura hexagonal onde ela compensa: como o DOP mantém os fornecedores atrás de ports"
date: 2026-09-18T08:00:00-04:00
draft: false
translationKey: "hexagonal-architecture-dop"
categories: ["Tecnologia"]
tags: ["dop", "arquitetura-hexagonal", "go", "decisoes-de-arquitetura", "nuvem"]
description: "O núcleo do DOP roda no Cloud Run e num cluster k3s sem mudar uma linha do domínio. O que torna isso verdade não é a estrutura de pastas: dois adapters por port desde o primeiro dia, uma suíte de contrato que todo adapter passa e um teste que quebra o build quando o domínio importa infraestrutura — com o código."
---

O núcleo do DOP precisa rodar em dois lugares que não concordam em nada. No
Google Cloud Run, um segredo mora no Secret Manager e a identidade vem do
Firebase. Num cluster k3s, um segredo é um Secret do Kubernetes e a identidade
vem do provedor OIDC que o cluster tiver. Some a lista que cresce com o
produto — armazenamento de objetos, um broker de mensagens, o executor que
roda o sandbox de um agente, o host git que recebe o pull request — e acoplar
o domínio a qualquer um deles significaria uma reescrita por ambiente.

Arquitetura hexagonal — ports e adapters — é a resposta de manual. É também o
padrão que mais frequentemente termina como o nome de uma pasta: um pacote
`interfaces/`, uma implementação por interface, e um domínio que continua
sabendo o que é um bucket. Este artigo é sobre a versão que o
[DOP](https://dop-t.com/) roda: onde a hexagonal valeu a pena, o que ela
custa, e as três disciplinas que a impedem de apodrecer. O código é real — os
trechos vêm do `dop-core`, o núcleo em Go da plataforma, aparados para
leitura.

## A forma

§FIG1§

Três regiões. `internal/domain` é dono do modelo e declara os ports — o
cofre, o provedor de identidade, o barramento de eventos, o executor, os
repositórios — no seu próprio vocabulário. `internal/adapter` tem um pacote
por tecnologia: Secret Manager e Secret do Kubernetes atrás da mesma
interface, NATS JetStream e um barramento em memória atrás de outra, GitHub e
GitLab atrás de uma terceira. `internal/app` é a raiz de composição: o único
lugar que conhece as duas pontas, onde um valor de configuração escolhe qual
adapter preenche qual port. Do outro lado, o servidor gRPC é o adapter
primário; o BFF em Python e a CLI chegam ao domínio por ele e por nada mais.

Nada disso é novo. O que importa é uma distinção que o diagrama faz e a
maioria das bases de código hexagonais não faz.

## Duas famílias de ports

| | Ports de infraestrutura | Ports de provedor de domínio |
|---|---|---|
| Exemplos | `SecretStore`, `IdentityProvider`, `ObjectStore`, `EventBus`, repositórios | `GitProvider`, `AgentProvider`, `Mailer` |
| Quem escolhe | O ambiente de implantação | A configuração da conta |
| Quando | Uma vez, no boot | A cada requisição |
| Quantos ativos | Um | Vários ao mesmo tempo |

Elas se parecem — uma interface Go, N implementações — e têm ciclos de vida
opostos. Um port de infraestrutura é escolhido pela implantação: uma vez, no
boot, um adapter ativo pela vida do processo. Um port de provedor de domínio
é escolhido pelos dados da conta: a cada requisição, vários adapters ativos
ao mesmo tempo, porque um workspace tem um repositório no GitHub e outro no
GitLab e os dois têm que funcionar. Confundir as duas é o erro típico deste
desenho — um provedor git escolhido por variável de ambiente funciona na demo
e falha, em silêncio, no primeiro cliente com dois hosts. A seção sobre o
provedor git, mais abaixo, mostra como a família por requisição fica em
código.

## Um port na linguagem do domínio

§SNIP:ports_secretstore.go§

Quatro verbos. `SecretRef` é opaco de propósito: o domínio nunca vê um
caminho no Secret Manager nem um namespace no Kubernetes. `SecretValue` não
consegue se imprimir, e é assim que a garantia 6 sobrevive a um `%v`
descuidado. E as garantias estão escritas no port, numeradas, porque são elas
que a suíte de contrato testa — a interface diz quais são os métodos; o
comentário diz o que eles prometem.

Repare no que não está lá: versões. O Secret Manager tem, um Secret do
Kubernetes não tem, e uma capacidade que não mapeia entre adapters fica fora
do port. Se um dia for necessária, entra como capacidade opcional que o
domínio nunca presume.

O caso de uso do outro lado do port sabe exatamente isto:

§SNIP:resource_set_credential.go§

O domínio monta uma referência a partir dos próprios identificadores e chama
`Put`. Ordena o cofre antes da linha por uma razão que ele mesmo escreve, e
não sabe nada sobre para onde os bytes vão.

## Dois adapters desde o primeiro dia

A primeira disciplina: um port com um único adapter é um chute, e sai com o
formato do fornecedor que o inspirou. Por isso o adapter local não é "para
depois" — é escrito junto com o port, e é a prova de que o port está certo.

§SNIP:secretstore_memory.go§

Cinquenta linhas, e não é um mock: copia os bytes na entrada e na saída para
que quem chama não altere o cofre por acidente, e passa exatamente os mesmos
testes que o adapter do GCP. O barramento de eventos em memória é a mesma
história com mais em jogo — entrega numa goroutine, com backoff, teto de
tentativas e a mesma política de mensagem envenenada do JetStream, porque um
dublê que entregasse de forma síncrona e perfeita esconderia os bugs que só
aparecem com entrega assíncrona.

A raiz de composição escolhe entre eles por configuração:

§SNIP:wire.go§

`Deps` guarda ports, nunca tipos concretos, e esse `switch` é o único
condicional sobre backend em toda a base de código. É assim que "escolhido no
boot, um ativo" fica na prática.

## A suíte de contrato é o que torna isso verdade

A segunda disciplina. Dois adapters que passam cada um nos próprios testes
são dois adapters; dois adapters que passam nos *mesmos* testes são
substituíveis. O DOP mantém uma suíte por port em `test/contract`, escrita
contra as garantias numeradas do port:

§SNIP:contract_secretstore.go§

O comentário do topo registra a armadilha. A primeira versão desta suíte
usava nomes de conta fixos e passava — contra o dublê em memória, onde cada
subteste ganha um cofre novo. Contra um backend real o mesmo cofre persiste
entre subtestes, e o segredo deixado pelo subteste 1 quebrou o subteste 5. A
suíte tinha sido escrita em cima do dublê e carregava uma premissa que só o
dublê satisfazia; nenhum adapter real passaria, e nenhum estava sendo
executado. Identificadores únicos por execução consertaram a suíte. Rodá-la
contra a coisa real foi o que achou o bug — e é a razão do arquivo seguinte:

§SNIP:contract_secretstore_test.go§

§FIG4§

A mesma função, três alvos: o adapter em memória sempre, o Kubernetes quando
um cluster responde, o Secret Manager atrás de uma build tag quando existe
credencial. O aviso acima do teste do GCP é merecido: o emulador é mais
permissivo que o Google em nove pontos documentados, e um deles é a primeira
garantia do port.

## Quando o adapter não consegue cumprir a promessa, o adapter paga

O `SecretStore` promete read-after-write. A promessa nasceu do adapter
Kubernetes, onde ela vale — desde que o adapter leia pela API e não por um
volume montado, que o kubelet sincroniza mais ou menos uma vez por minuto. O
adapter do GCP não conseguiu cumpri-la como estava escrita. O Google é
explícito: só a leitura *por número de versão* é fortemente consistente,
enquanto o alias `latest` converge "tipicamente em minutos, mas pode levar
algumas horas". E `SecretRef` é plano; não há onde guardar uma versão.

O modo de falha é o pior que um cofre pode ter. No GCP real, um `Get` logo
depois de um `Put` podia devolver `(nil, nil)` — que, pelo port, significa
"não existe". Uma credencial recém-escrita pareceria ausente, em silêncio, e
quem chamou concluiria que a integração nunca foi configurada. No emulador o
mesmo caso passa em dez milissegundos.

§FIG2§

Três saídas estavam na mesa. Afrouxar a garantia para "eventualmente
consistente" empurra um laço de releitura para cada chamador, e o chamador
não consegue distinguir "ainda não" de "nunca". Guardar o valor em cache no
processo depois do `Put` cria um segundo lugar onde a credencial existe, com
a própria invalidação — troca um problema de consistência por um de
segurança. Ler por número de versão é o caminho fortemente consistente, mas
exige que o `Put` devolva um identificador que o chamador guarda; isso muda o
port, não um adapter, e ficou registrado como evolução possível em vez de
rejeitado.

A decisão foi que a garantia se mantém e o adapter paga:

§SNIP:secretstore_gcp_await.go§

Confirmar a escrita por número de versão, depois esperar o `latest`
alcançar, com um teto, e se não convergir, recusar com um erro explícito.
Recusar é a parte que importa: um `Put` que devolve sucesso enquanto o `Get`
seguinte diz "não encontrado" produz uma integração silenciosamente quebrada;
um `Put` que falha produz um erro que alguém lê. O resíduo também está
escrito — um `Put` no GCP é mais lento e pode falhar por não-convergência,
comportamento que o emulador nunca reproduz, então o teste local não cobre
esse caminho.

É aqui que a hexagonal paga o próprio aluguel. O domínio nunca soube que o
Secret Manager tem um alias, o caso de uso não mudou uma linha, e o lugar
onde a semântica do fornecedor foi absorvida é uma função num adapter.

## A família por requisição: o provedor git

Um pull request vai para o host onde o repositório mora, e o token que o abre
pertence à integração da conta. O domínio de entrega declara o que precisa e
quem resolve:

§SNIP:delivery_gitprovider.go§

Duas interfaces. `GitProvider` é o vocabulário do domínio de entrega — abrir,
rebase, merge, e se o host tem uma fila de merge própria em cima da qual a
fila do DOP pode orquestrar. `GitProviders` resolve qual delas serve um dado
repositório. O resolvedor é implementado na raiz de composição, porque é o
único lugar autorizado a conhecer as três pontas:

§SNIP:app_gitproviders.go§

§FIG3§

Repositório → integração → credencial → adapter, a cada requisição. O adapter
git recebe um token pronto e nunca fica sabendo que existe um cofre; o
domínio de entrega nunca fica sabendo que o GitHub existe; o domínio de
recursos nunca fica sabendo que pull requests existem. Um provedor
desconhecido é uma recusa, não um default, porque abrir um PR no lugar errado
é pior do que não abrir. O port do provedor de agente — Anthropic ou OpenAI,
escolhido por conta — tem exatamente a mesma forma.

## A fronteira é um teste

A terceira disciplina é a mais barata e a mais pulada. Uma regra que mora no
README dura até o primeiro prazo. A do DOP mora na suíte de testes:

§SNIP:architecture_test.go§

Faça o parse dos imports de todo arquivo sob `internal/domain`; falhe em
qualquer pacote de adapter ou SDK de fornecedor. Um segundo teste percorre
todo o resto de `internal/` e falha se qualquer coisa além da raiz de
composição importar um adapter. Os dois rodam em todo `go test ./...`, então
a fronteira quebra o build antes de quebrar o desenho.

## O que custa, e onde não vale o esforço

Dois adapters por port, escritos e mantidos, desde o primeiro commit. Uma
suíte de contrato por port, e a infraestrutura para rodá-la contra os
backends reais, não só contra os emuladores. Uma indireção a mais em toda
chamada de infraestrutura. E o recurso mais forte de um fornecedor — versões
de segredo, IAM por segredo, custom claims do Firebase — inacessível ao
domínio por construção. Esse último é o preço, e é deliberado.

As mesmas regras dizem onde o padrão não compensa. Duas alternativas foram
consideradas para a plataforma como um todo e rejeitadas: acoplar ao GCP
agora e portar depois — "depois" é quando o acoplamento já se espalhou, e
rodar num cluster local era requisito de desenvolvimento, não ambição — e uma
biblioteca multi-cloud genérica, que entrega o denominador comum dos
fornecedores *da biblioteca*, não do domínio, e troca um acoplamento por
outro. Mas dentro da fronteira, o DOP não põe um port na frente de consultas
Postgres que só vão rodar no Postgres, não abstrai a borda gRPC e não
embrulha o logger. Um port vale a pena onde o segundo adapter é real: um
segundo ambiente, um segundo host que o cliente pode escolher, um teste que
precisa rodar sem infraestrutura. Onde o segundo adapter é imaginário, a
interface é o nome de uma pasta.

A hexagonal, no fim, é uma regra contábil: o domínio não paga nada ao
fornecedor, e o adapter paga o que o fornecedor cobrar. As três disciplinas
são o que mantém os livros honestos.
"""

def render(text, lang):
    L = LANG[lang]
    text = text.replace("§FIG1§", fig_shape(L)).replace("§FIG2§", fig_pays(L)) \
               .replace("§FIG3§", fig_provider(L)).replace("§FIG4§", fig_suite(L))
    import re
    return re.sub(r"§SNIP:([^§]+)§", lambda m: snip(m.group(1)), text)

(SITE / "en/writing/hexagonal-architecture-dop.md").write_text(render(EN, "en"))
(SITE / "pt-br/artigos/arquitetura-hexagonal-dop.md").write_text(render(PT, "pt-br"))
print("written")
