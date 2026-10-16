#!/usr/bin/env python3
"""Figures for "The Culture You Can Install" / "A Cultura que se Instala" (EN + PT-BR).

Three inline SVGs, identical in both languages except for the text:
  layers  — what foreman installs: the culture (same everywhere) and the project's five records
  roles   — the four roles around the cycle, the tooling, DEV and the human at both ends
  tooling — how the culture meets the project's tool: one verb per repetitive action

The markdown keeps a marker line before each figure; this script replaces the line that
follows the marker. Edit here, run, commit both.
"""
import re
from pathlib import Path

SITE = Path(__file__).resolve().parents[2] / "content"
FILES = {
    "en": SITE / "en" / "writing" / "the-culture-you-can-install.md",
    "pt-br": SITE / "pt-br" / "artigos" / "a-cultura-que-se-instala.md",
}

# ---------------------------------------------------------------- drawing primitives (site palette)
NAVY = "#1d4e89"
NAVY_DEEP = "#173d6e"
NAVY_SOFT = "#5b8fd6"
INK = "#16233a"
MUTED = "#5d6b7d"
ZONE = "#eef2f7"
ZONE_LINE = "#d5dde8"
CARD_LINE = "#b9c5d4"
GOLD = "#b7791f"
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
        out += T(x + 16, y + 22, title, size=12, color=MUTED, weight=600)
    return out


def card(x, y, w, h, title, sub=None, sub2=None, fill="#fff", line=CARD_LINE, tcolor=INK, scolor=MUTED, weight=600, size=13, dash=False):
    d = ' stroke-dasharray="6 5"' if dash else ""
    out = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{fill}" stroke="{line}" stroke-width="1.2"{d}/>'
    cx = x + w / 2
    if sub and sub2:
        out += T(cx, y + h / 2 - 9, title, size=size, color=tcolor, anchor="middle", weight=weight)
        out += T(cx, y + h / 2 + 7, sub, size=10.5, color=scolor, anchor="middle")
        out += T(cx, y + h / 2 + 21, sub2, size=10.5, color=scolor, anchor="middle")
    elif sub:
        out += T(cx, y + h / 2 - 3, title, size=size, color=tcolor, anchor="middle", weight=weight)
        out += T(cx, y + h / 2 + 14, sub, size=10.5, color=scolor, anchor="middle")
    else:
        out += T(cx, y + h / 2 + 5, title, size=size, color=tcolor, anchor="middle", weight=weight)
    return out


def navy_card(x, y, w, h, title, sub=None, sub2=None, size=13):
    return card(x, y, w, h, title, sub, sub2, fill=NAVY, line=NAVY_DEEP, tcolor="#fff", scolor="#cfe0f5", size=size)


def chip(x, y, text, w=None, fill="#fff", line=CARD_LINE, color=INK, size=11):
    w = w or int(len(text) * size * 0.56 + 14)
    return (f'<rect x="{x}" y="{y}" width="{w}" height="22" rx="11" fill="{fill}" stroke="{line}" stroke-width="1"/>'
            + T(x + w / 2, y + 15, text, size=size, color=color, anchor="middle")), w


def link(pts, color=INK, dash=False, head=True, width=1.6):
    d = ' stroke-dasharray="6 5"' if dash else ""
    m = {INK: "h-ink", NAVY: "h-navy", MUTED: "h-muted", GOLD: "h-gold"}.get(color, "h-ink")
    mk = f' marker-end="url(#{m})"' if head else ""
    pth = "M " + " L ".join(f"{x},{y}" for x, y in pts)
    return f'<path d="{pth}" fill="none" stroke="{color}" stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round"{d}{mk}/>'


def label(x, y, text, color=MUTED, anchor="start", size=11, weight=400):
    return T(x, y, text, size=size, color=color, anchor=anchor, weight=weight)


def marker(mid, color):
    return (f'<marker id="{mid}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
            f'<path d="M1,1 L9,5 L1,9 z" fill="{color}"/></marker>')


