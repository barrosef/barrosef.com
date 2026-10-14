#!/usr/bin/env python3
"""Generates episode 4 of "Spending Less on AI" in EN and PT-BR with identical SVG figures.

The five-week numbers come from docs/token-watch (strict per-card attribution,
2026-08-15..09-21). The before/after per round by role comes from cost-lab
(/api/calibration?project=vega, list price), read on 2026-10-14 after the
ingest that took the data to 2026-10-14.
Run from anywhere: python3 scripts/articles/gen_model_effort_article.py
"""
from pathlib import Path

SITE = Path(__file__).resolve().parents[2]
CONTENT = SITE / "content"
COVER = SITE / "static" / "img" / "covers" / "model-effort.svg"

# ---------------------------------------------------------------- drawing primitives (house style)
NAVY = "#1d4e89"
NAVY_DEEP = "#173d6e"
INK = "#16233a"
MUTED = "#5d6b7d"
ZONE = "#eef2f7"
ZONE_LINE = "#d5dde8"
CARD_LINE = "#b9c5d4"
FORBID = "#b3261e"
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
    m = {INK: "m-ink", NAVY: "m-navy", FORBID: "m-forbid", MUTED: "m-muted", GOLD: "m-gold"}.get(color, "m-ink")
    mk = f' marker-end="url(#{m})"' if head else ""
    pth = "M " + " L ".join(f"{x},{y}" for x, y in pts)
    return f'<path d="{pth}" fill="none" stroke="{color}" stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round"{d}{mk}/>'


def marker(mid, color):
    return (f'<marker id="{mid}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
            f'<path d="M1,1 L9,5 L1,9 z" fill="{color}"/></marker>')


DEFS = "<defs>" + "".join(marker(m, c) for m, c in [("m-ink", INK), ("m-navy", NAVY), ("m-forbid", FORBID), ("m-muted", MUTED), ("m-gold", GOLD)]) + "</defs>"


def figure(w, h, body, caption, aria):
    # No blank lines inside: Goldmark ends an HTML block at the first blank line.
    return (f'<figure class="diagram"><svg viewBox="0 0 {w} {h}" role="img" aria-label="{aria}" '
            f'xmlns="http://www.w3.org/2000/svg" font-family="{SANS}" color="{INK}">'
            f'{DEFS}{body}</svg><figcaption>{caption}</figcaption></figure>')


# ---------------------------------------------------------------- data (docs/token-watch, strict attribution)
# 36 demands with a typed prompt naming the card, turns each, sorted ascending.
TURNS = [1, 2, 8, 38, 42, 47, 56, 62, 64, 97, 97, 98, 99, 137, 154, 157, 209, 242, 260, 283, 289, 292, 303, 384, 390, 391, 496, 519, 571, 911, 946, 972, 1357, 1567, 1997, 2450]
CASES = {"A": 42, "B": 1997, "C": 911, "D": 2450}
# US$ per round, list price, same client platform. Before: the session alone on
# Opus 5, high effort (31/08..28/09). After: lead + helpers (29/09 onward).
BEFORE_ROUND = 0.52
AFTER_ROUNDS = [("lead", 0.24), ("qa_lead", 0.15), ("tester_inh", 0.13), ("reviewer", 0.06),
                ("tester", 0.047), ("builder", 0.04), ("reader", 0.035), ("builder_haiku", 0.01)]


# ---------------------------------------------------------------- figure 1: the spread
def fig_spread(L):
    b = ""
    x0, y0, w, h = 56, 36, 640, 260
    n = len(TURNS)
    bw = w / n
    mx = 2500
    b += link([(x0, y0 + h), (x0 + w, y0 + h)], color=CARD_LINE, head=False, width=1)
    for gy, lab in [(0, "0"), (500, "500"), (1000, "1 000"), (1500, "1 500"), (2000, "2 000"), (2500, "2 500")]:
        yy = y0 + h - h * gy / mx
        b += link([(x0, yy), (x0 + w, yy)], color=ZONE_LINE, head=False, width=1)
        b += T(x0 - 8, yy + 4, lab, size=10.5, color=MUTED, anchor="end", mono=True)
    tagged = {v: k for k, v in CASES.items()}
    for i, t in enumerate(TURNS):
        bh = h * t / mx
        x = x0 + i * bw + 2
        key = tagged.get(t)
        fill = NAVY if key else "#c9d6e6"
        b += f'<rect x="{x:.1f}" y="{y0 + h - bh:.1f}" width="{bw - 4:.1f}" height="{bh:.1f}" fill="{fill}"/>'
        if key:
            b += T(x + (bw - 4) / 2, y0 + h - bh - 8, key, size=12.5, color=NAVY, anchor="middle", weight=700)
    # median marker
    med = 242
    ym = y0 + h - h * med / mx
    b += link([(x0, ym), (x0 + w, ym)], color=GOLD, dash=True, head=False, width=1.3)
    b += T(x0 + w - 4, ym - 6, L["median"], size=11, color=GOLD, anchor="end", weight=600)
    b += T(x0, y0 + h + 24, L["spread_x"], size=11.5, color=MUTED)
    b += T(x0 + w, y0 + h + 24, L["spread_right"], size=11.5, color=MUTED, anchor="end")
    b += T(x0, y0 - 12, L["spread_y"], size=11.5, color=MUTED)
    return figure(720, 336, b, L["cap_spread"], L["aria_spread"])


# ---------------------------------------------------------------- figure 2: one turn, where the money goes
def fig_turn(L):
    b = ""
    # the turn as a courier: context stack -> model -> output; cost bar underneath
    b += zone(16, 16, 688, 150, L["turn_title"])
    b += card(32, 56, 190, 90, L["ctx"], L["ctx_sub"], fill="#fff")
    b += T(127, 130, "509 000", size=15, color=NAVY, anchor="middle", weight=700, mono=True)
    b += link([(224, 100), (262, 100)], color=NAVY)
    b += card(264, 56, 190, 90, L["model"], L["model_sub"], fill=NAVY, line=NAVY_DEEP, tcolor="#fff", scolor="#cfe0f5")
    b += link([(456, 100), (494, 100)], color=NAVY)
    b += card(496, 56, 190, 90, L["out"], L["out_sub"])
    b += T(591, 130, "1 000", size=15, color=NAVY, anchor="middle", weight=700, mono=True)
    # cost bar
    y = 196
    b += T(16, y - 8, L["cost_title"], size=12.5, color=MUTED, weight=600)
    x = 16
    W = 688
    parts = [(0.73, NAVY, L["c_read"]), (0.20, "#5b8fd6", L["c_write"]), (0.07, "#c9d6e6", L["c_out"])]
    for frac, col, lab in parts:
        pw = W * frac
        b += f'<rect x="{x:.1f}" y="{y}" width="{pw:.1f}" height="34" fill="{col}"/>'
        if frac < 0.1:
            b += T(x + pw, y - 6, lab, size=11.5, color=MUTED, anchor="end", weight=600)
        else:
            b += T(x + pw / 2, y + 22, lab, size=11.5, color="#fff", anchor="middle", weight=600)
        x += pw
    b += T(16, y + 58, L["cost_note"], size=11.5, color=MUTED)
    # the lever
    b += zone(16, 276, 688, 96, None, dash=True)
    b += T(32, 300, L["lever_title"], size=12.5, color=NAVY, weight=600)
    b += T(32, 322, L["lever_1"], size=11.5, color=INK)
    b += T(32, 340, L["lever_2"], size=11.5, color=INK)
    b += T(32, 358, L["lever_3"], size=11.5, color=MUTED, italic=True)
    return figure(720, 388, b, L["cap_turn"], L["aria_turn"])


