#!/usr/bin/env python3
"""Generates the hexagonal-architecture article (DOP) in EN and PT-BR with identical SVG figures."""
from pathlib import Path

SITE = Path(__file__).resolve().parents[2] / "content"

# ---------------------------------------------------------------- drawing primitives
# The column renders at ~600px, so the canvas is 720 wide and labels are
# 12.5–14px: legible at the size people actually read them. One memorable
# element per figure (the navy domain); everything else white cards on soft
# zones. Legends live in the figcaption, not inside the picture.
NAVY = "#1d4e89"
NAVY_DEEP = "#173d6e"
INK = "#16233a"
MUTED = "#5d6b7d"
ZONE = "#eef2f7"
ZONE_LINE = "#d5dde8"
CARD_LINE = "#b9c5d4"
FORBID = "#b3261e"
SANS = "IBM Plex Sans, system-ui, sans-serif"
MONO_F = "IBM Plex Mono, ui-monospace, monospace"

def T(x, y, text, size=13, color=INK, anchor="start", weight=400, mono=False, italic=False):
    ff = f' font-family="{MONO_F}"' if mono else ""
    it = ' font-style="italic"' if italic else ""
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-size="{size}" font-weight="{weight}" fill="{color}"{ff}{it}>{text}</text>'

def zone(x, y, w, h, title=None, fill=ZONE, line=ZONE_LINE, dash=False):
    d = ' stroke-dasharray="6 5"' if dash else ""
    out = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{fill}" stroke="{line}" stroke-width="1"{d}/>'
    if title:
        out += T(x + 16, y + 24, title, size=12.5, color=MUTED, weight=600)
    return out

def card(x, y, w, h, title, sub=None, fill="#fff", line=CARD_LINE, tcolor=INK, scolor=MUTED, sub_mono=False, dash=False, weight=600, size=13):
    d = ' stroke-dasharray="6 5"' if dash else ""
    out = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{fill}" stroke="{line}" stroke-width="1.2"{d}/>'
    cx = x + w / 2
    if sub:
        out += T(cx, y + h / 2 - 3, title, size=size, color=tcolor, anchor="middle", weight=weight)
        out += T(cx, y + h / 2 + 14, sub, size=11, color=scolor, anchor="middle", mono=sub_mono)
    else:
        out += T(cx, y + h / 2 + 5, title, size=size, color=tcolor, anchor="middle", weight=weight)
    return out

def chip(x, y, text, w=None, fill="#fff", line=CARD_LINE, color=INK, size=11):
    w = w or int(len(text) * size * 0.62 + 18)
    return (f'<rect x="{x}" y="{y}" width="{w}" height="22" rx="11" fill="{fill}" stroke="{line}" stroke-width="1"/>'
            + T(x + w / 2, y + 15, text, size=size, color=color, anchor="middle", mono=True)), w

def link(pts, color=INK, dash=False, head=True, width=1.6):
    d = ' stroke-dasharray="6 5"' if dash else ""
    m = {INK: "h-ink", NAVY: "h-navy", FORBID: "h-forbid", MUTED: "h-muted"}.get(color, "h-ink")
    mk = f' marker-end="url(#{m})"' if head else ""
    pth = "M " + " L ".join(f"{x},{y}" for x, y in pts)
    return f'<path d="{pth}" fill="none" stroke="{color}" stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round"{d}{mk}/>'

def socket(x, y, r=6):
    # a port: a white socket on the hexagon's edge
    return f'<rect x="{x - r}" y="{y - r}" width="{2*r}" height="{2*r}" rx="2" fill="#fff" stroke="{NAVY}" stroke-width="1.6"/>'

def marker(mid, color):
    return (f'<marker id="{mid}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
            f'<path d="M1,1 L9,5 L1,9 z" fill="{color}"/></marker>')

DEFS = "<defs>" + marker("h-ink", INK) + marker("h-navy", NAVY) + marker("h-forbid", FORBID) + marker("h-muted", MUTED) + "</defs>"

def figure(w, h, body, caption, aria):
    # No blank lines inside: Goldmark ends an HTML block at the first blank line.
    return (f'<figure class="diagram"><svg viewBox="0 0 {w} {h}" role="img" aria-label="{aria}" '
            f'xmlns="http://www.w3.org/2000/svg" font-family="{SANS}" color="{INK}">'
            f'{DEFS}{body}</svg><figcaption>{caption}</figcaption></figure>')