DEFS = "<defs>" + marker("h-ink", INK) + marker("h-navy", NAVY) + marker("h-muted", MUTED) + marker("h-gold", GOLD) + "</defs>"


def figure(w, h, body, caption, aria):
    # No blank lines inside: Goldmark ends an HTML block at the first blank line.
    return (f'<figure class="diagram"><svg viewBox="0 0 {w} {h}" role="img" aria-label="{aria}" '
            f'xmlns="http://www.w3.org/2000/svg" font-family="{SANS}" color="{INK}">'
            f'{DEFS}{body}</svg><figcaption>{caption}</figcaption></figure>')


# ---------------------------------------------------------------- text, per language
L = {
    "en": dict(
        # figure 1
        f1_top="the install, in three passes",
        f1_detect="detects", f1_detect_s="reads only what the project tracks",
        f1_ask="asks", f1_ask_s="five questions at most, answer marked",
        f1_write="writes", f1_write_s="never over a byte that was there",
        f1_left="the culture · identical in every project",
        f1_rules="the rules", f1_rules_s="principles, the cycle,", f1_rules_s2="one human gate",
        f1_roles="four roles as contracts", f1_roles_s="architect · reviewer ·", f1_roles_s2="executors · quality team",
        f1_mech="the mechanism", f1_mech_s="roles → agents ·", f1_mech_s2="capability and effort per role",
        f1_agents="five agents, copied in, yours to tune",
        f1_right="the project · filled at install",
        f1_r1="repositories", f1_r1_s="what exists and how it relates",
        f1_r2="delivery", f1_r2_s="branches, pull requests, what DEV means",
        f1_r3="environment", f1_r3_s="up, down, test",
        f1_r4="demands", f1_r4_s="where a request lives, how it moves",
        f1_r5="quality", f1_r5_s="test layers, the team, reports",
        f1_leg="each value says how it was filled:",
        f1_c1="detected", f1_c2="answered", f1_c3="default",
        f1_cap="What two steps leave behind. The culture on the left is the same in every project and names no vendor; the five records on the right are the project's own, filled at install from what was detected, answered or defaulted, and edited freely afterwards.",
        f1_aria="Diagram of what foreman installs: a top band with three passes, detect, ask and write; a left zone with the culture, rules, four roles and the mechanism plus five agents; a right zone with the five records, each marked as detected, answered or default.",
        # figure 2
        f2_req="the request", f2_req_s="stated by a human: what and why",
        f2_arch="the architect", f2_arch_s="reads, doubts, specifies, splits, judges", f2_arch_s2="the only one who sees the whole request",
        f2_rev="the reviewer", f2_rev_s="objects before anything is built", f2_rev_s2="at the architect's own level",
        f2_exec="executors", f2_reader="reader", f2_reader_s="one bounded question", f2_builder="builder", f2_builder_s="one bounded change",
        f2_qa="quality team", f2_lead="the lead", f2_lead_s="sizes and judges the attack", f2_tester="tester",
        f2_tool="the project's tooling", f2_tool_s="delivery, with the verdict attached",
        f2_dev="DEV", f2_dev_s="where it runs",
        f2_human="the human", f2_human_s="sees it working · says done",
        f2_l1="1 read and doubt", f2_l2="2 the plan", f2_l3="3 objections", f2_l4="4 a task with a boundary",
        f2_l5="5 attack", f2_l6="6 deliver", f2_l7="7 · 8",
        f2_cap="The four roles around one request. The human states it and, at the end, says it is done; nothing in between waits for permission. The reviewer objects before any work, the executors never widen a task, the quality team never fixes what it finds, and delivery goes out through the project's own tooling.",
        f2_aria="Diagram of the cycle: a human states the request; the architect in the centre sends the plan to the reviewer and receives objections, dispatches a reader and a builder with bounded tasks, calls the quality lead who dispatches testers, delivers through the project's tooling into DEV, where the human sees it working and says done.",
        # figure 3
        f3_roles="the roles", f3_a="architect", f3_a_s="decides, delivers", f3_b="builders", f3_b_s="change code", f3_q="quality team", f3_q_s="runs the attack",
        f3_tool="the project's tool", f3_tool_s="one verb per action",
        f3_v1="up · down · test · logs", f3_v2="branch · deliver", f3_v3="move the request",
        f3_env="the local environment", f3_env_s="up, down, test, reset",
        f3_del="delivery", f3_del_s="branches, pull requests, DEV",
        f3_dem="the request", f3_dem_s="states move on delivery events",
        f3_human="the human", f3_human_s="sees it working in DEV · says done",
        f3_rec_env="environment record", f3_rec_del="delivery record", f3_rec_dem="demands record",
        f3_cmd="commands",
        f3_rule="a missing verb is a gap to report, not a reason to improvise",
        f3_cap="Governance through tooling, not discipline. Every repetitive operation is a verb of a tool the project owns; the records say which verbs exist and what each one touches. When the tool has a verb for an action, the action never happens by hand.",
        f3_aria="Diagram of the culture meeting the tooling: the roles send commands to the project's tool, which alone acts on the local environment, on delivery and on the request's states; delivery reaches DEV, where the human sees the work and says done. Each target is named by one record.",
    ),
    "pt-br": dict(
        f1_top="a instalação, em três passagens",
        f1_detect="detecta", f1_detect_s="lê só o que o projeto versiona",
        f1_ask="pergunta", f1_ask_s="até cinco, resposta já marcada",
        f1_write="escreve", f1_write_s="nunca por cima do que já existia",
        f1_left="a cultura · idêntica em todo projeto",
        f1_rules="as regras", f1_rules_s="princípios, o ciclo,", f1_rules_s2="um portão humano",
        f1_roles="quatro papéis como contratos", f1_roles_s="arquiteto · revisor ·", f1_roles_s2="executores · time de qualidade",
        f1_mech="o mecanismo", f1_mech_s="papéis → agentes ·", f1_mech_s2="capacidade e esforço por papel",
        f1_agents="cinco agentes, copiados, seus para ajustar",
        f1_right="o projeto · preenchido na instalação",
        f1_r1="repositórios", f1_r1_s="o que existe e como se relaciona",
        f1_r2="entrega", f1_r2_s="ramos, pull requests, o que é DEV",
        f1_r3="ambiente", f1_r3_s="subir, derrubar, testar",
        f1_r4="demandas", f1_r4_s="onde um pedido mora, como se move",
        f1_r5="qualidade", f1_r5_s="camadas de teste, o time, relatórios",
        f1_leg="cada valor diz como foi preenchido:",
        f1_c1="detectado", f1_c2="respondido", f1_c3="padrão",
        f1_cap="O que dois passos deixam para trás. A cultura, à esquerda, é a mesma em todo projeto e não nomeia fornecedor; os cinco registros, à direita, são do projeto, preenchidos na instalação com o que foi detectado, respondido ou assumido por padrão, e editados livremente depois.",
        f1_aria="Diagrama do que o foreman instala: uma faixa superior com três passagens, detecta, pergunta e escreve; uma zona à esquerda com a cultura, regras, quatro papéis e o mecanismo mais cinco agentes; uma zona à direita com os cinco registros, cada um marcado como detectado, respondido ou padrão.",
        f2_req="o pedido", f2_req_s="por um humano: o quê e o porquê",
        f2_arch="o arquiteto", f2_arch_s="lê, duvida, especifica, divide, julga", f2_arch_s2="o único que vê o pedido inteiro",
        f2_rev="o revisor", f2_rev_s="objeta antes de qualquer trabalho", f2_rev_s2="no mesmo nível do arquiteto",
        f2_exec="executores", f2_reader="leitor", f2_reader_s="uma pergunta delimitada", f2_builder="construtor", f2_builder_s="uma mudança delimitada",
        f2_qa="time de qualidade", f2_lead="o líder", f2_lead_s="dimensiona e dá o veredito", f2_tester="testador",
        f2_tool="o ferramental do projeto", f2_tool_s="entrega, com o veredito anexado",
        f2_dev="DEV", f2_dev_s="onde roda",
        f2_human="o humano", f2_human_s="vê funcionando · diz pronto",
        f2_l1="1 ler e duvidar", f2_l2="2 o plano", f2_l3="3 objeções", f2_l4="4 uma tarefa com fronteira",
        f2_l5="5 atacar", f2_l6="6 entregar", f2_l7="7 · 8",
        f2_cap="Os quatro papéis em torno de um pedido. O humano o enuncia e, no fim, diz que está pronto; nada no meio espera permissão. O revisor objeta antes de qualquer trabalho, os executores nunca alargam uma tarefa, o time de qualidade nunca corrige o que encontra, e a entrega sai pelo ferramental do próprio projeto.",
        f2_aria="Diagrama do ciclo: um humano enuncia o pedido; o arquiteto, ao centro, envia o plano ao revisor e recebe objeções, despacha um leitor e um construtor com tarefas delimitadas, aciona o líder de qualidade que despacha testadores, entrega pelo ferramental do projeto em DEV, onde o humano vê funcionando e diz pronto.",
        f3_roles="os papéis", f3_a="arquiteto", f3_a_s="decide, entrega", f3_b="construtores", f3_b_s="mudam o código", f3_q="time de qualidade", f3_q_s="conduz o ataque",
        f3_tool="a ferramenta do projeto", f3_tool_s="um verbo por ação",
        f3_v1="subir · derrubar · testar", f3_v2="logs · ramificar · entregar", f3_v3="mover o pedido",
        f3_env="o ambiente local", f3_env_s="subir, derrubar, testar, reiniciar",
        f3_del="a entrega", f3_del_s="ramos, pull requests, DEV",
        f3_dem="o pedido", f3_dem_s="move-se por eventos de entrega",
        f3_human="o humano", f3_human_s="vê funcionando em DEV, diz pronto",
        f3_rec_env="registro de ambiente", f3_rec_del="registro de entrega", f3_rec_dem="registro de demandas",
        f3_cmd="comandos",
        f3_rule="um verbo que falta é uma lacuna a reportar, não motivo para improvisar",
        f3_cap="Governança pelo ferramental, não pela disciplina. Toda operação repetitiva é um verbo de uma ferramenta que o projeto possui; os registros dizem quais verbos existem e em que cada um toca. Quando a ferramenta tem um verbo para uma ação, a ação nunca acontece à mão.",
        f3_aria="Diagrama da cultura encontrando o ferramental: os papéis enviam comandos à ferramenta do projeto, que sozinha age sobre o ambiente local, sobre a entrega e sobre os estados do pedido; a entrega chega a DEV, onde o humano vê o trabalho e diz pronto. Cada alvo é nomeado por um registro.",
    ),
}