# ---------------------------------------------------------------- figure 3: the map
def fig_map(L):
    b = ""
    x0, y0, w, h = 150, 30, 520, 300
    b += f'<rect x="{x0}" y="{y0}" width="{w}" height="{h}" fill="#fff" stroke="{CARD_LINE}" stroke-width="1"/>'
    b += link([(x0 + w / 2, y0), (x0 + w / 2, y0 + h)], color=ZONE_LINE, head=False, width=1)
    b += link([(x0, y0 + h / 2), (x0 + w, y0 + h / 2)], color=ZONE_LINE, head=False, width=1)
    # axes
    b += T(x0 + w / 2, y0 + h + 28, L["ax_x"], size=12, color=MUTED, anchor="middle", weight=600)
    b += T(x0 + 6, y0 + h + 14, L["ax_x_lo"], size=10.5, color=MUTED)
    b += T(x0 + w - 6, y0 + h + 14, L["ax_x_hi"], size=10.5, color=MUTED, anchor="end")
    b += f'<text transform="translate({x0 - 28},{y0 + h / 2}) rotate(-90)" text-anchor="middle" font-size="12" font-weight="600" fill="{MUTED}">{L["ax_y"]}</text>'
    b += T(x0 - 8, y0 + h - 4, L["ax_y_lo"], size=10.5, color=MUTED, anchor="end")
    b += T(x0 - 8, y0 + 12, L["ax_y_hi"], size=10.5, color=MUTED, anchor="end")
    # quadrant labels
    q = [(x0 + 12, y0 + 22, L["q_tl"]), (x0 + w / 2 + 12, y0 + 22, L["q_tr"]),
         (x0 + 12, y0 + h / 2 + 22, L["q_bl"]), (x0 + w / 2 + 12, y0 + h / 2 + 22, L["q_br"])]
    for x, y, lab in q:
        b += T(x, y, lab, size=11, color=MUTED, weight=600)
    # cases as navy dots with model×effort chips
    pts = {"A": (x0 + 90, y0 + h - 60, L["pA"]), "B": (x0 + w - 110, y0 + h - 80, L["pB"]),
           "C": (x0 + 110, y0 + 70, L["pC"]), "D": (x0 + w - 120, y0 + 60, L["pD"])}
    for k, (x, y, lab) in pts.items():
        b += f'<circle cx="{x}" cy="{y}" r="15" fill="{NAVY}" stroke="{NAVY_DEEP}" stroke-width="1.5"/>'
        b += T(x, y + 5, k, size=13, color="#fff", anchor="middle", weight=700)
        c, cw = chip(x - 6, y + 22, lab, fill=ZONE, line=ZONE_LINE)
        if x + cw > x0 + w:
            c, cw = chip(x - cw + 6, y + 22, lab, fill=ZONE, line=ZONE_LINE)
        b += c
    # D is not a point: dashed arc across the map
    b += f'<path d="M {x0 + 100},{y0 + h - 70} C {x0 + 200},{y0 + h - 40} {x0 + 300},{y0 + 40} {x0 + w - 130},{y0 + 62}" fill="none" stroke="{GOLD}" stroke-width="1.6" stroke-dasharray="6 5" marker-end="url(#m-gold)"/>'
    b += T(x0 + w / 2 - 20, y0 + h / 2 - 58, L["d_note"], size=11, color=GOLD, weight=600, anchor="middle")
    return figure(720, 380, b, L["cap_map"], L["aria_map"])


# ---------------------------------------------------------------- figure 4: case B, as it happened vs led
def fig_caseb(L):
    b = ""
    # top lane: as it happened — one long line of turns with five redirect flags
    b += zone(16, 16, 688, 120, L["b_top"])
    y = 80
    b += link([(40, y), (680, y)], color=NAVY, head=True, width=3)
    for x in [180, 260, 380, 470, 560]:
        b += f'<path d="M {x},{y - 4} L {x},{y - 28} L {x + 16},{y - 22} L {x},{y - 16}" fill="{FORBID}" stroke="none"/>'
    b += T(40, y + 26, L["b_top_note"], size=11.5, color=MUTED)
    b += T(680, y + 26, "1 997", size=13, color=NAVY, anchor="end", weight=700, mono=True)
    # bottom lane: led
    b += zone(16, 156, 688, 232, L["b_bot"])
    b += card(24, 200, 170, 60, L["lead"], L["lead_sub"], fill=NAVY, line=NAVY_DEEP, tcolor="#fff", scolor="#cfe0f5")
    # fan out to 14 workers
    wx0, wy = 222, 196
    for i in range(14):
        col = i % 7
        row = i // 7
        x = wx0 + col * 60
        yy = wy + row * 36
        b += f'<rect x="{x}" y="{yy}" width="48" height="26" rx="5" fill="#fff" stroke="{CARD_LINE}" stroke-width="1.1"/>'
        b += T(x + 24, yy + 17, f"w{i + 1}", size=10.5, color=INK, anchor="middle", mono=True)
    b += link([(196, 230), (216, 230)], color=NAVY)
    b += T(wx0, wy + 90, L["workers"], size=11.5, color=MUTED)
    b += T(wx0, wy + 108, L["workers_sub"], size=11.5, color=MUTED)
    # back to leader for the 2
    b += card(24, 300, 170, 60, L["lead2"], L["lead2_sub"], fill="#fff")
    b += link([(216, 300), (196, 318)], color=NAVY)
    b += T(222, 318, L["back"], size=11.5, color=NAVY, weight=600)
    b += T(222, 336, L["back_sub"], size=11.5, color=MUTED)
    return figure(720, 404, b, L["cap_caseb"], L["aria_caseb"])