def curve(x1, y1, x2, y2, color=NAVY, width=1.2):
    c = (x2 - x1) * 0.5
    return (f'<path d="M {x1},{y1} C {x1 + c},{y1} {x2 - c},{y2} {x2},{y2}" fill="none" '
            f'stroke="{color}" stroke-width="{width}" stroke-linecap="round"/>')

# ---------------------------------------------------------------- figure 1: the shape
def fig_shape(L):
    b = ""
    cx, cy, R = 306, 222, 96
    hx = [(cx - R * 0.5, cy - R * 0.87), (cx + R * 0.5, cy - R * 0.87), (cx + R, cy),
          (cx + R * 0.5, cy + R * 0.87), (cx - R * 0.5, cy + R * 0.87), (cx - R, cy)]
    b += zone(16, 60, 190, 330, L["driving"])
    b += zone(420, 60, 284, 330, L["driven"])
    pts = " ".join(f"{x:.1f},{y:.1f}" for x, y in hx)
    b += f'<polygon points="{pts}" fill="{NAVY}" stroke="{NAVY_DEEP}" stroke-width="1.5"/>'
    b += T(cx, cy - 30, "internal/domain", size=14.5, color="#fff", anchor="middle", weight=600)
    b += T(cx, cy - 11, L["domain_sub"], size=11, color="#cfe0f5", anchor="middle")
    for i, ln in enumerate(L["domain_lines"]):
        b += T(cx, cy + 14 + i * 16, ln, size=10.5, color="#e8f0fa", anchor="middle", mono=True)
    # driving side: two callers, one edge, one socket on the left vertex
    b += card(32, 104, 110, 50, "dop-api", L["bff_sub"])
    b += card(32, 176, 110, 50, "dop-cmd", L["cli_sub"])
    b += card(150, 138, 50, 56, L["edge"], "gRPC", sub_mono=True)
    b += link([(142, 129), (150, 152)])
    b += link([(142, 201), (150, 180)])
    b += link([(200, 166), (204, 214)], color=NAVY, head=False)
    b += socket(hx[5][0], hx[5][1])
    b += T(32, 262, L["driving_note1"], size=11.5, color=MUTED)
    b += T(32, 279, L["driving_note2"], size=11.5, color=MUTED)
    b += T(32, 296, L["driving_note3"], size=11.5, color=MUTED)
    # driven side: sockets spread along the right edges, one curve per port row
    rows_a = [("SecretStore", ["memory", "k8s", "gcp"]), ("EventBus", ["memory", "nats"]),
              ("IdentityProvider", ["firebase", "oidc"]), ("SandboxLauncher", ["docker", "k8s"])]
    rows_b = [("GitProvider", ["github", "gitlab"]), ("AgentProvider", ["anthropic", "openai"]), ("Mailer", ["smtp", "sendgrid"])]
    b += T(436, 108, L["family_a"], size=11.5, color=NAVY, weight=600)
    b += T(436, 280, L["family_b"], size=11.5, color=NAVY, weight=600)
    def edge_x(y):
        top, mid, bot = hx[1], hx[2], hx[3]
        if y <= mid[1]:
            return top[0] + (mid[0] - top[0]) * (y - top[1]) / (mid[1] - top[1])
        return mid[0] - (mid[0] - bot[0]) * (y - mid[1]) / (bot[1] - mid[1])
    rows = [(n, a, 132 + i * 34) for i, (n, a) in enumerate(rows_a)] + [(n, a, 304 + i * 34) for i, (n, a) in enumerate(rows_b)]
    for i, (name, adapters, ry) in enumerate(rows):
        sy = 152 + i * 24
        sx = edge_x(sy)
        b += curve(sx + 7, sy, 428, ry)
        b += socket(sx, sy, r=5)
        b += T(436, ry + 4, name, size=11.5, color=INK, weight=600, mono=True)
        x = 436 + int(len(name) * 7.1) + 10
        for a in adapters:
            w = int(len(a) * 6.4 + 16)
            b += f'<rect x="{x}" y="{ry - 11}" width="{w}" height="22" rx="11" fill="#fff" stroke="{CARD_LINE}" stroke-width="1"/>'
            b += T(x + w / 2, ry + 4, a, size=10.5, color=INK, anchor="middle", mono=True)
            x += w + 6
    # the composition root
    b += zone(16, 404, 688, 44, fill="#fff", line=CARD_LINE, dash=True)
    b += T(32, 431, "internal/app", size=13, weight=600, mono=True)
    b += T(140, 431, L["root_note"], size=12, color=MUTED)
    return figure(720, 464, b, L["fig1_caption"], L["fig1_aria"])

