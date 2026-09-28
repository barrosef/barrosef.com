#!/usr/bin/env python3
"""Builds the inline SVG figures for "Spending Less on AI · episode 2" and injects
them into the EN and PT articles at their markers.

Same visual language as episode 1: <figure class="diagram">, inline SVG, light
palette, a descriptive aria-label and a figcaption. Every number below is real —
see docs/token-watch/data/ and the proxy request log.

Usage: python3 scripts/articles/gen_receipts_figures.py
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EN = ROOT / "content/en/writing/spending-less-on-ai-what-the-receipts-said.md"
PT = ROOT / "content/pt-br/artigos/economizando-com-ia-o-que-os-comprovantes-disseram.md"

INK, NAVY, MUTED, LINE, FILL = "#16233a", "#1d4e89", "#5d6b7d", "#d5dde8", "#eef2f7"
RED, GREEN = "#a4252c", "#1d7a4a"

# Stored-again ÷ reused, per day. Fifteen days before the proxy, six days after.
BEFORE = [1.8, 0.8, 3.1, 2.3, 0.7, 0.4, 1.2, 0.6, 1.5, 0.9, 2.4, 4.2, 4.4, 1.9, 7.6]
AFTER = [13.1, 15.7, 22.4, 37.5, 33.7, 22.3]
# Model · text saved % · share of spend %
BYMODEL = [("Opus", 5.4, 91.0), ("Sonnet", 32.6, 3.0), ("Haiku", 44.1, 0.3)]


def fig(svg, caption):
    return f'<figure class="diagram">\n{svg}\n<figcaption>{caption}</figcaption>\n</figure>'


def head(vb, label):
    return (f'<svg viewBox="0 0 {vb}" role="img" aria-label="{label}" '
            f'xmlns="http://www.w3.org/2000/svg" '
            f'font-family="IBM Plex Sans, system-ui, sans-serif" color="{INK}">')


def f_daily(L):
    w, h, top = 720, 300, 30
    n = len(BEFORE) + len(AFTER)
    gap, bw = 4, (720 - 80 - (len(BEFORE) + len(AFTER) - 1) * 4) / n
    peak, base = max(AFTER), 250
    s = [head(f"{w} {h}", L["a_daily"])]
    for i, v in enumerate(BEFORE + AFTER):
        x = 60 + i * (bw + gap)
        bh = max(2, (base - top) * v / peak)
        c = RED if i >= len(BEFORE) else "#c9d3df"
        s.append(f'<rect x="{x:.1f}" y="{base - bh:.1f}" width="{bw:.1f}" height="{bh:.1f}" fill="{c}" rx="2"/>')
    split = 60 + len(BEFORE) * (bw + gap) - gap / 2
    s.append(f'<line x1="60" y1="{base}" x2="{w - 20}" y2="{base}" stroke="{LINE}" stroke-width="1.5"/>')
    s.append(f'<line x1="{split:.1f}" y1="{top - 8}" x2="{split:.1f}" y2="{base}" stroke="{MUTED}" '
             f'stroke-width="1" stroke-dasharray="4 3"/>')
    s.append(f'<text x="{split + 6:.1f}" y="{top - 12}" font-size="11" fill="{MUTED}">{L["d_split"]}</text>')
    for v, y in ((40, top + 4), (20, top + (base - top) * (1 - 20 / peak)), (0, base)):
        s.append(f'<text x="52" y="{y + 4:.0f}" text-anchor="end" font-size="10.5" fill="{MUTED}">{v}%</text>')
    s.append(f'<text x="60" y="{base + 20}" font-size="10.5" fill="{MUTED}">{L["d_left"]}</text>')
    s.append(f'<text x="{w - 20}" y="{base + 20}" text-anchor="end" font-size="10.5" fill="{MUTED}">{L["d_right"]}</text>')
    s.append(f'<text x="60" y="{base + 40}" font-size="11" fill="{INK}">{L["d_note"]}</text>')
    s.append("</svg>")
    return fig("".join(s), L["c_daily"])


def f_model(L):
    w, h = 720, 250
    s = [head(f"{w} {h}", L["a_model"])]
    for i, (name, saved, share) in enumerate(BYMODEL):
        y = 40 + i * 62
        s.append(f'<text x="16" y="{y + 16}" font-size="14" font-weight="600" fill="{INK}">{name}</text>')
        s.append(f'<text x="16" y="{y + 33}" font-size="10.5" fill="{MUTED}">{L["m_share"]} {share:g}%</text>')
        s.append(f'<rect x="130" y="{y}" width="420" height="28" rx="6" fill="{FILL}"/>')
        s.append(f'<rect x="130" y="{y}" width="{420 * saved / 50:.0f}" height="28" rx="6" fill="{GREEN}"/>')
        s.append(f'<text x="566" y="{y + 20}" font-size="15" font-weight="700" fill="{GREEN}">'
                 f'−{L["dec"](saved)}%</text>')
        sw = max(3, 120 * share / 100)
        s.append(f'<rect x="640" y="{y}" width="120" height="28" rx="6" fill="{FILL}" opacity=".6"/>'
                 if False else "")
        s.append(f'<rect x="646" y="{y + 6}" width="{sw:.0f}" height="16" rx="3" fill="{RED}"/>')
    s.append(f'<text x="130" y="28" font-size="10.5" fill="{MUTED}">{L["m_axis"]}</text>')
    s.append(f'<text x="646" y="28" font-size="10.5" fill="{MUTED}">{L["m_spend"]}</text>')
    s.append(f'<text x="16" y="{h - 12}" font-size="11" fill="{INK}">{L["m_note"]}</text>')
    s.append("</svg>")
    return fig("".join(s), L["c_model"])


def f_price(L):
    w, h = 720, 210
    s = [head(f"{w} {h}", L["a_price"])]
    for i, (lab, mult, col) in enumerate(((L["p_reuse"], 1, NAVY), (L["p_store"], 12.5, RED))):
        y = 44 + i * 74
        s.append(f'<text x="16" y="{y + 18}" font-size="14" font-weight="600" fill="{INK}">{lab}</text>')
        s.append(f'<rect x="250" y="{y}" width="{400 * mult / 12.5:.0f}" height="30" rx="6" fill="{col}"/>')
        s.append(f'<text x="{250 + 400 * mult / 12.5 + 14:.0f}" y="{y + 21}" font-size="17" '
                 f'font-weight="700" fill="{col}">{mult:g}×</text>')
    s.append(f'<text x="16" y="26" font-size="11" fill="{MUTED}">{L["p_axis"]}</text>')
    s.append(f'<text x="16" y="{h - 14}" font-size="11" fill="{INK}">{L["p_note"]}</text>')
    s.append("</svg>")
    return fig("".join(s), L["c_price"])


def f_balance(L):
    w, h = 720, 210
    s = [head(f"{w} {h}", L["a_bal"])]
    rows = ((L["b_saved"], 439, GREEN, "+"), (L["b_paid"], 1200, RED, "−"), (L["b_net"], 750, RED, "−"))
    for i, (lab, v, col, sign) in enumerate(rows):
        y = 34 + i * 50
        s.append(f'<text x="16" y="{y + 20}" font-size="13.5" fill="{INK}">{lab}</text>')
        op = ' opacity="0.85"' if i == 2 else ""
        s.append(f'<rect x="300" y="{y + 2}" width="{300 * v / 1200:.0f}" height="26" rx="5" '
                 f'fill="{col}"{op}/>')
        n = f"{v:,}".replace(",", L["thou"])
        s.append(f'<text x="{300 + 300 * v / 1200 + 12:.0f}" y="{y + 21}" font-size="16" '
                 f'font-weight="700" fill="{col}">{sign}${n}</text>')
        if i == 1:
            s.append(f'<line x1="300" y1="{y + 40}" x2="{w - 20}" y2="{y + 40}" stroke="{LINE}"/>')
    s.append(f'<text x="16" y="{h - 12}" font-size="11" fill="{INK}">{L["b_note"]}</text>')
    s.append("</svg>")
    return fig("".join(s), L["c_bal"])


EN_L = dict(
    dec=lambda v: f"{v:.1f}", thou=",",
    a_daily="Bar chart of twenty-one working days. The fifteen before the proxy sit between 0.4 and 7.6 percent; the six after it range from 13.1 to 37.5 percent.",
    d_split="proxy switched on", d_left="fifteen days before", d_right="six days after",
    d_note="Stored again, as a share of what was reused — one bar per day.",
    c_daily="The ratio of context stored again to context reused, per day. The median over the fifteen days before was 1.9%; the six days after ran between 13% and 37%.",
    a_model="Three horizontal bars: Opus saves 5.4 percent and is 91 percent of the spend; Sonnet saves 32.6 percent and is 3 percent; Haiku saves 44.1 percent and is 0.3 percent.",
    m_share="share of spend:", m_axis="text saved", m_spend="share of spend",
    m_note="It performs six to eight times better on the models that carry almost none of the bill.",
    c_model="Text saved per model against each model's share of my spend. The green bar is the saving; the red bar is where the money actually is.",
    a_price="Two bars comparing prices: reusing stored context costs one unit, storing it again costs twelve and a half.",
    p_reuse="Reuse what is stored", p_store="Store it again", p_axis="price for the same words",
    p_note="Cache read is 0.10× the base rate; cache write is 1.25×.",
    c_price="The same words, two prices. Anything that rewrites the start of a message moves tokens from the cheap column to the expensive one.",
    a_bal="Three bars: 439 dollars saved, about 1,200 dollars paid on top, leaving about 750 dollars negative.",
    b_saved="Saved on text sent", b_paid="Paid on top in re-writes", b_net="Net, six days",
    b_note="$439 is measured. The other two are estimates — three scopes put the excess between $1,110 and $1,271.",
    c_bal="The six days, as an account. The saving is real and the line beneath it is larger.",
)

PT_L = dict(
    dec=lambda v: f"{v:.1f}".replace(".", ","), thou=".",
    a_daily="Gráfico de barras de vinte e um dias úteis. Os quinze antes do proxy ficam entre 0,4 e 7,6 por cento; os seis depois vão de 13,1 a 37,5 por cento.",
    d_split="proxy ligado", d_left="quinze dias antes", d_right="seis dias depois",
    d_note="Guardado de novo, como fração do que foi reaproveitado — uma barra por dia.",
    c_daily="A razão entre contexto guardado de novo e contexto reaproveitado, por dia. A mediana dos quinze dias anteriores era 1,9%; os seis dias seguintes correram entre 13% e 37%.",
    a_model="Três barras horizontais: Opus economiza 5,4 por cento e é 91 por cento do gasto; Sonnet economiza 32,6 por cento e é 3 por cento; Haiku economiza 44,1 por cento e é 0,3 por cento.",
    m_share="fatia do gasto:", m_axis="texto economizado", m_spend="fatia do gasto",
    m_note="Ela rende de seis a oito vezes mais nos modelos que quase não pesam na conta.",
    c_model="Texto economizado por modelo contra a fatia de gasto de cada um. A barra verde é a economia; a vermelha é onde o dinheiro está.",
    a_price="Duas barras comparando preços: reaproveitar o contexto guardado custa uma unidade, guardar de novo custa doze e meia.",
    p_reuse="Reaproveitar o guardado", p_store="Guardar de novo", p_axis="preço pelas mesmas palavras",
    p_note="Leitura de cache custa 0,10× a tarifa base; escrita custa 1,25×.",
    c_price="As mesmas palavras, dois preços. Tudo que reescreve o começo da mensagem move tokens da coluna barata para a cara.",
    a_bal="Três barras: 439 dólares economizados, cerca de 1.200 dólares pagos a mais, deixando cerca de 750 dólares negativos.",
    b_saved="Economizou em texto enviado", b_paid="Pagou a mais em regravação", b_net="Saldo, seis dias",
    b_note="US$ 439 é medido. Os outros dois são estimativa — três recortes põem o excesso entre US$ 1.110 e US$ 1.271.",
    c_bal="Os seis dias, como extrato. A economia é real e a linha abaixo dela é maior.",
)

FIGS = {"DAILY": f_daily, "MODEL": f_model, "PRICE": f_price, "BALANCE": f_balance}


def inject(path, L):
    t = path.read_text(encoding="utf-8")
    for name, fn in FIGS.items():
        marker = f"<!-- FIG:{name} -->"
        if marker not in t:
            print(f"  ! {path.name}: marcador {marker} não encontrado")
            continue
        block = re.compile(re.escape(marker) + r"(?:\n<figure class=\"diagram\">.*?</figure>)?", re.S)
        t = block.sub(marker + "\n" + fn(L), t, count=1)
    path.write_text(t, encoding="utf-8")
    print(f"  {path.name}: {sum(1 for n in FIGS if f'<!-- FIG:{n} -->' in t)} figuras")


if __name__ == "__main__":
    inject(EN, EN_L)
    inject(PT, PT_L)
