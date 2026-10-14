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
    ba_share1="rounds on the most expensive model: nine in ten before, about one in three after",
    ba_share2="the weekly average round fell from about 40 cents to about 10",
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
    ba_share1="rodadas no modelo mais caro: nove em dez antes, cerca de uma em três depois",
    ba_share2="a rodada média da semana caiu de uns 40 centavos para uns 10",
    cap_ba="A fatura, por rodada, antes e depois de o líder e os ajudantes entrarem. Antes, toda rodada era a própria sessão no modelo caro. Depois, as rodadas do líder custam a metade e as que foram para os ajudantes custam um décimo. A barra vermelha é o testador nas semanas em que herdou em silêncio o modelo do líder.",
    aria_ba="Gráfico de barras horizontais de dólares por rodada: uma barra antes em 0,52, depois oito barras, do líder em 0,24 até o construtor no Haiku em 0,01; o testador enquanto herdava o modelo do líder destacado em vermelho em 0,13.",
)


def figs(L):
    return dict(spread=fig_spread(L), turn=fig_turn(L), map=fig_map(L), caseb=fig_caseb(L), cased=fig_cased(L), leader=fig_leader(L), beforeafter=fig_beforeafter(L))


# ---------------------------------------------------------------- the articles
EN_MD = """---
title: "The most expensive model, doing the cheapest work"
date: 2026-10-14T08:00:00-04:00
draft: false
translationKey: "model-effort"
categories: ["Technology"]
tags: ["ai-agents", "cost", "management", "delegation", "software-delivery", "spending-less-on-ai"]
description: "Episode 4 of Spending Less on AI. Five weeks of an AI coding agent, task by task, all on the most expensive model because nobody had chosen otherwise. What four tasks revealed about where the money goes, the lead-and-helpers setup that replaced one model for everything, and what the invoice said after: the average round of work fell from about 40 cents to about 10."
---

*Fourth episode of **Spending Less on AI**. Episodes 1 and 2, {{{{< episode 1 >}}}}
and {{{{< episode 2 >}}}}, tested a tool that promises a lighter bill. Episode 3,
{{{{< episode 3 >}}}}, showed that the number every such tool reports is not the
number on the invoice, and closed on the lever that moved our bill more than any
tool: which model answered which kind of task. This episode pulls that lever,
and comes back with the receipt.*

---

For five weeks I wrote down what every task cost.

Not to study anything. An AI coding agent had been doing the delivery work
on a client platform for months, I had never looked at the invoice in
detail, and it seemed like the sort of thing a person should know about his
own operation. Thirty-six tasks went into the spreadsheet. At list price
they came to **$5,908**.

When I finally sorted the sheet, the first thing I noticed was not a number.
It was how little the numbers varied.

{spread}

Tasks that took a single round of work and tasks that took two and a
half thousand had been done by the same model, at the same effort setting. The
cheapest cost nine dollars, the most expensive nine hundred and forty-five,
and nothing in between them had ever prompted a different choice. Not
because anyone had weighed it and decided so — because that was the setting
the session opened with, months earlier, and nobody had touched it since.

Then I looked for the worst offender, and found a task that cost **$660**
to work through a list of fourteen items that needed checking, one at a
time. Twelve of the fourteen turned out to be the same mistake repeated.

Six hundred and sixty dollars is not a catastrophe. But it was clearly the
wrong price for that work, and I could not explain *why* it had been so
expensive — which meant I did not actually understand what I was buying.

## What you are paying for

Here is the thing I had wrong, and I suspect I am not alone.

An agent has no memory between one action and the next. Every time it does
something — opens a file, runs a check, changes a line — it sends the whole
conversation back to the model and asks what to do now. That is one round of
work, and the five weeks were about sixteen thousand of them. By the
afternoon, each round carried the equivalent of a 350-page book.

{turn}

A round is four lines on the invoice, at four prices: text the model
re-reads from its cache, at a tenth of the price of new text; new text,
never seen before; text written into the cache, at up to twice; and the
answer it writes, at five times. Over these five weeks, with nothing
disturbing the cache, the split was **73 cents of every dollar on
re-reading, 20 on caching, 7 on the answer**. The part everyone pictures
when they imagine what AI costs — the answer, thinking included — is the
small one.

Episode 3 showed what happens when something does disturb the cache: the
20 grows until it is the bill. Nothing did here, which is what makes these
five weeks a clean reading of the other two settings, the ones you actually
control.

The **model** sets the price of all four lines at once. At the time, Opus
read at five dollars per million tokens, Sonnet at two, Haiku at one, and
the other three lines scale the same way. Same book, same number of rounds,
less than half the cost on Sonnet and a fifth on Haiku.

The **effort level** sets how many rounds there are. It is usually
described as how hard the model thinks, and on this kind of work that is
nearly beside the point, because thinking lives inside the seven per cent.
What lower effort really changes is behaviour: the agent takes fewer and
larger steps, and every step it does not take is a book it does not
re-send.

Price per round, and number of rounds. With those two numbers in hand I
went back to the spreadsheet, and the thirty-six tasks stopped looking like
a list.

## Four kinds of work

### The one with no decision in it — $9

Forty-two rounds, one day. A value that already existed in one part of
the system had to appear in another, and the request asked whether it was
available at the source. It was. After that the work was carrying one field
through three layers, and there was no judgment call anywhere in it.

Nine dollars is nothing. But on Sonnet at low effort it would have been
closer to three, doing exactly the same work — and there were twenty-odd
tasks of this size in five weeks. That is where the flat setting quietly
costs you: not in the big tasks, where it is often right, but in the many
small ones where it is never examined.

### The one that was a rule, applied fourteen times — $660

This was the task from the spreadsheet, and it is worth telling properly
because the money went somewhere unexpected.

An automated report had produced a list of fourteen items, each one a place
in the code that might or might not have a real problem. The analysis
itself was good work: the agent traced each one through the system, wrote a
short rule for telling a real finding from a false one, and applied that
rule to all fourteen. Twelve were false. Eleven of the twelve were the
identical false finding — the report had matched a naming pattern and
flagged eleven places that had nothing to do with the problem it was
looking for.

So the task needed **one** piece of judgment and thirteen mechanical
repetitions of it. What it got was the most expensive model doing all
fourteen, one after another, in a single conversation — which meant that by
the fourteenth item it was re-reading everything it had learned about the
first thirteen. The book grew all day.

And it got worse, because that conversation also picked up a second,
related task and the two got tangled. Five separate times I had to pull it
back on course: *focus on this one, don't mix them, what do I actually need
to decide?*

The $660 bought one good rule, thirteen expensive repetitions of it, and
five interventions from me.

{caseb}

Drawn the second way, the shape is obvious — and it is the shape the work
had all along. One expensive model writes the rule, once. Fourteen cheap
agents each take one item, apply the rule, and hand back a single line, in
parallel, each one starting from a clean slate that cannot get tangled with
anything because it has never heard of the second task. The expensive model
comes back only for the two findings that survive.

### The one that was worth every cent — $304

The opposite case, and I want it in here because the answer is not "use the
cheap model".

Nine hundred rounds, two days, and the request was a single sentence:
something the system sends out was arriving wrong at the other end. True,
and a symptom. The agent went into the history of the code and found that
several years earlier someone had centralised the piece that was now
missing — it used to be inserted automatically, so nobody producing that
kind of message ever had to supply it, and years of them were written on
that assumption. A later modernisation replaced the component with a leaner
one that sends only what it is explicitly given, and the automatic
insertion stayed behind in an old copy that nothing calls any more.

An assumption held for years had broken in silence. And it had broken
**nine things, not the one in the request**.

No cheap model finds that. Not because the cheaper ones lack skill, but
because the question — *why does everything here refer to something nobody
provides?* — only gets asked by a model willing to doubt the request, and
only gets answered by one willing to read a change from years ago. Three
hundred dollars was the price of the doubt, and it was the best three
hundred dollars of the five weeks. Fixing the one reported symptom would
have closed the request and left the other eight broken.

So: some tasks want the cheap model, some want the expensive one, and so
far the rule is easy. The fourth task is where it stops being easy.

### The one that changed the subject — $945

Two and a half thousand rounds, ten days.

The request listed four requirements. The agent read the code and reported
that three of them were already live and the fourth was impossible, because
another rule in the product forbids the action in exactly that situation.
That finding closed the request as written — and opened the real work,
which we agreed on afterwards: an investigation, instrumentation so the
behaviour could be traced, and a new screen.

{cased}

The investigation was the third task all over again. The screen was the
first task, thirty times. The instrumentation was the second task: one
pattern, repeated in five places.

Ten days, three kinds of work already described, one setting for all of it.

## Two questions

{map}

Once you have walked through the four, the sorting rule is simple, and it
is two questions rather than one.

**Can the request be trusted?** If the premise might be wrong, you are
buying judgment, and judgment is bought with the model. That is the
expensive one, at whatever effort the doubt requires, and it pays for
itself — the third task proves it.

**How much is there to do?** If the premise is sound, the model question
settles cheaply and only volume is left. Volume is the effort lever and,
past a certain size, the number of agents: not one model doing fourteen
things, but fourteen doing one thing each.

Three of the four tasks sit still in one square. The fourth crossed the
whole map in ten days — and in my experience most tasks above a certain
size are the fourth. Which is the problem with choosing a model at the
start of a task: for anything big enough to matter, there is no single
right answer to choose.

## Somebody has to be choosing

{leader}

So the choice moves. Instead of one setting for the session, a lead and a
few helpers.

The lead runs on the expensive model and does three things only: it reads
the request and decides whether it can be trusted; it splits the work into
tasks and picks who does each one; and it holds the scope while the others
work, judging what comes back. It does not read fourteen items. It does not
fill in thirty fields.

The helpers are short configuration files, each naming a model, an effort
level, a turn limit and the tools it is allowed to touch. This is what went
in at the end of September, on the same client platform. A **reader** on
Sonnet at low effort, read-only — for the fourteen items, and for every
automated report that will ever land. A **builder** on Sonnet at medium
effort — for the small task and for the thirty fields; it implements a
settled change and never negotiates with the request. A **tester** on
Sonnet, dispatched by a **QA lead** that decides what the testing has to
cover. And a **reviewer** that attacks the plan before any work is handed
out. The reviewer and the QA lead run at the lead's own level, on purpose:
a reviewer below the lead can only review spelling. The doubt — the third
task — stays with the lead, at whatever effort the doubt demands.

I had Haiku in mind for the reading. What went in was Sonnet at low effort,
and that difference is small next to the one that matters, between the
expensive model and either of them.

And because the fourth kind of task changes shape while it runs, the lead
can override the model for a single hand-off. It does not decide on day
one that this is an expensive-model task; it decides at each fork what the
*next* piece of work is, and when a batch turns out to be trivial it says
*Sonnet, this one* and moves on. The file sets the default. The hand-off
sets the exception.

## What it was worth, and the part I found last

The first draft of this article ended in arithmetic: move the mechanical
half of the rounds to Sonnet and the bill drops by almost a third. I did
not publish it, because a reader of this series is owed a measurement, not
a projection. So the lead and the helpers went in, the agent kept working
on the same platform, and I kept the spreadsheet open.

{beforeafter}

Here is what the invoice says, per round, at list price. Before, the
session did everything itself on the expensive model, and a round cost
**52 cents**. After, the lead's own rounds cost 24 cents — part of that is
a newer generation of the same model, priced a fifth lower, and part is a
lead that takes fewer, larger steps because it no longer executes. The
rounds that moved to the helpers cost **four to five cents** each, and the
batches the lead sent to Haiku by hand cost one. Across
whole weeks, the average round fell from about 40 cents to about 10, and
the share of rounds on the most expensive model fell from nine in ten to
about one in three.

Three honest caveats. These are list prices on a subscription, so this is
the shape of the bill, not an invoice. The weeks after are fewer than the
weeks before, and some of them ran through the proxy of episodes 1 to 3,
which makes a round dearer, not cheaper — so if anything the "after" is
overstated. And the comparison is per round, never per total: a total
moves with how much work happened, and the point of episode 3 was to stop
reading the wrong number.

The practical version is one question. Look at where your agent's rounds
went last month and check what model they ran on. If the answer is "the
best one, always", you are paying senior rates for filing.

I asked myself that question while the draft was still a draft, and the
answer was worse than I expected. The helper that runs the tests on every
task — the one thing that touches all of them — had no model of its own.
It inherited whatever the session was running, which was the most
expensive one, and had been doing so for weeks. The invoice has it in
plain sight now: 1,441 rounds of testing at 13 cents each before anyone
noticed, and the same job at under five cents a round since the file got
the one line it was missing.

Which is the whole point, really. The five weeks did not go wrong because
somebody made a bad call. They went wrong because nobody made a call at
all, and the default is invisible until you go looking for it.

I went looking. The spreadsheet is still open.

---

*Method, in short. One client platform, the same operator throughout. The
five weeks are 36 tasks with every round attributed to the task that asked
for it, 15 August to 21 September, priced at the provider's published
rates. The before and after is every round of the same platform from 31
August to 28 September against every round from 29 September onward, each
priced at the published rate of the model that answered it and attributed
to the role that ran it, from the agent's own logs. All values are
list-price equivalents: we pay a fixed monthly plan, and this series is the
study we do before moving to metered use.*
"""