# ---------------------------------------------------------------- figure 5: case D changes nature
def fig_cased(L):
    b = ""
    b += T(16, 28, L["d_title"], size=12.5, color=MUTED, weight=600)
    y0, H = 44, 54
    segs = [(0.16, "#c9d6e6", INK, L["d1"]), (0.30, NAVY, "#fff", L["d2"]), (0.24, "#5b8fd6", "#fff", L["d3"]),
            (0.18, "#c9d6e6", INK, L["d4"]), (0.12, NAVY, "#fff", L["d5"])]
    x = 16
    W = 688
    for frac, col, tc, lab in segs:
        pw = W * frac
        b += f'<rect x="{x:.1f}" y="{y0}" width="{pw:.1f}" height="{H}" fill="{col}" stroke="#fff" stroke-width="2"/>'
        b += T(x + pw / 2, y0 + H / 2 + 4, lab, size=11, color=tc, anchor="middle", weight=600)
        x += pw
    b += T(16, y0 + H + 20, L["d_start"], size=10.5, color=MUTED, mono=True)
    b += T(16 + W, y0 + H + 20, L["d_end"], size=10.5, color=MUTED, anchor="end", mono=True)
    # legend of natures
    ly = 146
    for i, (col, lab) in enumerate([("#c9d6e6", L["n_mech"]), ("#5b8fd6", L["n_vol"]), (NAVY, L["n_judge"])]):
        y = ly + i * 24
        b += f'<rect x="16" y="{y}" width="18" height="18" rx="3" fill="{col}"/>'
        b += T(42, y + 14, lab, size=11.5, color=INK)
    # the point
    b += zone(16, 232, 688, 70, None, dash=True)
    b += T(32, 258, L["d_point1"], size=12, color=INK, weight=600)
    b += T(32, 280, L["d_point2"], size=11.5, color=MUTED)
    return figure(720, 318, b, L["cap_cased"], L["aria_cased"])


# ---------------------------------------------------------------- figure 6: the lead and the helpers, as configured
def fig_leader(L):
    b = ""
    b += card(260, 14, 200, 62, L["lead_box"], L["lead_box_sub"], fill=NAVY, line=NAVY_DEEP, tcolor="#fff", scolor="#cfe0f5")
    b += T(360, 92, L["lead_line1"], size=11, color=MUTED, anchor="middle")
    # a bus under the lead, one drop into each helper
    xs = [16 + i * 140 for i in range(5)]
    b += link([(360, 76), (360, 104)], color=NAVY, head=False, width=1.3)
    b += link([(xs[0] + 64, 104), (xs[-1] + 64, 104)], color=NAVY, head=False, width=1.3)
    for i, x in enumerate(xs):
        title, fm = L["w"][i]
        b += link([(x + 64, 104), (x + 64, 118)], color=NAVY, head=True, width=1.3)
        b += f'<rect x="{x}" y="122" width="128" height="124" rx="6" fill="#fff" stroke="{CARD_LINE}" stroke-width="1.2"/>'
        b += T(x + 64, 144, title, size=12.5, color=INK, anchor="middle", weight=600)
        for k, ln in enumerate(fm):
            mono = k < 3
            b += T(x + 10, 168 + k * 17, ln, size=10.5 if mono else 10, color=NAVY if k < 2 else MUTED, mono=mono, italic=not mono)
    # runtime override
    b += zone(16, 262, 688, 92, None, dash=True)
    b += T(32, 286, L["rt_title"], size=12.5, color=NAVY, weight=600)
    b += T(32, 308, L["rt_1"], size=11.5, color=INK, italic=True)
    b += T(32, 328, L["rt_2"], size=11.5, color=INK)
    b += T(32, 346, L["rt_3"], size=11.5, color=MUTED, italic=True)
    return figure(720, 370, b, L["cap_leader"], L["aria_leader"])


# ---------------------------------------------------------------- figure 7: before and after, US$ per round by role
def fig_beforeafter(L):
    b = ""
    scale = 1000  # px per dollar
    x0, lw = 16, 236  # label column
    b += T(x0, 28, L["ba_title"], size=12.5, color=MUTED, weight=600)
    b += T(704, 28, L["ba_unit"], size=11, color=MUTED, anchor="end")
    y = 44
    # before: one bar
    b += T(x0, y + 15, L["ba_before"], size=11.5, color=INK, weight=600)
    w = BEFORE_ROUND * scale * 0.8
    b += f'<rect x="{x0 + lw}" y="{y}" width="{w:.1f}" height="22" fill="{NAVY}"/>'
    b += T(x0 + lw + w + 8, y + 15, f"{BEFORE_ROUND:.2f}", size=12, color=NAVY, weight=700, mono=True)
    y += 40
    b += f'<path d="M{x0},{y} L704,{y}" stroke="{CARD_LINE}" stroke-width="1" stroke-dasharray="3 3"/>'
    y += 10
    b += T(x0, y + 15, L["ba_after"], size=11.5, color=INK, weight=600)
    for key, val in AFTER_ROUNDS:
        lab = L["ba_roles"][key]
        inherited = key == "tester_inh"
        col = "#c44536" if inherited else ("#5b8fd6" if key in ("lead", "qa_lead", "reviewer") else "#9fc0e8")
        b += T(x0 + lw - 10, y + 15, lab, size=11, color="#c44536" if inherited else INK, anchor="end", italic=inherited)
        w = val * scale * 0.8
        b += f'<rect x="{x0 + lw}" y="{y}" width="{w:.1f}" height="20" fill="{col}"/>'
        b += T(x0 + lw + w + 8, y + 14, f"{val:.3f}".rstrip("0"), size=11.5, color=INK, weight=600, mono=True)
        y += 26
    y += 8
    b += zone(x0, y, 688, 48, None, dash=True)
    b += T(x0 + 16, y + 20, L["ba_share1"], size=11.5, color=NAVY, weight=600)
    b += T(x0 + 16, y + 38, L["ba_share2"], size=11, color=MUTED, italic=True)
    return figure(720, y + 64, b, L["cap_ba"], L["aria_ba"])


# ---------------------------------------------------------------- cover 800×600 (dark ground, like the others)
def cover():
    s = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 600" role="img" aria-hidden="true"><rect width="800" height="600" fill="#0b1622"/>']
    # bars: the spread, in muted blue; four navy-bright ones
    base = 470
    vals = [4, 6, 10, 14, 18, 22, 26, 30, 34, 40, 46, 52, 60, 70, 82, 96, 112, 130, 150, 176, 210, 250, 300, 360]
    x = 60
    for i, v in enumerate(vals):
        h = v
        bright = i in (4, 15, 20, 23)
        col = "#7fb0ea" if bright else "#1d4e89"
        s.append(f'<rect x="{x}" y="{base - h}" width="20" height="{h}" rx="3" fill="{col}"/>')
        x += 28
    # one flat line across the top: "one model"
    s.append('<path d="M60,120 L740,120" stroke="#dce6f2" stroke-width="6" stroke-linecap="round" stroke-dasharray="1 0"/>')
    s.append('<circle cx="740" cy="120" r="14" fill="#dce6f2"/>')
    s.append('</svg>')
    COVER.write_text("".join(s), encoding="utf-8")