# ---------------------------------------------------------------- figure 1: what gets installed
def fig_layers(t):
    b = []
    # top band: three passes
    b.append(zone(16, 16, 688, 84, t["f1_top"]))
    for i, (k, s, x) in enumerate([("f1_detect", "f1_detect_s", 32), ("f1_ask", "f1_ask_s", 262), ("f1_write", "f1_write_s", 492)]):
        b.append(card(x, 40, 196, 48, t[k], t[s], size=13))
    b.append(link([(230, 64), (258, 64)], color=NAVY))
    b.append(link([(460, 64), (488, 64)], color=NAVY))
    # left: the culture
    b.append(zone(16, 118, 330, 296, t["f1_left"]))
    b.append(card(32, 144, 298, 54, t["f1_rules"], t["f1_rules_s"], t["f1_rules_s2"]))
    b.append(card(32, 206, 298, 54, t["f1_roles"], t["f1_roles_s"], t["f1_roles_s2"]))
    b.append(navy_card(32, 268, 298, 54, t["f1_mech"], t["f1_mech_s"], t["f1_mech_s2"]))
    b.append(label(181, 344, t["f1_agents"], anchor="middle", size=11))
    x = 40
    for n in ["reviewer", "reader", "builder", "qa lead", "tester"]:
        c, w = chip(x, 352, n, size=9.5)
        b.append(c)
        x += w + 6
    # right: the records
    b.append(zone(362, 118, 342, 296, t["f1_right"]))
    y = 144
    for k, s in [("f1_r1", "f1_r1_s"), ("f1_r2", "f1_r2_s"), ("f1_r3", "f1_r3_s"), ("f1_r4", "f1_r4_s"), ("f1_r5", "f1_r5_s")]:
        b.append(card(378, y, 310, 38, t[k], t[s], size=12.5))
        y += 42
    b.append(label(378, 370, t["f1_leg"], size=10.5))
    x = 378
    for k, fill, col in [("f1_c1", NAVY, "#fff"), ("f1_c2", "#fff", INK), ("f1_c3", ZONE, MUTED)]:
        c, w = chip(x, 376, t[k], fill=fill, line=NAVY if fill == NAVY else CARD_LINE, color=col, size=10)
        b.append(c)
        x += w + 6
    # write → records
    b.append(link([(590, 92), (590, 112)], color=NAVY))
    return figure(720, 430, "".join(b), t["f1_cap"], t["f1_aria"])