PT_MD = """---
title: "O modelo mais caro, fazendo o trabalho mais barato"
date: 2026-10-14T08:00:00-04:00
draft: false
translationKey: "model-effort"
categories: ["Tecnologia"]
tags: ["agentes-de-ia", "custo", "gestão", "delegação", "entrega-de-software", "economizando-com-ia"]
description: "Episódio 4 de Economizando com IA. Cinco semanas de um agente de IA, tarefa por tarefa, tudo no modelo mais caro porque ninguém tinha escolhido outra coisa. O que quatro tarefas revelaram sobre para onde o dinheiro vai, o arranjo de líder e ajudantes que substituiu um modelo para tudo, e o que a fatura disse depois: a rodada média de trabalho caiu de uns 40 centavos para uns 10."
---

*Quarto episódio de **Economizando com IA**. Os episódios 1 e 2, {{{{< episode 1 >}}}}
e {{{{< episode 2 >}}}}, testaram uma ferramenta que promete uma conta mais leve. O
episódio 3, {{{{< episode 3 >}}}}, mostrou que o número que toda ferramenta dessas
exibe não é o número da fatura, e fechou na alavanca que moveu a nossa conta
mais do que qualquer ferramenta: qual modelo respondeu que tipo de tarefa. Este
episódio puxa essa alavanca, e volta com o comprovante.*

---

Durante cinco semanas, anotei quanto custava cada tarefa.

Não era para estudar nada. Um agente de IA vinha fazendo o trabalho de
entrega numa plataforma de cliente havia meses, eu nunca tinha olhado a
fatura em detalhe, e me pareceu o tipo de coisa que uma pessoa deveria
saber sobre a própria operação. Trinta e seis tarefas entraram na planilha.
Em preço de tabela, somaram **US$ 5.908**.

Quando finalmente ordenei a planilha, a primeira coisa que me chamou a
atenção não foi um número. Foi o quão pouco os números variavam.

{spread}

Tarefas que levaram uma única rodada de trabalho e tarefas que levaram
duas mil e quinhentas tinham sido feitas pelo mesmo modelo, no mesmo nível de esforço.
A mais barata custou nove dólares, a mais cara novecentos e quarenta e
cinco, e nada entre as duas jamais provocou uma escolha diferente. Não
porque alguém tivesse pesado e decidido assim — mas porque era a
configuração com que a sessão abria, meses antes, e ninguém tinha mexido
nela desde então.

Aí fui procurar o pior caso, e encontrei uma tarefa que custou **US$ 660**
para percorrer uma lista de catorze itens que precisavam ser conferidos, um
a um. Doze dos catorze acabaram sendo o mesmo engano, repetido.

Seiscentos e sessenta dólares não são uma catástrofe. Mas era claramente o
preço errado para aquele trabalho, e eu não conseguia explicar *por que*
tinha saído tão caro — o que significava que eu não entendia de fato o que
estava comprando.

## Pelo que você está pagando

Aqui está o que eu entendia errado, e desconfio que não estou sozinho.

Um agente não tem memória entre uma ação e a seguinte. Toda vez que faz
alguma coisa — abre um arquivo, roda uma verificação, muda uma linha — ele
manda a conversa inteira de volta ao modelo e pergunta o que fazer agora.
Isso é uma rodada de trabalho, e as cinco semanas foram cerca de dezesseis
mil delas. À tarde, cada rodada já carregava o equivalente a um livro de
350 páginas.

{turn}

Uma rodada são quatro linhas na fatura, a quatro preços: o texto que o
modelo relê do cache, a um décimo do preço do texto novo; o texto novo,
nunca visto; o texto gravado no cache, a até o dobro; e a resposta que ele
escreve, a cinco vezes. Nessas cinco semanas, sem nada perturbando o cache,
a divisão foi **73 centavos de cada dólar em releitura, 20 em gravação, 7
na resposta**. A parte que todo mundo imagina quando pensa no custo da IA —
a resposta, raciocínio incluído — é a pequena.

O episódio 3 mostrou o que acontece quando algo perturba o cache: os 20
crescem até virar a conta. Aqui nada perturbou, e é isso que faz destas
cinco semanas uma leitura limpa das outras duas configurações, as que você
de fato controla.

O **modelo** define o preço das quatro linhas de uma vez. Na época, o Opus
lia a cinco dólares por milhão de tokens, o Sonnet a dois, o Haiku a um, e
as outras três linhas escalam do mesmo jeito. Mesmo livro, mesmo número de
rodadas, menos da metade do custo no Sonnet e um quinto no Haiku.

O **nível de esforço** define quantas rodadas existem. Costuma ser descrito
como o quanto o modelo pensa, e neste tipo de trabalho isso é quase
irrelevante, porque o raciocínio mora dentro dos sete por cento. O que o
esforço menor muda de verdade é comportamento: o agente dá passos menos
numerosos e maiores, e cada passo que ele não dá é um livro que ele não
reenvia.

Preço por rodada, e número de rodadas. Com esses dois números na mão
voltei à planilha, e as trinta e seis tarefas deixaram de parecer uma
lista.

## Quatro tipos de trabalho

### A que não tinha decisão nenhuma — US$ 9

Quarenta e duas rodadas, um dia. Um valor que já existia numa parte do
sistema precisava aparecer em outra, e o pedido perguntava se ele estava
disponível na origem. Estava. Depois disso, o trabalho era levar um campo
por três camadas, e não havia juízo a fazer em ponto algum.

Nove dólares não são nada. Mas no Sonnet com esforço baixo teriam sido mais
perto de três, fazendo exatamente o mesmo trabalho — e havia vinte e tantas
tarefas desse tamanho em cinco semanas. É aí que a configuração fixa cobra
de você em silêncio: não nas tarefas grandes, onde ela costuma estar certa,
mas nas muitas pequenas, onde nunca é examinada.

### A que era uma regra, aplicada catorze vezes — US$ 660

Era a tarefa da planilha, e vale contar direito, porque o dinheiro foi
parar num lugar inesperado.

Um relatório automático tinha produzido uma lista de catorze itens, cada um
um ponto do código que podia ou não ter um problema real. A análise em si
foi bom trabalho: o agente rastreou cada um deles pelo sistema, escreveu
uma regra curta para separar achado real de achado falso, e aplicou essa
regra aos catorze. Doze eram falsos. Onze dos doze eram o mesmo achado
falso — o relatório tinha casado um padrão de nome e marcado onze pontos
que não tinham nada a ver com o problema que ele procurava.

Ou seja: a tarefa precisava de **um** juízo e treze repetições mecânicas
dele. O que ela recebeu foi o modelo mais caro fazendo os catorze, um atrás
do outro, numa única conversa — o que significa que, no décimo quarto item,
ele estava relendo tudo o que tinha aprendido sobre os treze primeiros. O
livro cresceu o dia inteiro.

E piorou, porque aquela conversa também pegou uma segunda tarefa
relacionada e as duas se emaranharam. Cinco vezes distintas tive de trazê-la
de volta ao rumo: *foco nesta, não mistura, o que eu preciso de fato
decidir?*

Os US$ 660 compraram uma boa regra, treze repetições caras dela, e cinco
intervenções minhas.

{caseb}

Desenhado do segundo jeito, a forma é óbvia — e é a forma que o trabalho
sempre teve. Um modelo caro escreve a regra, uma vez. Catorze agentes
baratos pegam um item cada, aplicam a regra e devolvem uma única linha, em
paralelo, cada um partindo de uma página em branco que não consegue se
emaranhar com nada porque nunca ouviu falar da segunda tarefa. O modelo
caro só volta para os dois achados que sobrevivem.

### A que valeu cada centavo — US$ 304

O caso oposto, e eu quero ele aqui porque a resposta não é "use o modelo
barato".

Novecentas rodadas, dois dias, e o pedido era uma frase só: algo que o
sistema envia chegava errado do outro lado. Verdade, e um sintoma. O agente
foi ao histórico do código e descobriu que, vários anos antes, alguém tinha
centralizado justamente a peça que agora faltava — ela era inserida
automaticamente, então ninguém que produzisse aquele tipo de mensagem
precisava fornecê-la, e anos de mensagens foram escritos sobre essa
suposição. Uma modernização posterior substituiu o componente por um mais
enxuto, que envia só o que recebe explicitamente, e a inserção automática
ficou para trás numa cópia antiga que nada mais chama.

Uma suposição sustentada por anos tinha quebrado em silêncio. E tinha
quebrado **nove coisas, não a única que o pedido citava**.

Nenhum modelo barato acha isso. Não porque falte capacidade aos mais
baratos, mas porque a pergunta — *por que tudo aqui se refere a algo que
ninguém fornece?* — só é feita por um modelo disposto a duvidar do pedido,
e só é respondida por um disposto a ler uma mudança de anos atrás.
Trezentos dólares foi o preço da dúvida, e foram os melhores trezentos
dólares das cinco semanas. Corrigir o único sintoma relatado teria fechado
o pedido e deixado os outros oito quebrados.

Então: algumas tarefas querem o modelo barato, outras querem o caro, e até
aqui a regra é fácil. A quarta tarefa é onde ela para de ser fácil.

### A que mudou de assunto — US$ 945

Duas mil e quinhentas rodadas, dez dias.

O pedido listava quatro requisitos. O agente leu o código e reportou que
três deles já estavam no ar e o quarto era impossível, porque outra regra
do produto proíbe a ação exatamente naquela situação. Esse achado fechou o
pedido como estava escrito — e abriu o trabalho de verdade, que combinamos
depois: uma investigação, instrumentação para que o comportamento pudesse
ser rastreado, e uma tela nova.

{cased}

A investigação era a terceira tarefa outra vez. A tela era a primeira
tarefa, trinta vezes. A instrumentação era a segunda tarefa: um padrão,
repetido em cinco lugares.

Dez dias, três tipos de trabalho já descritos, uma configuração para tudo.

## Duas perguntas

{map}

Depois de percorrer as quatro, a regra de triagem fica simples — e são duas
perguntas, não uma.

**Dá para confiar no pedido?** Se a premissa pode estar errada, você está
comprando julgamento, e julgamento se compra com o modelo. É o caro, no
esforço que a dúvida exigir, e ele se paga — a terceira tarefa prova.

**Quanto há para fazer?** Se a premissa é sólida, a questão do modelo se
resolve barato e só resta o volume. Volume é a alavanca do esforço e,
passado certo tamanho, o número de agentes: não um modelo fazendo catorze
coisas, mas catorze fazendo uma cada.

Três das quatro tarefas ficam paradas num quadrante. A quarta atravessou o
mapa inteiro em dez dias — e, na minha experiência, a maioria das tarefas
acima de certo tamanho é a quarta. O que é justamente o problema de
escolher o modelo no início de uma tarefa: para qualquer coisa grande o
bastante para importar, não existe uma resposta única a escolher.

## Alguém precisa estar escolhendo

{leader}

Então a escolha se muda de lugar. Em vez de uma configuração para a sessão,
um líder e alguns ajudantes.

O líder roda no modelo caro e faz só três coisas: lê o pedido e decide se
dá para confiar nele; divide o trabalho em tarefas e escolhe quem faz cada
uma; e segura o escopo enquanto os outros trabalham, julgando o que volta.
Não lê catorze itens. Não preenche trinta campos.

Os ajudantes são arquivos curtos de configuração, cada um nomeando um
modelo, um nível de esforço, um limite de turnos e as ferramentas que pode
tocar. Foi isto que entrou no fim de setembro, na mesma plataforma do
cliente. Um **leitor** no Sonnet com esforço baixo, só leitura — para os
catorze itens e para todo relatório automático que ainda vai chegar. Um
**construtor** no Sonnet com esforço médio — para a tarefa pequena e para
os trinta campos; ele implementa uma mudança já decidida e nunca negocia
com o pedido. Um **testador** no Sonnet, despachado por um **líder de QA**
que decide o que o teste precisa cobrir. E um **revisor** que ataca o plano
antes de qualquer trabalho ser distribuído. O revisor e o líder de QA rodam
no nível do próprio líder, de propósito: um revisor abaixo do líder só
consegue revisar ortografia. A dúvida — a terceira tarefa — fica com o
líder, no esforço que a dúvida exigir.

Eu tinha o Haiku em mente para a leitura. O que entrou foi o Sonnet com
esforço baixo, e essa diferença é pequena perto da que importa, entre o
modelo caro e qualquer um dos dois.

E como o quarto tipo de tarefa muda de forma enquanto roda, o líder pode
sobrescrever o modelo numa entrega isolada. Ele não decide no dia um que
aquilo é tarefa de modelo caro; decide a cada bifurcação o que é o
*próximo* pedaço de trabalho, e quando um lote se revela trivial diz
*Sonnet, neste* e segue. O arquivo define o padrão. A entrega define a
exceção.

## Quanto valeu, e a parte que encontrei por último

A primeira versão deste artigo terminava em aritmética: mover a metade
mecânica das rodadas para o Sonnet e a conta cai quase um terço. Não
publiquei, porque quem lê esta série tem direito a uma medição, não a uma
projeção. Então o líder e os ajudantes entraram, o agente seguiu
trabalhando na mesma plataforma, e eu deixei a planilha aberta.

{beforeafter}

Eis o que a fatura diz, por rodada, a preço de lista. Antes, a sessão fazia
tudo sozinha no modelo caro, e uma rodada custava **52 centavos**. Depois,
as rodadas do próprio líder custam 24 centavos — parte disso é uma geração
mais nova do mesmo modelo, um quinto mais barata, e parte é um líder que dá
passos menores em número e maiores em tamanho porque já não executa. As
rodadas que foram para os ajudantes custam **quatro a cinco centavos** cada,
e os lotes que o líder mandou à mão para o Haiku custam um. Em semanas
inteiras, a rodada média caiu de uns 40 centavos para uns 10, e
a fatia de rodadas no modelo mais caro caiu de nove em dez para cerca de
uma em três.

Três ressalvas honestas. São preços de lista numa assinatura, então isto é
a forma da conta, não uma fatura. As semanas de depois são menos que as de
antes, e parte delas passou pelo proxy dos episódios 1 a 3, que encarece a
rodada em vez de baratear — ou seja, se algo, o "depois" está
superestimado. E a comparação é por rodada, nunca por total: um total se
move com a quantidade de trabalho que houve, e o ponto do episódio 3 era
parar de ler o número errado.

A versão prática é uma pergunta. Olhe para onde foram as rodadas do seu
agente no mês passado e veja em que modelo elas rodaram. Se a resposta for
"no melhor, sempre", você está pagando hora de sênior para arquivar papel.

Fiz essa pergunta a mim mesmo quando o rascunho ainda era rascunho, e a
resposta foi pior do que eu esperava. O ajudante que roda os testes em toda
tarefa — a única coisa que encosta em todas — não tinha modelo próprio.
Herdava o que a sessão estivesse rodando, que era o mais caro, e vinha
fazendo isso havia semanas. A fatura agora mostra isso à vista: 1.441
rodadas de teste a 13 centavos cada antes de alguém notar, e o mesmo
trabalho a menos de cinco centavos por rodada desde que o arquivo ganhou a
linha que faltava.

O que é o ponto inteiro, no fundo. As cinco semanas não deram errado porque
alguém tomou uma decisão ruim. Deram errado porque ninguém tomou decisão
nenhuma, e o padrão é invisível até você ir procurar.

Eu fui procurar. A planilha continua aberta.

---

*Método, em resumo. Uma plataforma de cliente, o mesmo operador do início
ao fim. As cinco semanas são 36 tarefas com cada rodada atribuída à tarefa
que a pediu, de 15 de agosto a 21 de setembro, precificadas pelas tarifas
publicadas do provedor. O antes e depois é toda rodada da mesma plataforma
de 31 de agosto a 28 de setembro contra toda rodada de 29 de setembro em
diante, cada uma precificada pela tarifa publicada do modelo que a respondeu
e atribuída ao papel que a rodou, a partir dos registros do próprio agente.
Todos os valores são equivalentes a preço de lista: pagamos um plano mensal
fixo, e esta série é o estudo que fazemos antes de migrar para o uso
medido.*
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
