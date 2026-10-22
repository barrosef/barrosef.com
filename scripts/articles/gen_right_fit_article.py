#!/usr/bin/env python3
"""Figures for "The Right Fit" / "A Medida Certa" (EN + PT-BR), episode 5 of Spending Less on AI.

Two inline SVGs, identical in both languages except for the text:
  matrix — six requests, each with its right fit, when to step up, overpaying and underpowered
  team   — the lead and its five helpers, each with the model and effort its role carries

The markdown keeps a marker line before each figure; this script replaces the line that
follows the marker. Edit here, run, commit both.
"""
import re
from pathlib import Path

SITE = Path(__file__).resolve().parents[2] / "content"
FILES = {
    "en": SITE / "en" / "writing" / "the-right-fit.md",
    "pt-br": SITE / "pt-br" / "artigos" / "a-medida-certa.md",
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


RED = "#b3261e"


# ---------------------------------------------------------------- text, per language
# Matrix rows, in Ed's order. Each value fits one line of a card (<= 30 characters).
L = {
    "en": dict(
        cols=("Right fit", "Step up when", "Overpaying", "Underpowered"),
        rows=[
            ("Endpoint", "Haiku · high", "the rule is ambiguous", "Opus · xhigh", "Haiku · low, vague rule"),
            ("Bug", "Sonnet · high", "it can't be reproduced", "Fable · max on a typo", "Haiku, intermittent bug"),
            ("Refactoring", "Sonnet · medium", "the structure changes", "Opus on a rename", "many files, no tests"),
            ("Tests", "Sonnet · high", "the rules are critical", "Fable on routine tests", "written by the code's author"),
            ("Code review", "author's model or above · high", "security, money, data", "Fable · max on one line", "reviewer below the author"),
            ("Architecture", "Opus · xhigh", "hard to undo: Fable · max", "Fable · max, reversible", "Sonnet or Haiku"),
        ],
        m_cap="Six requests and the right fit for each, as model · effort. Above it you overpay; below it you risk the rework.",
        m_aria="Matrix of six software requests — endpoint, bug, refactoring, tests, code review, architecture — each with its right model and effort, when to step up, what overpaying looks like and what being underpowered looks like.",
        lead=("Lead", "decides, plans, checks", "Opus · Sonnet on routine days"),
        helpers=[
            ("Reader", "Sonnet · low", "reads and reports"),
            ("Builder", "Sonnet · medium", "Haiku for trivial changes"),
            ("Tester", "Sonnet · high", "attacks the work"),
            ("Reviewer", "lead's model · high", "never below the author"),
            ("QA lead", "lead's model · high", "decides what tests cover"),
        ],
        t_hand="hands each piece over, choosing the model",
        t_cap="The lead and its five helpers. Effort is fixed in each role; the model is chosen by the lead for each request.",
        t_aria="Diagram of the lead on top handing work to five helpers below: reader on Sonnet at low effort, builder on Sonnet at medium, tester on Sonnet at high, reviewer and QA lead on the lead's model at high.",
    ),
    "pt-br": dict(
        cols=("Medida certa", "Suba quando", "Pagando a mais", "Fraco demais"),
        rows=[
            ("Endpoint", "Haiku · high", "a regra é ambígua", "Opus · xhigh", "Haiku · low, regra vaga"),
            ("Bug", "Sonnet · high", "não se reproduz", "Fable · max num erro bobo", "Haiku, bug intermitente"),
            ("Refatoração", "Sonnet · medium", "a estrutura muda", "Opus para renomear", "muitos arquivos sem testes"),
            ("Testes", "Sonnet · high", "as regras são críticas", "Fable em testes de rotina", "escrito pelo autor do código"),
            ("Revisão de código", "o do autor ou acima · high", "segurança, dinheiro, dados", "Fable · max em uma linha", "revisor abaixo do autor"),
            ("Arquitetura", "Opus · xhigh", "irreversível: Fable · max", "Fable · max, reversível", "Sonnet ou Haiku"),
        ],
        m_cap="Seis pedidos e a medida certa de cada um, como modelo · esforço. Acima dela você paga a mais; abaixo, arrisca o retrabalho.",
        m_aria="Matriz de seis pedidos de software — endpoint, bug, refatoração, testes, revisão de código, arquitetura — cada um com o modelo e o esforço certos, quando subir, como é pagar a mais e como é ficar fraco demais.",
        lead=("Líder", "decide, planeja, confere", "Opus · Sonnet em dias de rotina"),
        helpers=[
            ("Leitor", "Sonnet · low", "lê e relata"),
            ("Construtor", "Sonnet · medium", "Haiku nas mudanças triviais"),
            ("Testador", "Sonnet · high", "ataca o trabalho"),
            ("Revisor", "modelo do líder · high", "nunca abaixo do autor"),
            ("Líder de QA", "modelo do líder · high", "decide o que testar"),
        ],
        t_hand="entrega cada parte, escolhendo o modelo",
        t_cap="O líder e seus cinco ajudantes. O esforço é fixo em cada papel; o modelo, o líder escolhe a cada pedido.",
        t_aria="Diagrama do líder no alto entregando trabalho a cinco ajudantes abaixo: leitor no Sonnet com esforço low, construtor no Sonnet medium, testador no Sonnet high, revisor e líder de QA no modelo do líder com esforço high.",
    ),
}


# ---------------------------------------------------------------- figure 1: the matrix, as six request cards
def matrix_svg(t, cols, cls, cw=344):
    """Six request cards in `cols` columns. The wide drawing is two columns for the page;
    the narrow one is a single column, so a phone shows it at a legible size."""
    b = []
    colors = (NAVY, MUTED, GOLD, RED)
    weights = (600, 400, 400, 400)
    ch, gx, gy, x0, y0 = 150, 16, 14, 8, 8
    rows_n = -(-len(t["rows"]) // cols)
    for i, (req, *vals) in enumerate(t["rows"]):
        x = x0 + (i % cols) * (cw + gx)
        y = y0 + (i // cols) * (ch + gy)
        b.append(f'<rect x="{x}" y="{y}" width="{cw}" height="{ch}" rx="8" fill="#fff" stroke="{CARD_LINE}" stroke-width="1.2"/>')
        b.append(f'<rect x="{x}" y="{y}" width="{cw}" height="34" rx="8" fill="{ZONE}"/>')
        b.append(f'<rect x="{x}" y="{y + 26}" width="{cw}" height="8" fill="{ZONE}"/>')
        b.append(T(x + 14, y + 23, req, size=15, weight=600))
        for k, (col, val) in enumerate(zip(t["cols"], vals)):
            ly = y + 58 + k * 26
            b.append(f'<rect x="{x + 14}" y="{ly - 11}" width="4" height="14" rx="2" fill="{colors[k]}"/>')
            b.append(T(x + 24, ly, col, size=11, color=MUTED, weight=600))
            b.append(T(x + 128, ly, val, size=13, color=colors[k] if k else INK, weight=weights[k]))
    w = x0 * 2 + cols * cw + (cols - 1) * gx
    h = y0 + rows_n * ch + (rows_n - 1) * gy + 8
    return svg(cls, w, h, "".join(b), t["m_aria"])


def fig_matrix(t):
    # No blank lines inside: Goldmark ends an HTML block at the first blank line.
    return (f'<figure class="diagram">{matrix_svg(t, 2, "wide")}{matrix_svg(t, 1, "narrow")}'
            f'<figcaption>{t["m_cap"]}</figcaption></figure>')


# ---------------------------------------------------------------- figure 2: the lead and its helpers
def svg(cls, w, h, body, aria):
    return (f'<svg class="{cls}" viewBox="0 0 {w} {h}" role="img" aria-label="{aria}" '
            f'xmlns="http://www.w3.org/2000/svg" font-family="{SANS}" color="{INK}">{DEFS}{body}</svg>')


def team_wide(t):
    b = []
    name, sub, sub2 = t["lead"]
    b.append(navy_card(240, 12, 240, 70, name, sub, sub2, size=15))
    b.append(link([(360, 82), (360, 112)], color=NAVY, head=False))
    b.append(link([(76, 112), (644, 112)], color=NAVY, head=False))
    b.append(label(368, 104, t["t_hand"], color=NAVY, size=11, weight=600))
    w, gap, x0 = 132, 10, 10
    for i, (role, me, what) in enumerate(t["helpers"]):
        cx = x0 + i * (w + gap) + w / 2
        b.append(link([(cx, 112), (cx, 130)], color=NAVY))
        b.append(card(cx - w / 2, 134, w, 78, role, me, what, size=14))
    return svg("wide", 720, 224, "".join(b), t["t_aria"])


def team_narrow(t):
    b = []
    name, sub, sub2 = t["lead"]
    b.append(navy_card(8, 8, 344, 70, name, sub, sub2, size=15))
    b.append(label(36, 100, t["t_hand"], color=NAVY, size=11, weight=600))
    top = 112
    b.append(link([(22, 78), (22, top + 5 * 70 - 38)], color=NAVY, head=False))
    for i, (role, me, what) in enumerate(t["helpers"]):
        y = top + i * 70
        b.append(link([(22, y + 32), (34, y + 32)], color=NAVY))
        b.append(card(38, y, 314, 62, role, me, what, size=14))
    return svg("narrow", 360, top + 5 * 70, "".join(b), t["t_aria"])


def fig_team(t):
    return (f'<figure class="diagram">{team_wide(t)}{team_narrow(t)}'
            f'<figcaption>{t["t_cap"]}</figcaption></figure>')


FIGS = {"matrix": fig_matrix, "team": fig_team}


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
        if path.exists():
            inject(path, lang)