# ---------------------------------------------------------------- figure 2: the adapter pays
def fig_pays(L):
    b = ""
    b += card(16, 16, 250, 48, "SecretStore.Put", L["promise"], sub_mono=False, fill=NAVY, line=NAVY_DEEP, tcolor="#fff", scolor="#cfe0f5")
    # lane 1: memory
    b += zone(16, 88, 688, 88, L["lane_mem"])
    b += card(32, 122, 150, 40, "map[key] = copy", None, weight=400, size=12.5)
    b += link([(182, 142), (208, 142)])
    b += card(210, 122, 110, 40, "return nil", None, weight=400, size=12.5)
    b += T(340, 147, L["mem_note"], size=12, color=MUTED, italic=True)
    # lane 2: GCP
    b += zone(16, 192, 688, 246, L["lane_gcp"])
    steps = [("AddSecretVersion", L["s1"]), ("confirm v = n", L["s2"]), ("await latest ≥ n", L["s3"]), ("destroyOlder", L["s4"])]
    W, G, y = 138, 18, 226
    for i, (t, s) in enumerate(steps):
        x = 32 + i * (W + G)
        hot = i == 2
        b += card(x, y, W, 52, t, s, weight=600 if hot else 500, size=12.5,
                  fill=NAVY if hot else "#fff", line=NAVY_DEEP if hot else CARD_LINE,
                  tcolor="#fff" if hot else INK, scolor="#cfe0f5" if hot else MUTED)
        b += link([(x + W + 2, y + 26), (x + W + G - 2, y + 26)])
    b += card(656, y, 34, 52, "✓", None, weight=600, size=16, fill="#fff")
    # under the hot step: the retry loop (left) and the way out (right)
    hx0 = 32 + 2 * (W + G)
    b += link([(hx0 + 30, y + 54), (hx0 + 30, y + 76), (hx0 + 12, y + 76), (hx0 + 12, y + 56)], color=NAVY, width=1.3)
    b += T(hx0 + 2, y + 80, L["loop"], size=11, color=NAVY, mono=True, anchor="end")
    b += link([(hx0 + W - 24, y + 54), (hx0 + W - 24, y + 112)], color=NAVY, dash=True, width=1.3)
    rx = hx0 + W - 24 - 80
    b += card(rx, y + 114, 160, 44, "KindUnavailable", L["refuse_sub"], line=NAVY, tcolor=NAVY, weight=600, size=12.5)
    b += T(rx + 80, y + 178, L["refuse_note1"], size=11.5, color=MUTED, anchor="middle")
    b += T(rx + 80, y + 194, L["refuse_note2"], size=11.5, color=MUTED, anchor="middle")
    return figure(720, 454, b, L["fig2_caption"], L["fig2_aria"])