# ---------------------------------------------------------------- labels
EN = dict(
    median="median · 242", spread_x="36 tasks, five weeks — one bar per task", spread_right="sorted by size",
    spread_y="rounds of work (each one re-sends the whole conversation)",
    cap_spread="Thirty-six tasks, one bar each. The smallest cost nine dollars, the largest 945, and between them sits every kind of work a delivery team does in five weeks. The four the article follows are in navy. All thirty-six ran on the same model.",
    aria_spread="Bar chart of 36 tasks sorted by number of rounds, from 1 to 2,450, with a gold median line at 242 and four navy bars labelled A, B, C and D.",
    turn_title="one round of work", ctx="the conversation", ctx_sub="tokens re-sent, average", model="the model", model_sub="reads all of it, again",
    out="the answer", out_sub="tokens written, average",
    cost_title="where the 37 cents go", c_read="re-reading what it already saw · 73%", c_write="caching · 20%", c_out="the answer · 7%",
    cost_note="Thinking lives inside that 7%. What an agent costs is not what it writes — it is what it re-reads.",
    lever_title="which leaves exactly two levers",
    lever_1="The model sets the price of every line: at the time, Opus $5, Sonnet $2, Haiku $1 per million tokens read.",
    lever_2="The effort level sets how many rounds there are: lower effort, fewer and larger steps, fewer rounds.",
    lever_3="Average round across the five weeks: 509,000 tokens in, 1,000 out, 37 cents.",
    cap_turn="One round of work, taken apart. The agent re-sends half a million tokens in order to write a thousand — so three quarters of the bill is re-reading, and the model you choose sets the price of every re-read.",
    aria_turn="A conversation of 509,000 tokens enters a navy model box and a 1,000-token answer leaves; below, a cost bar split 73% re-reading, 20% caching, 7% answer; a dashed panel lists the two levers.",
    ax_x="how much work", ax_x_lo="one place", ax_x_hi="many places, one pattern", ax_y="how much doubt", ax_y_lo="the request is right", ax_y_hi="the request may be wrong",
    q_tl="find the truth", q_tr="find it, then repeat it", q_bl="just do it", q_br="do it many times",
    pA="Sonnet · low", pB="Opus, then 14 × Haiku", pC="Opus · max", pD="moves while you work", d_note="the fourth crosses the map",
    cap_map="Two questions, four answers. Doubt buys the model; volume buys the effort level and, past a point, more hands. Three of the four tasks sit still in one square. The fourth does not — and that is the whole argument for a lead.",
    aria_map="A two-by-two map with doubt vertical and amount of work horizontal; task A bottom-left Sonnet low, B bottom-right Opus then fourteen Haiku, C top-left Opus max, D top-right with a dashed gold arc crossing the map.",
    b_top="what happened — one model, one conversation", b_top_note="five times I had to pull it back on course; two tasks tangled in one thread",
    b_bot="what the work actually was", lead="Opus", lead_sub="writes the rule, once", workers="14 × Haiku · in parallel, one item each",
    workers_sub="a clean context every time, so nothing can get tangled", lead2="Opus", lead2_sub="reviews the two real ones",
    back="2 come back", back_sub="the other 12 were the same mistake",
    cap_caseb="The repeated task, drawn twice. Above, the $660 as it was actually spent, with a flag wherever I had to pull the conversation back on course. Below, the shape the work had all along: write the rule once, apply it fourteen times, judge twice.",
    aria_caseb="Top lane: a long navy arrow of 1,997 rounds with five red flags marking human corrections. Bottom lane: an Opus box writes a rule, fans out to fourteen Haiku boxes working in parallel, and two results return for review.",
    d_title="the fourth task · ten days · $945",
    d1="read it", d2="3 of 4 already existed", d3="investigate", d4="build the screen", d5="renegotiate",
    d_start="day 1", d_end="day 10", n_mech="mechanical — Haiku territory", n_vol="volume — one pattern, many places", n_judge="judgment — the request was wrong",
    d_point1="Pick one model on day one and you are wrong by day four.",
    d_point2="The choice has to be made per task, while the work runs — which means somebody has to be making it.",
    cap_cased="The largest task, coloured by the kind of work each stretch demanded. It opens in judgment, turns to volume, goes mechanical, and ends in judgment again. No single choice made at the start survives the middle.",
    aria_cased="A horizontal timeline of the fourth task in five segments coloured by nature of work, with a legend and a closing note below.",
    lead_box="the lead", lead_box_sub="Opus · the session itself",
    lead_line1="reads the request, splits the work, holds the scope, judges what comes back",
    w=[("reader", ["model: sonnet", "effort: low", "maxTurns: 25", "reads, never writes"]),
       ("builder", ["model: sonnet", "effort: medium", "maxTurns: 80", "one settled change"]),
       ("tester", ["model: sonnet", "effort: high", "maxTurns: 120", "level set at hand-off"]),
       ("reviewer", ["model: inherit", "effort: high", "maxTurns: 40", "the lead's own level"]),
       ("QA lead", ["model: inherit", "effort: high", "maxTurns: 160", "dispatches the testers"])],
    rt_title="and the lead can override the model on any single hand-off",
    rt_1="“This batch is trivial — run it on Sonnet.”",
    rt_2="The file sets the default. The hand-off sets the exception. The lead holds both.",
    rt_3="These are the real settings of the five helper files, not a metaphor.",
    cap_leader="What replaced one model for everything, as it was actually configured: a lead that decides and never executes, three helpers on the cheaper model that read, build and test, and two adversaries — the reviewer and the QA lead — that deliberately run at the lead's own level.",
    aria_leader="A navy lead box connects to five helper boxes labelled reader, builder, tester, reviewer and QA lead, each showing configuration lines for model, effort and turn limit.",
    ba_title="what one round cost, before and after", ba_unit="US$ per round · list price",
    ba_before="before · the session alone, on Opus",
    ba_after="after · by role",
    ba_roles={"lead": "the lead", "qa_lead": "QA lead · lead's level", "tester_inh": "tester, while it inherited the lead's model",
              "reviewer": "reviewer · lead's level", "tester": "tester · Sonnet", "builder": "builder · Sonnet", "reader": "reader · Sonnet", "builder_haiku": "builder · Haiku, by hand-off"},
    ba_share1="a working day: US$ 163 before, US$ 137 after — with three times more rounds done",
    ba_share2="rounds on the most expensive model: nine in ten before, about one in three after",
    cap_ba="The invoice, per round, before and after the lead and the helpers went in. Before, every round was the session itself on the expensive model. After, the lead's rounds cost half as much and the rounds that moved to the helpers cost a tenth. The red bar is the tester during the weeks it silently inherited the lead's model.",
    aria_ba="Horizontal bar chart of US dollars per round: one bar before at 0.52, then eight bars after, from the lead at 0.24 down to the builder on Haiku at 0.01; the tester while inheriting the lead's model is highlighted in red at 0.13.",
)