# ---------------------------------------------------------------- figure 2: the roles around the cycle
def fig_roles(t):
    b = []
    # the request (human) at the top, the architect below it, same centre line (x = 360)
    b.append(navy_card(250, 16, 220, 46, t["f2_req"], t["f2_req_s"], size=13))
    b.append(link([(360, 62), (360, 146)], color=NAVY))
    b.append(label(368, 108, t["f2_l1"], color=NAVY, weight=600))
    b.append(navy_card(248, 150, 224, 80, t["f2_arch"], t["f2_arch_s"], t["f2_arch_s2"], size=14))
    # the reviewer, left: the plan goes over the top, the objections come straight back
    b.append(card(16, 120, 168, 60, t["f2_rev"], t["f2_rev_s"], t["f2_rev_s2"], size=12.5))
    b.append(link([(276, 150), (276, 96), (100, 96), (100, 116)], color=INK))
    b.append(label(188, 90, t["f2_l2"], anchor="middle"))
    b.append(link([(184, 160), (244, 160)], color=MUTED, dash=True))
    b.append(label(214, 198, t["f2_l3"], anchor="middle", size=10))
    # the executors, bottom left
    b.append(zone(16, 270, 232, 124, t["f2_exec"]))
    b.append(card(32, 296, 200, 42, t["f2_reader"], t["f2_reader_s"], size=12.5))
    b.append(card(32, 344, 200, 42, t["f2_builder"], t["f2_builder_s"], size=12.5))
    b.append(link([(290, 230), (290, 256), (132, 256), (132, 266)], color=INK))
    b.append(label(298, 252, t["f2_l4"]))
    # the quality team, right: the lead receives the attack, dispatches its testers
    b.append(zone(520, 84, 184, 150, t["f2_qa"]))
    b.append(card(536, 110, 152, 46, t["f2_lead"], t["f2_lead_s"], size=12.5))
    for i in range(3):
        x = 536 + i * 52
        b.append(card(x, 176, 48, 40, t["f2_tester"], size=10.5, weight=500))
        b.append(link([(612, 156), (x + 24, 172)], color=MUTED, width=1.2))
    b.append(link([(440, 150), (440, 133), (532, 133)], color=INK))
    b.append(label(486, 126, t["f2_l5"], anchor="middle"))
    # delivery: through the tooling, into DEV, to the human
    b.append(link([(395, 230), (395, 296)], color=NAVY))
    b.append(label(403, 266, t["f2_l6"], color=NAVY, weight=600))
    b.append(card(300, 300, 190, 50, t["f2_tool"], t["f2_tool_s"], line=NAVY, size=12.5))
    b.append(card(526, 300, 90, 50, t["f2_dev"], t["f2_dev_s"], size=13))
    b.append(link([(490, 325), (522, 325)], color=NAVY))
    b.append(navy_card(526, 362, 178, 44, t["f2_human"], t["f2_human_s"], size=12.5))
    b.append(link([(571, 350), (571, 358)], color=NAVY))
    b.append(label(640, 358, t["f2_l7"], color=NAVY, weight=600))
    return figure(720, 420, "".join(b), t["f2_cap"], t["f2_aria"])