# ---------------------------------------------------------------- figure 3: per-request provider
def fig_provider(L):
    b = ""
    b += card(16, 60, 160, 64, "domain/delivery", L["dl_sub"], fill=NAVY, line=NAVY_DEEP, tcolor="#fff", scolor="#cfe0f5")
    b += link([(176, 92), (206, 92)], color=NAVY)
    b += T(96, 146, "For(account, repo)", size=11, color=NAVY, anchor="middle", mono=True)
    # the resolver zone with three steps
    b += zone(208, 24, 320, 172, "internal/app · gitProviders.For")
    steps = [("1", L["r1_t"], L["r1_s"]), ("2", L["r2_t"], L["r2_s"]), ("3", L["r3_t"], L["r3_s"])]
    for i, (n, t, s) in enumerate(steps):
        x = 222 + i * 100
        b += card(x, 56, 92, 52, t, s, weight=600, size=12.5)
        if i < 2:
            b += link([(x + 94, 82), (x + 98, 82)], head=False)
    b += T(222, 138, L["per_request"], size=11.5, color=NAVY, weight=600)
    b += T(222, 156, L["refusal1"], size=11.5, color=MUTED)
    b += T(222, 172, L["refusal2"], size=11.5, color=MUTED)
    # adapters
    b += card(548, 36, 156, 52, "GitHub", L["gh_sub"])
    b += card(548, 108, 156, 52, "GitLab", L["gl_sub"])
    b += link([(528, 82), (546, 62)], color=NAVY)
    b += link([(528, 110), (546, 134)], color=NAVY)
    b += T(632, 180, L["adapter_note"], size=11, color=MUTED, anchor="middle", italic=True)
    # the vault, read inside the resolver
    b += link([(468, 110), (468, 224)], color=INK, head=True, width=1.3)
    b += T(476, 214, "Get(ref)", size=11, color=MUTED, mono=True)
    b += card(388, 226, 160, 48, "ports.SecretStore", L["vault_sub"])
    b += T(16, 232, L["k1"], size=12, color=MUTED)
    b += T(16, 250, L["k2"], size=12, color=MUTED)
    b += T(16, 268, L["k3"], size=12, color=MUTED)
    return figure(720, 290, b, L["fig3_caption"], L["fig3_aria"])

# ---------------------------------------------------------------- figure 4: one suite, three adapters, the frontier
def fig_suite(L):
    b = ""
    b += card(16, 44, 190, 70, "SecretStoreSuite", L["suite_sub"], fill=NAVY, line=NAVY_DEEP, tcolor="#fff", scolor="#cfe0f5")
    b += T(111, 132, "test/contract/secretstore.go", size=10.5, color=MUTED, anchor="middle", mono=True)
    targets = [("memory", L["t_mem"], False), ("k8s", L["t_k8s"], False), ("gcp", L["t_gcp"], True)]
    for i, (name, cond, dash) in enumerate(targets):
        y = 24 + i * 52
        b += link([(206, 79), (240, 79), (262, y + 22), (282, y + 22)], color=NAVY, width=1.4)
        b += card(284, y, 110, 44, name, None, dash=dash, weight=600)
        b += T(408, y + 27, cond, size=12, color=MUTED)
    b += T(284, 194, L["same_fn"], size=12, color=NAVY, weight=600)
    # the frontier: three columns, allowed in navy, forbidden in red
    b += zone(16, 226, 688, 150, L["guards"])
    cols = [("internal/domain", L["g_dom"], 40), ("internal/adapter", L["g_ad"], 290), ("SDKs", "pgx · nats · gcp · k8s", 540)]
    for name, sub, x in cols:
        b += card(x, 262, 150, 52, name, sub, sub_mono=(name == "SDKs"), weight=600, size=12.5)
    b += link([(440, 288), (538, 288)], color=NAVY)          # adapter → SDK: allowed
    b += T(489, 280, L["allowed"], size=10.5, color=NAVY, anchor="middle")
    b += link([(290, 276), (192, 276)], color=NAVY)          # adapter → domain (ports): allowed
    b += T(241, 268, L["implements"], size=10.5, color=NAVY, anchor="middle")
    b += link([(192, 300), (290, 300)], color=FORBID, dash=True)  # domain → adapter: forbidden
    b += T(241, 322, L["forbidden"], size=10.5, color=FORBID, anchor="middle", weight=600)
    b += T(40, 350, L["g_note1"], size=11.5, color=MUTED)
    b += T(40, 366, L["g_note2"], size=11.5, color=MUTED)
    return figure(720, 392, b, L["fig4_caption"], L["fig4_aria"])