PT = dict(
    median="mediana · 242", spread_x="36 tarefas, cinco semanas — uma barra por tarefa", spread_right="em ordem de tamanho",
    spread_y="rodadas de trabalho (cada uma reenvia a conversa inteira)",
    cap_spread="Trinta e seis tarefas, uma barra cada. A menor custou nove dólares, a maior 945, e entre elas está todo tipo de trabalho que um time de entrega faz em cinco semanas. As quatro que o artigo acompanha estão em azul. Todas as trinta e seis rodaram no mesmo modelo.",
    aria_spread="Gráfico de barras de 36 tarefas ordenadas por número de rodadas, de 1 a 2.450, com linha dourada de mediana em 242 e quatro barras azul-marinho rotuladas A, B, C e D.",
    turn_title="uma rodada de trabalho", ctx="a conversa", ctx_sub="tokens reenviados, em média", model="o modelo", model_sub="lê tudo, de novo",
    out="a resposta", out_sub="tokens escritos, em média",
    cost_title="para onde vão os 37 centavos", c_read="reler o que já tinha visto · 73%", c_write="cache · 20%", c_out="a resposta · 7%",
    cost_note="O raciocínio mora dentro desses 7%. O que um agente custa não é o que ele escreve — é o que ele relê.",
    lever_title="o que deixa exatamente duas alavancas",
    lever_1="O modelo define o preço de todas as linhas: na época, Opus US$ 5, Sonnet US$ 2, Haiku US$ 1 por milhão de tokens lidos.",
    lever_2="O nível de esforço define quantas rodadas existem: menos esforço, passos maiores, menos rodadas.",
    lever_3="Rodada média nas cinco semanas: 509 mil tokens de entrada, 1 mil de saída, 37 centavos.",
    cap_turn="Uma rodada de trabalho, desmontada. O agente reenvia meio milhão de tokens para conseguir escrever mil — então três quartos da conta é releitura, e o modelo que você escolhe define o preço de cada uma delas.",
    aria_turn="Uma conversa de 509.000 tokens entra numa caixa azul-marinho do modelo e uma resposta de 1.000 tokens sai; abaixo, uma barra de custo dividida em 73% releitura, 20% cache, 7% resposta; um painel tracejado lista as duas alavancas.",
    ax_x="quanto trabalho", ax_x_lo="um lugar", ax_x_hi="muitos lugares, um padrão", ax_y="quanta dúvida", ax_y_lo="o pedido está certo", ax_y_hi="o pedido pode estar errado",
    q_tl="descobrir a verdade", q_tr="descobrir, depois repetir", q_bl="só fazer", q_br="fazer muitas vezes",
    pA="Sonnet · baixo", pB="Opus, depois 14 × Haiku", pC="Opus · máximo", pD="muda enquanto você trabalha", d_note="a quarta atravessa o mapa",
    cap_map="Duas perguntas, quatro respostas. A dúvida compra o modelo; o volume compra o nível de esforço e, passado certo ponto, mais mãos. Três das quatro tarefas ficam paradas num quadrante. A quarta não fica — e é aí que mora o argumento a favor de um líder.",
    aria_map="Um mapa dois por dois com dúvida na vertical e quantidade de trabalho na horizontal; tarefa A embaixo à esquerda Sonnet baixo, B embaixo à direita Opus e depois catorze Haiku, C em cima à esquerda Opus máximo, D em cima à direita com arco dourado tracejado atravessando o mapa.",
    b_top="o que aconteceu — um modelo, uma conversa", b_top_note="cinco vezes tive de trazer de volta ao rumo; duas tarefas emaranhadas num fio",
    b_bot="o que o trabalho de fato era", lead="Opus", lead_sub="escreve a regra, uma vez", workers="14 × Haiku · em paralelo, um item cada",
    workers_sub="um contexto limpo a cada um, então nada consegue se emaranhar", lead2="Opus", lead2_sub="revisa os dois reais",
    back="2 voltam", back_sub="os outros 12 eram o mesmo engano",
    cap_caseb="A tarefa repetida, desenhada duas vezes. Acima, os US$ 660 como foram de fato gastos, com uma bandeira onde tive de trazer a conversa de volta ao rumo. Abaixo, a forma que o trabalho sempre teve: escrever a regra uma vez, aplicá-la catorze, julgar duas.",
    aria_caseb="Faixa superior: uma longa seta azul-marinho de 1.997 rodadas com cinco bandeiras vermelhas marcando correções humanas. Faixa inferior: uma caixa Opus escreve uma regra, distribui para catorze caixas Haiku em paralelo, e dois resultados voltam para revisão.",
    d_title="a quarta tarefa · dez dias · US$ 945",
    d1="ler", d2="3 de 4 já existiam", d3="investigar", d4="construir a tela", d5="renegociar",
    d_start="dia 1", d_end="dia 10", n_mech="mecânico — território do Haiku", n_vol="volume — um padrão, muitos lugares", n_judge="julgamento — o pedido estava errado",
    d_point1="Escolha um modelo no dia um e você estará errado no dia quatro.",
    d_point2="A escolha tem de ser feita por tarefa, com o trabalho em andamento — o que significa que alguém precisa estar fazendo essa escolha.",
    cap_cased="A maior tarefa, colorida pelo tipo de trabalho que cada trecho exigiu. Abre em julgamento, vira volume, fica mecânica e termina em julgamento de novo. Nenhuma escolha única feita no início sobrevive ao meio.",
    aria_cased="Uma linha do tempo horizontal da quarta tarefa em cinco segmentos coloridos pela natureza do trabalho, com legenda e nota de fecho abaixo.",
    lead_box="o líder", lead_box_sub="Opus · a própria sessão",
    lead_line1="lê o pedido, divide o trabalho, segura o escopo, julga o que volta",
    w=[("leitor", ["model: sonnet", "effort: low", "maxTurns: 25", "lê, nunca escreve"]),
       ("construtor", ["model: sonnet", "effort: medium", "maxTurns: 80", "uma mudança decidida"]),
       ("testador", ["model: sonnet", "effort: high", "maxTurns: 120", "nível vem na entrega"]),
       ("revisor", ["model: inherit", "effort: high", "maxTurns: 40", "no nível do líder"]),
       ("líder de QA", ["model: inherit", "effort: high", "maxTurns: 160", "despacha os testadores"])],
    rt_title="e o líder pode sobrescrever o modelo em qualquer entrega isolada",
    rt_1="“Este lote é trivial — roda no Sonnet.”",
    rt_2="O arquivo define o padrão. A entrega define a exceção. O líder segura os dois.",
    rt_3="São as configurações reais dos cinco arquivos dos ajudantes, não uma metáfora.",
    cap_leader="O que substituiu um modelo para tudo, como foi configurado de fato: um líder que decide e nunca executa, três ajudantes no modelo mais barato que leem, constroem e testam, e dois adversários — o revisor e o líder de QA — que rodam de propósito no nível do próprio líder.",
    aria_leader="Uma caixa líder azul-marinho conecta a cinco caixas de ajudantes rotuladas leitor, construtor, testador, revisor e líder de QA, cada uma mostrando linhas de configuração para modelo, esforço e limite de turnos.",
    ba_title="quanto custou uma rodada, antes e depois", ba_unit="US$ por rodada · preço de lista",
    ba_before="antes · a sessão sozinha, no Opus",
    ba_after="depois · por papel",
    ba_roles={"lead": "o líder", "qa_lead": "líder de QA · nível do líder", "tester_inh": "testador, enquanto herdava o modelo do líder",
              "reviewer": "revisor · nível do líder", "tester": "testador · Sonnet", "builder": "construtor · Sonnet", "reader": "leitor · Sonnet", "builder_haiku": "construtor · Haiku, por entrega"},
    ba_share1="um dia de trabalho: US$ 163 antes, US$ 137 depois — com três vezes mais rodadas feitas",
    ba_share2="rodadas no modelo mais caro: nove em dez antes, cerca de uma em três depois",
    cap_ba="A fatura, por rodada, antes e depois de o líder e os ajudantes entrarem. Antes, toda rodada era a própria sessão no modelo caro. Depois, as rodadas do líder custam a metade e as que foram para os ajudantes custam um décimo. A barra vermelha é o testador nas semanas em que herdou em silêncio o modelo do líder.",
    aria_ba="Gráfico de barras horizontais de dólares por rodada: uma barra antes em 0,52, depois oito barras, do líder em 0,24 até o construtor no Haiku em 0,01; o testador enquanto herdava o modelo do líder destacado em vermelho em 0,13.",
)