# ---------------------------------------------------------------- figure 3: the culture meets the tooling
def fig_tooling(t):
    b = []
    # roles
    b.append(zone(16, 96, 190, 180, t["f3_roles"]))
    b.append(card(32, 122, 158, 42, t["f3_a"], t["f3_a_s"], size=12.5))
    b.append(card(32, 172, 158, 42, t["f3_b"], t["f3_b_s"], size=12.5))
    b.append(card(32, 222, 158, 42, t["f3_q"], t["f3_q_s"], size=12.5))
    # the tool
    b.append(f'<rect x="258" y="104" width="204" height="150" rx="8" fill="{NAVY}" stroke="{NAVY_DEEP}" stroke-width="1.2"/>')
    b.append(T(360, 132, t["f3_tool"], size=14, color="#fff", anchor="middle", weight=600))
    b.append(T(360, 150, t["f3_tool_s"], size=10.5, color="#cfe0f5", anchor="middle"))
    b.append(f'<line x1="276" y1="162" x2="444" y2="162" stroke="{NAVY_SOFT}" stroke-width="1"/>')
    b.append(T(360, 184, t["f3_v1"], size=11.5, color="#fff", anchor="middle", mono=True))
    b.append(T(360, 206, t["f3_v2"], size=11.5, color="#fff", anchor="middle", mono=True))
    b.append(T(360, 228, t["f3_v3"], size=11.5, color="#fff", anchor="middle", mono=True))
    b.append(link([(206, 186), (254, 186)], color=INK))
    b.append(label(230, 178, t["f3_cmd"], anchor="middle"))
    # environment below the tool
    b.append(card(258, 292, 204, 46, t["f3_env"], t["f3_env_s"], size=12.5))
    b.append(link([(360, 254), (360, 288)], color=NAVY))
    b.append(label(372, 276, t["f3_rec_env"], size=10, color=GOLD, weight=600))
    # delivery and request on the right
    b.append(card(510, 24, 194, 50, t["f3_del"], t["f3_del_s"], size=12.5))
    b.append(link([(462, 130), (486, 130), (486, 49), (506, 49)], color=NAVY))
    b.append(label(606, 88, t["f3_rec_del"], size=10, color=GOLD, weight=600, anchor="middle"))
    b.append(card(510, 128, 194, 50, t["f3_dem"], t["f3_dem_s"], size=12.5))
    b.append(link([(462, 170), (486, 170), (486, 153), (506, 153)], color=NAVY))
    b.append(label(606, 192, t["f3_rec_dem"], size=10, color=GOLD, weight=600, anchor="middle"))
    # human
    b.append(navy_card(510, 228, 194, 52, t["f3_human"], t["f3_human_s"], size=12.5))
    b.append(link([(690, 76), (690, 224)], color=NAVY, dash=True))
    # the rule
    b.append(label(360, 362, t["f3_rule"], anchor="middle", size=11, color=MUTED))
    return figure(720, 376, "".join(b), t["f3_cap"], t["f3_aria"])


FIGS = {"layers": fig_layers, "roles": fig_roles, "tooling": fig_tooling}


def inject(path: Path, lang: str):
    text = path.read_text(encoding="utf-8")
    for name, fn in FIGS.items():
        svg = fn(L[lang])
        pattern = re.compile(rf"(<!-- fig:{name} -->\n)(<figure class=\"diagram\">.*?</figure>\n)?", re.DOTALL)
        if not pattern.search(text):
            raise SystemExit(f"{path}: marker <!-- fig:{name} --> not found")
        text = pattern.sub(lambda m: m.group(1) + svg + "\n", text, count=1)
    path.write_text(text, encoding="utf-8")
    print(f"figures written into {path.relative_to(SITE.parent)}")


if __name__ == "__main__":
    for lang, path in FILES.items():
        inject(path, lang)