# ---------------------------------------------------------------- figure text
LANG = {
    "en": dict(
        driving="drives the domain", driven="driven by the domain",
        domain_sub="model · use cases · ports", domain_lines=["demand · delivery", "execution · resource", "identity · …"],
        bff_sub="Python BFF", cli_sub="CLI", edge="edge",
        driving_note1="The BFF and the CLI reach the", driving_note2="domain only through gRPC —", driving_note3="the one driving adapter.",
        family_a="infrastructure · chosen at boot, one active", family_b="providers · per request, several active",
        root_note="the composition root — knows both ends; configuration picks each adapter",
        fig1_caption="The three regions of dop-core. The domain declares the ports (the sockets on its edges); each adapter package plugs into one; the composition root does the plugging, by configuration. The two families on the right have opposite life cycles.",
        fig1_aria="The BFF and the CLI reach a navy hexagon labelled internal/domain through a gRPC edge; on the right, ports drawn as sockets on the hexagon's edge connect to rows of adapter chips, grouped as infrastructure ports chosen at boot and domain provider ports chosen per request; a composition root band underneath.",
        promise="the promise: read-after-write", lane_mem="in-memory adapter", mem_note="the promise costs nothing here",
        lane_gcp="Secret Manager adapter", s1="version n created", s2="by number — strong", s3="alias — eventual", s4="old material gone",
        loop="retry · 25 ms → 1 s · ≤ 30 s", refuse_sub="past the ceiling",
        refuse_note1="write accepted, read-after-write not confirmed:", refuse_note2="an error somebody reads, not a Get saying \"absent\".",
        fig2_caption="The same Put through two adapters. In memory the promise is free. On Secret Manager the adapter confirms by version number, waits for the alias to catch up — the highlighted step — and past the ceiling refuses rather than lie.",
        fig2_aria="Two lanes for SecretStore.Put: the in-memory adapter writes a map and returns; the Secret Manager adapter adds a version, confirms it by number, waits for the latest alias with retries, destroys older versions and returns, or refuses with KindUnavailable past the ceiling.",
        dl_sub="opens the PR", r1_t="repository", r1_s="→ integration", r2_t="integration", r2_s="→ provider", r3_t="vault", r3_s="→ token",
        per_request="resolved on every request", refusal1="unknown provider: a refusal,", refusal2="never a default",
        gh_sub="GraphQL · merge queue", gl_sub="REST · merge trains", adapter_note="the token arrives ready-made",
        vault_sub="read here, in the core",
        k1="The delivery domain never learns GitHub exists.", k2="The git adapter never learns a vault exists.", k3="The resource domain never learns PRs exist.",
        fig3_caption="A per-request port. The delivery domain asks for a provider by repository; the composition root resolves integration and credential and returns a ready adapter — GitHub for one repository, GitLab for the next.",
        fig3_aria="The delivery domain calls For with account and repository; inside the composition root three steps resolve repository, integration and vault; a GitHub or GitLab adapter is returned per call; the vault is read inside the resolver.",
        suite_sub="six numbered guarantees", t_mem="always", t_k8s="when a cluster answers", t_gcp="behind a build tag, when a credential exists",
        same_fn="one function, three targets",
        guards="the frontier, guarded by two tests on every go test ./...", g_dom="declares the ports", g_ad="implements them",
        allowed="allowed", implements="implements", forbidden="never",
        g_note1="TestTheDomainDoesNotImportInfrastructure — nothing under internal/domain imports an adapter or an SDK.",
        g_note2="TestOnlyAppKnowsTheAdapters — outside internal/app, nothing imports internal/adapter.",
        fig4_caption="What keeps the pattern true over time. Above: one contract suite runs against every adapter. Below: the import frontier — adapters may know the domain and the SDKs; the domain may know neither — enforced by tests that break the build.",
        fig4_aria="The SecretStore contract suite fans out to three adapters: memory always, k8s when a cluster answers, GCP behind a build tag; below, three columns for domain, adapter and SDKs, with allowed arrows from adapter to domain and to SDKs, and a red dashed forbidden arrow from domain to adapter.",
    ),
    "pt-br": dict(
        driving="aciona o domínio", driven="acionado pelo domínio",
        domain_sub="modelo · casos de uso · ports", domain_lines=["demand · delivery", "execution · resource", "identity · …"],
        bff_sub="BFF Python", cli_sub="CLI", edge="borda",
        driving_note1="O BFF e a CLI chegam ao", driving_note2="domínio só por gRPC —", driving_note3="o único adapter primário.",
        family_a="infraestrutura · no boot, um ativo", family_b="provedores · por requisição, vários ativos",
        root_note="a raiz de composição — conhece as duas pontas; a configuração escolhe cada adapter",
        fig1_caption="As três regiões do dop-core. O domínio declara os ports (as tomadas nas suas bordas); cada pacote de adapter se liga a uma; a raiz de composição faz a ligação, por configuração. As duas famílias à direita têm ciclos de vida opostos.",
        fig1_aria="O BFF e a CLI chegam a um hexágono azul-marinho rotulado internal/domain por uma borda gRPC; à direita, ports desenhados como tomadas na borda do hexágono ligam-se a fileiras de chips de adapters, agrupados em ports de infraestrutura escolhidos no boot e ports de provedor escolhidos por requisição; uma faixa de raiz de composição embaixo.",
        promise="a promessa: read-after-write", lane_mem="adapter em memória", mem_note="aqui a promessa não custa nada",
        lane_gcp="adapter Secret Manager", s1="versão n criada", s2="por número — forte", s3="alias — eventual", s4="material antigo destruído",
        loop="retry · 25 ms → 1 s · ≤ 30 s", refuse_sub="passado o teto",
        refuse_note1="escrita aceita, read-after-write não confirmado:", refuse_note2="um erro que alguém lê, não um Get dizendo \"não existe\".",
        fig2_caption="O mesmo Put por dois adapters. Em memória a promessa é de graça. No Secret Manager o adapter confirma por número de versão, espera o alias alcançar — o passo destacado — e, passado o teto, recusa em vez de mentir.",
        fig2_aria="Duas raias para SecretStore.Put: o adapter em memória escreve num map e retorna; o adapter Secret Manager cria uma versão, confirma por número, espera o alias latest com retries, destrói versões antigas e retorna, ou recusa com KindUnavailable passado o teto.",
        dl_sub="abre o PR", r1_t="repositório", r1_s="→ integração", r2_t="integração", r2_s="→ provedor", r3_t="cofre", r3_s="→ token",
        per_request="resolvido a cada requisição", refusal1="provedor desconhecido: recusa,", refusal2="nunca um default",
        gh_sub="GraphQL · merge queue", gl_sub="REST · merge trains", adapter_note="o token chega pronto",
        vault_sub="lido aqui, no core",
        k1="O domínio de entrega nunca fica sabendo que o GitHub existe.", k2="O adapter git nunca fica sabendo que existe um cofre.", k3="O domínio de recursos nunca fica sabendo que PRs existem.",
        fig3_caption="Um port por requisição. O domínio de entrega pede um provedor por repositório; a raiz de composição resolve integração e credencial e devolve um adapter pronto — GitHub para um repositório, GitLab para o seguinte.",
        fig3_aria="O domínio de entrega chama For com conta e repositório; dentro da raiz de composição três passos resolvem repositório, integração e cofre; um adapter GitHub ou GitLab é devolvido por chamada; o cofre é lido dentro do resolvedor.",
        suite_sub="seis garantias numeradas", t_mem="sempre", t_k8s="quando um cluster responde", t_gcp="atrás de uma build tag, quando há credencial",
        same_fn="uma função, três alvos",
        guards="a fronteira, guardada por dois testes em todo go test ./...", g_dom="declara os ports", g_ad="os implementa",
        allowed="permitido", implements="implementa", forbidden="nunca",
        g_note1="TestTheDomainDoesNotImportInfrastructure — nada sob internal/domain importa um adapter ou um SDK.",
        g_note2="TestOnlyAppKnowsTheAdapters — fora de internal/app, nada importa internal/adapter.",
        fig4_caption="O que mantém o padrão verdadeiro ao longo do tempo. Em cima: uma suíte de contrato roda contra todo adapter. Embaixo: a fronteira de imports — adapters podem conhecer o domínio e os SDKs; o domínio não conhece nenhum dos dois — imposta por testes que quebram o build.",
        fig4_aria="A suíte de contrato do SecretStore se abre em três adapters: memória sempre, k8s quando um cluster responde, GCP atrás de uma build tag; embaixo, três colunas para domínio, adapter e SDKs, com setas permitidas do adapter para o domínio e para os SDKs, e uma seta tracejada vermelha proibida do domínio para o adapter.",
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