def figs(L):
    return dict(spread=fig_spread(L), turn=fig_turn(L), map=fig_map(L), caseb=fig_caseb(L), cased=fig_cased(L), leader=fig_leader(L), beforeafter=fig_beforeafter(L))


# ---------------------------------------------------------------- the articles
EN_MD = """---
title: "The Cheap Team"
date: 2026-10-14T08:00:00-04:00
draft: false
translationKey: "model-effort"
categories: ["Technology"]
tags: ["ai-agents", "cost", "management", "delegation", "software-delivery", "spending-less-on-ai"]
description: "Episode 4 of Spending Less on AI. Cutting tokens raised our bill. So we stopped saving tokens and started managing models: the expensive one decides, cheap ones execute. Sixteen days later, the invoice: a round of work at a quarter of the price, a working day 16% cheaper — and the lead is now the bill."
---

*Fourth episode of **Spending Less on AI**. Episodes 1 and 2, {{{{< episode 1 >}}}}
and {{{{< episode 2 >}}}}, installed a tool that promised a lighter bill by sending
fewer tokens to the model. Episode 3, {{{{< episode 3 >}}}}, opened the invoice: the
tokens fell 46% and the bill rose 14%, because tokens are not what the provider
charges for. This is what we did next.*

---

For three episodes this series tried to spend less on AI by sending less
text to the model. It is the obvious idea, every tool in this market sells
it, and in our hands it failed. The tool cut what the agent sends by nearly
half, and a round of work came out 14% dearer. Episode 3 explained why: a
token is what the provider counts, the invoice has four lines at four
prices, and the line the tool shrank is the cheapest of the four.

The same episode ended on the one lever that had moved our bill more than
any tool, in both directions: which model answered which kind of task. So
we stopped saving tokens and pulled that lever instead. This episode is the
receipt.

The short answer is yes, it saved money. The long answer is more
interesting, because the bill did not fall the way the arithmetic said it
would, and the reason points straight at the next episode.

## Where the idea came from

It came from a spreadsheet I kept for five weeks, not to study anything,
just to know. An AI coding agent had been doing the delivery work on a
client platform for months, and I had never looked at the invoice task by
task. Thirty-six tasks went in. At list price they came to **$5,908**.

{spread}

Sorted, the sheet showed one thing before it showed anything else: every
task had run on the same model, at the same effort, from the one that took
a single round of work to the one that took two and a half thousand. Not
because anyone had weighed it. Because that was the setting the session
opened with, months earlier, and nobody had touched it since.

Then I went looking for the worst case and found a task that cost **$660**
to work through fourteen items from an automated report, one at a time.
The agent did good work: it traced each item, wrote a short rule to tell a
real finding from a false one, and applied it. Twelve of the fourteen were
false, and eleven of the twelve were the *same* false finding. The task
needed one judgment and thirteen repetitions of it, and it got the most
expensive model doing all fourteen in one long conversation, re-reading
everything it had learned about the first thirteen before touching the
last. Five times I had to pull it back on course.

{caseb}

And then the opposite case, which is why the answer is not "use the cheap
model". A **$304** task opened with one sentence: something the system
sends arrives wrong on the other side. The agent doubted the sentence, read
years of history, and found that a piece everybody assumed was added
automatically had stopped being added during an old upgrade. Nine things
were broken, not the one in the request. No cheap model asks that question.
Three hundred dollars was the price of doubt, and the best three hundred of
the five weeks.

Two kinds of work, then. Judgment, which wants the expensive model. And
repetition, which wants anything but. One price for both.

## What a round of work costs

To see why the price matters so much, you have to see what a round is.

{turn}

An agent has no memory between one action and the next. Every time it does
something, it sends the whole conversation back to the model and asks what
to do now. That is one round, and by the afternoon each one carries the
equivalent of a 350-page book. The book is four lines on the invoice:
re-read from the cache at a tenth of the price of new text, new text at
full price, text written into the cache at up to twice, and the answer at
five times. In the five weeks, with nothing disturbing the cache,
re-reading was 73 cents of every dollar and the answer, thinking included,
seven.

The **model** multiplies all four lines at once. At the time, Opus read at
five dollars per million tokens, Sonnet at two, Haiku at one. Same book,
same number of rounds, less than half the cost on Sonnet and a fifth on
Haiku. The **effort level** sets how many rounds there are: lower effort,
fewer and larger steps, fewer books re-sent.

That is the whole idea. Keep the expensive model for the judgment, hand the
repetition to a cheaper one, and let somebody decide which is which, task
by task.

## What we changed, and for how long

At the end of September, on the same client platform, one model for
everything was replaced by a lead and five helpers.

{leader}

The lead is the session itself, on the expensive model, and it does three
things only: reads the request and decides whether it can be trusted,
splits the work and picks who does each piece, and holds the scope while
the others work, judging what comes back. It does not read fourteen items.

The helpers are five short configuration files, each naming a model, an
effort level and a turn limit. A **reader** on Sonnet at low effort, which
reads and never writes. A **builder** on Sonnet at medium effort, which
implements one settled change and never negotiates with the request. A
**tester** on Sonnet, dispatched by a **QA lead** that decides what the
testing has to cover. And a **reviewer** that attacks the plan before any
work is handed out. The reviewer and the QA lead run at the lead's own
level, on purpose: a reviewer below the lead can only review spelling.

And because a big task changes shape while it runs, the lead can override
the model on any single hand-off. When a batch turns out to be trivial it
says *Haiku, this one* and moves on. The file sets the default; the
hand-off sets the exception.

This has been running since 29 September. The invoice below compares the
twenty-four working days before it, all on the expensive model, with the
sixteen days since, ten of them working days, on the same platform with
the same operator.

## What the invoice says

{beforeafter}

Before, every round was the session itself on the expensive model, and a
round cost **52 cents**. After, the lead's own rounds cost 24 — part of
that is a newer generation of the same model, priced a fifth lower, and
part is a lead that takes fewer, larger steps because it no longer
executes. The rounds that moved to the helpers cost **four to five cents**.
The batches the lead sent to Haiku by hand cost one. Nine in ten rounds ran
on the most expensive model before; about one in three after.

The invoice also showed me something I had not configured. The tester had
no model of its own: it inherited whatever the session was running, which
was the most expensive one, and it did **1,441 rounds** that way at 13
cents each before anyone noticed. Since the file got the one line it was
missing, the same job costs under five cents a round. Nobody made a bad
call there. Nobody made a call, and the default is invisible until you go
looking.

## So: did it save money?

Yes. Per round of work, a quarter of the price: 37 cents on average before,
9 after. Per working day, **$163 before and $137 after**, 16% less — while
the agent did three times as many rounds, because helpers take many small
steps where the session took few large ones. Read it as: the day cost less
and more got done, not as three times the work.

Sixteen per cent is less than the thirty the arithmetic promised when this
article was still a draft, and the invoice says why. The lead's rounds
cost 24 cents and it still does about four hundred of them a day. On a
quiet day it is seventy per cent of the bill. We moved from *everything on
the expensive model* to *the lead on the expensive model*, and the lead is
now the bill. That is the next lever, and the next episode.

Put the two experiments side by side. The tool of episodes 1 to 3 cut
tokens by 46% and made a round 14% dearer. Managing models did not touch
the tokens — the agent sends more than ever — and made a round 75%
cheaper. Spending less on AI was never about tokens. It is about who does
the work, and what you pay them per round.

The spreadsheet is still open.

---

*Method, in short. One client platform, the same operator throughout. The
five weeks are 36 tasks with every round attributed to the task that asked
for it, 15 August to 21 September. The before and after is every round of
the same platform from 31 August to 28 September against every round from
29 September to 14 October, each priced at the provider's published rate
for the model that answered it and attributed to the role that ran it, from
the agent's own logs. Part of the after window still ran through the proxy
of episodes 1 to 3, which makes a round dearer, so the after is, if
anything, overstated; the days after the proxy was removed show the same
per-round levels. All values are list-price equivalents: we pay a fixed
monthly plan, and this series is the study we do before moving to metered
use.*
"""

PT_MD = """---
title: "O Time Barato"
date: 2026-10-14T08:00:00-04:00
draft: false
translationKey: "model-effort"
categories: ["Tecnologia"]
tags: ["agentes-de-ia", "custo", "gestão", "delegação", "entrega-de-software", "economizando-com-ia"]
description: "Episódio 4 de Economizando com IA. Cortar tokens subiu a nossa conta. Então paramos de economizar tokens e passamos a gerir modelos: o caro decide, os baratos executam. Dezesseis dias depois, a fatura: a rodada de trabalho a um quarto do preço, o dia de trabalho 16% mais barato — e o líder virou a conta."
---

*Quarto episódio de **Economizando com IA**. Os episódios 1 e 2, {{{{< episode 1 >}}}}
e {{{{< episode 2 >}}}}, instalaram uma ferramenta que prometia uma conta mais leve
enviando menos tokens ao modelo. O episódio 3, {{{{< episode 3 >}}}}, abriu a fatura:
os tokens caíram 46% e a conta subiu 14%, porque token não é o que o provedor
cobra. Isto é o que fizemos em seguida.*

---

Por três episódios esta série tentou gastar menos com IA enviando menos
texto ao modelo. É a ideia óbvia, toda ferramenta desse mercado vende
isso, e nas nossas mãos ela falhou. A ferramenta cortou quase pela metade o
que o agente envia, e a rodada de trabalho saiu 14% mais cara. O episódio 3
explicou por quê: token é o que o provedor conta, a fatura tem quatro
linhas a quatro preços, e a linha que a ferramenta encolheu é a mais barata
das quatro.

O mesmo episódio terminou na única alavanca que tinha movido a nossa conta
mais do que qualquer ferramenta, nas duas direções: qual modelo respondeu
que tipo de tarefa. Então paramos de economizar tokens e puxamos essa
alavanca. Este episódio é o comprovante.

A resposta curta é sim, economizou. A resposta longa é mais interessante,
porque a conta não caiu do jeito que a aritmética dizia que cairia, e o
motivo aponta direto para o próximo episódio.

## De onde saiu a ideia

Saiu de uma planilha que mantive por cinco semanas, não para estudar nada,
só para saber. Um agente de IA vinha fazendo o trabalho de entrega numa
plataforma de cliente havia meses, e eu nunca tinha olhado a fatura tarefa
por tarefa. Trinta e seis tarefas entraram. Em preço de lista, somaram
**US$ 5.908**.

{spread}

Ordenada, a planilha mostrou uma coisa antes de qualquer outra: toda tarefa
tinha rodado no mesmo modelo, no mesmo esforço, da que levou uma única
rodada de trabalho à que levou duas mil e quinhentas. Não porque alguém
tivesse pesado. Porque era a configuração com que a sessão abria, meses
antes, e ninguém tinha mexido nela desde então.

Aí fui procurar o pior caso e encontrei uma tarefa que custou **US$ 660**
para percorrer catorze itens de um relatório automático, um a um. O agente
fez bom trabalho: rastreou cada item, escreveu uma regra curta para separar
achado real de achado falso, e a aplicou. Doze dos catorze eram falsos, e
onze dos doze eram o *mesmo* achado falso. A tarefa precisava de um juízo e
treze repetições dele, e recebeu o modelo mais caro fazendo os catorze numa
única conversa longa, relendo tudo o que tinha aprendido sobre os treze
primeiros antes de tocar no último. Cinco vezes tive de trazê-la de volta
ao rumo.

{caseb}

E depois o caso oposto, que é por que a resposta não é "use o modelo
barato". Uma tarefa de **US$ 304** abriu com uma frase: algo que o sistema
envia chega errado do outro lado. O agente duvidou da frase, leu anos de
histórico, e descobriu que uma peça que todo mundo supunha inserida
automaticamente tinha deixado de ser inserida numa atualização antiga. Nove
coisas estavam quebradas, não a única do pedido. Nenhum modelo barato faz
essa pergunta. Trezentos dólares foi o preço da dúvida, e os melhores
trezentos das cinco semanas.

Dois tipos de trabalho, então. Julgamento, que quer o modelo caro. E
repetição, que quer qualquer um menos ele. Um preço para os dois.

## Quanto custa uma rodada de trabalho

Para ver por que o preço importa tanto, é preciso ver o que é uma rodada.

{turn}

Um agente não tem memória entre uma ação e a seguinte. Toda vez que faz
alguma coisa, manda a conversa inteira de volta ao modelo e pergunta o que
fazer agora. Isso é uma rodada, e à tarde cada uma já carrega o equivalente
a um livro de 350 páginas. O livro são quatro linhas na fatura: releitura
do cache a um décimo do preço do texto novo, texto novo a preço cheio,
texto gravado no cache a até o dobro, e a resposta a cinco vezes. Nas cinco
semanas, sem nada perturbando o cache, a releitura foi 73 centavos de cada
dólar e a resposta, raciocínio incluído, sete.

O **modelo** multiplica as quatro linhas de uma vez. Na época, o Opus lia a
cinco dólares por milhão de tokens, o Sonnet a dois, o Haiku a um. Mesmo
livro, mesmo número de rodadas, menos da metade do custo no Sonnet e um
quinto no Haiku. O **nível de esforço** define quantas rodadas existem:
menos esforço, passos maiores e em menor número, menos livros reenviados.

Essa é a ideia inteira. Guardar o modelo caro para o julgamento, entregar a
repetição a um mais barato, e deixar alguém decidir qual é qual, tarefa por
tarefa.

## O que mudamos, e por quanto tempo

No fim de setembro, na mesma plataforma do cliente, um modelo para tudo foi
substituído por um líder e cinco ajudantes.

{leader}

O líder é a própria sessão, no modelo caro, e faz só três coisas: lê o
pedido e decide se dá para confiar nele, divide o trabalho e escolhe quem
faz cada pedaço, e segura o escopo enquanto os outros trabalham, julgando o
que volta. Não lê catorze itens.

Os ajudantes são cinco arquivos curtos de configuração, cada um nomeando um
modelo, um nível de esforço e um limite de turnos. Um **leitor** no Sonnet
com esforço baixo, que lê e nunca escreve. Um **construtor** no Sonnet com
esforço médio, que implementa uma mudança já decidida e nunca negocia com o
pedido. Um **testador** no Sonnet, despachado por um **líder de QA** que
decide o que o teste precisa cobrir. E um **revisor** que ataca o plano
antes de qualquer trabalho ser distribuído. O revisor e o líder de QA rodam
no nível do próprio líder, de propósito: um revisor abaixo do líder só
consegue revisar ortografia.

E como uma tarefa grande muda de forma enquanto roda, o líder pode
sobrescrever o modelo em qualquer entrega isolada. Quando um lote se revela
trivial, ele diz *Haiku, neste* e segue. O arquivo define o padrão; a
entrega define a exceção.

Isso está rodando desde 29 de setembro. A fatura abaixo compara os vinte e
quatro dias úteis anteriores, todos no modelo caro, com os dezesseis dias
desde então, dez deles de trabalho, na mesma plataforma e com o mesmo
operador.

## O que a fatura diz

{beforeafter}

Antes, toda rodada era a própria sessão no modelo caro, e uma rodada custava
**52 centavos**. Depois, as rodadas do próprio líder custam 24 — parte
disso é uma geração mais nova do mesmo modelo, um quinto mais barata, e
parte é um líder que dá passos maiores e em menor número porque já não
executa. As rodadas que foram para os ajudantes custam **quatro a cinco
centavos**. Os lotes que o líder mandou à mão para o Haiku custam um. Nove
em dez rodadas rodavam no modelo mais caro antes; cerca de uma em três
depois.

A fatura também me mostrou algo que eu não tinha configurado. O testador
não tinha modelo próprio: herdava o que a sessão estivesse rodando, que era
o mais caro, e fez **1.441 rodadas** assim a 13 centavos cada antes de
alguém notar. Desde que o arquivo ganhou a linha que faltava, o mesmo
trabalho custa menos de cinco centavos por rodada. Ninguém tomou uma
decisão ruim ali. Ninguém tomou decisão nenhuma, e o padrão é invisível até
você ir procurar.

## Então: economizou ou não?

Sim. Por rodada de trabalho, um quarto do preço: 37 centavos em média
antes, 9 depois. Por dia de trabalho, **US$ 163 antes e US$ 137 depois**,
16% a menos — enquanto o agente fez três vezes mais rodadas, porque
ajudantes dão muitos passos pequenos onde a sessão dava poucos e grandes.
Leia assim: o dia custou menos e rendeu mais, não como três vezes o
trabalho.

Dezesseis por cento é menos do que os trinta que a aritmética prometia
quando este artigo ainda era rascunho, e a fatura diz por quê. As rodadas
do líder custam 24 centavos e ele ainda faz umas quatrocentas por dia. Num
dia calmo, ele é setenta por cento da conta. Saímos de *tudo no modelo
caro* para *o líder no modelo caro*, e o líder virou a conta. Essa é a
próxima alavanca, e o próximo episódio.

Ponha os dois experimentos lado a lado. A ferramenta dos episódios 1 a 3
cortou 46% dos tokens e deixou a rodada 14% mais cara. Gerir modelos não
tocou nos tokens — o agente envia mais do que nunca — e deixou a rodada 75%
mais barata. Economizar com IA nunca foi sobre tokens. É sobre quem faz o
trabalho, e quanto você paga a ele por rodada.

A planilha continua aberta.

---

*Método, em resumo. Uma plataforma de cliente, o mesmo operador do início
ao fim. As cinco semanas são 36 tarefas com cada rodada atribuída à tarefa
que a pediu, de 15 de agosto a 21 de setembro. O antes e depois é toda
rodada da mesma plataforma de 31 de agosto a 28 de setembro contra toda
rodada de 29 de setembro a 14 de outubro, cada uma precificada pela tarifa
publicada do provedor para o modelo que a respondeu e atribuída ao papel
que a rodou, a partir dos registros do próprio agente. Parte da janela de
depois ainda passou pelo proxy dos episódios 1 a 3, que encarece a rodada,
então o depois está, se algo, superestimado; os dias após a remoção do
proxy mostram os mesmos níveis por rodada. Todos os valores são
equivalentes a preço de lista: pagamos um plano mensal fixo, e esta série é
o estudo que fazemos antes de migrar para o uso medido.*
"""


def main():
    en = EN_MD.format(**figs(EN))
    pt = PT_MD.format(**figs(PT))
    (CONTENT / "en" / "writing" / "the-most-expensive-model.md").write_text(en, encoding="utf-8")
    (CONTENT / "pt-br" / "artigos" / "o-modelo-mais-caro.md").write_text(pt, encoding="utf-8")
    cover()
    print("wrote EN, PT, cover")


if __name__ == "__main__":
    main()
