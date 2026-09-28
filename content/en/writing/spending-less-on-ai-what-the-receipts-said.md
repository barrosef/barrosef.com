---
title: "A tool to spend less on AI made my bill go up"
date: 2026-09-28T09:00:00-04:00
draft: false
translationKey: "headroom-receipts"
categories: ["Technology"]
tags: ["claude-code", "headroom", "ai-assisted-development", "tooling", "cost", "spending-less-on-ai"]
description: "Episode 2 of Spending Less on AI. The editor took his seat eight days ago; here is what the receipts say. It saved $439 and about $1,200 came back on another line — and the rule I wrote in advance had a blind spot exactly where the money went."
---

*Second episode of **Spending Less on AI**. The first one — [Headroom: the editor
between you and the model](/writing/headroom-the-editor-between-you-and-the-model/)
— described what the tool promises and set it up. This one reports what the
receipts say. Next week, episode three: the same tool, configured the way its
documentation describes rather than the way I improvised.*

---

Eight days ago I put a proxy between my coding agent and the model, wrote down
the rules of the test before the first request went through, and promised to
publish what the receipts said. This is that.

The short version: **it saved $439, and roughly $1,200 came back on another line
of the same invoice.**

Both halves are real. Understanding how they can both be true is the whole point
of this episode, and it is worth more than either number.

<!-- FIG:BALANCE -->
<figure class="diagram">
<svg viewBox="0 0 720 210" role="img" aria-label="Three bars: 439 dollars saved, about 1,200 dollars paid on top, leaving about 750 dollars negative." xmlns="http://www.w3.org/2000/svg" font-family="IBM Plex Sans, system-ui, sans-serif" color="#16233a"><text x="16" y="54" font-size="13.5" fill="#16233a">Saved on text sent</text><rect x="300" y="36" width="110" height="26" rx="5" fill="#1d7a4a"/><text x="422" y="55" font-size="16" font-weight="700" fill="#1d7a4a">+$439</text><text x="16" y="104" font-size="13.5" fill="#16233a">Paid on top in re-writes</text><rect x="300" y="86" width="300" height="26" rx="5" fill="#a4252c"/><text x="612" y="105" font-size="16" font-weight="700" fill="#a4252c">−$1,200</text><line x1="300" y1="124" x2="700" y2="124" stroke="#d5dde8"/><text x="16" y="154" font-size="13.5" fill="#16233a">Net, six days</text><rect x="300" y="136" width="188" height="26" rx="5" fill="#a4252c" opacity="0.85"/><text x="500" y="155" font-size="16" font-weight="700" fill="#a4252c">−$750</text><text x="16" y="198" font-size="11" fill="#16233a">$439 is measured. The other two are estimates — three scopes put the excess between $1,110 and $1,271.</text></svg>
<figcaption>The six days, as an account. The saving is real and the line beneath it is larger.</figcaption>
</figure>

## What it did, exactly as advertised

Six days of ordinary work. 3,994 requests, each one logged with what went in
before the proxy touched it and what went out after.

**6.4% less text sent to the model.** On `claude-opus-5`, which carries 91% of
what I spend, the proxy's own ledger puts the saving at **$438.94**. That is not
a vendor estimate and it is not my arithmetic — it is the tool's accounting of
its own work, and my request log agrees with it.

The editor did his job. He shortened the dossier before it went out the door.

## And the invoice went the other way

Here is the part I did not see coming.

An agent has no memory, so every step re-sends the whole conversation. The
provider stores that conversation and charges very little to read it back —
a tenth of the base rate. Storing it fresh costs **1.25×** the base rate. Between
reusing what is stored and storing it again there is a factor of **twelve and a
half**, for the same words.

<!-- FIG:PRICE -->
<figure class="diagram">
<svg viewBox="0 0 720 210" role="img" aria-label="Two bars comparing prices: reusing stored context costs one unit, storing it again costs twelve and a half." xmlns="http://www.w3.org/2000/svg" font-family="IBM Plex Sans, system-ui, sans-serif" color="#16233a"><text x="16" y="62" font-size="14" font-weight="600" fill="#16233a">Reuse what is stored</text><rect x="250" y="44" width="32" height="30" rx="6" fill="#1d4e89"/><text x="296" y="65" font-size="17" font-weight="700" fill="#1d4e89">1×</text><text x="16" y="136" font-size="14" font-weight="600" fill="#16233a">Store it again</text><rect x="250" y="118" width="400" height="30" rx="6" fill="#a4252c"/><text x="664" y="139" font-size="17" font-weight="700" fill="#a4252c">12.5×</text><text x="16" y="26" font-size="11" fill="#5d6b7d">price for the same words</text><text x="16" y="196" font-size="11" fill="#16233a">Cache read is 0.10× the base rate; cache write is 1.25×.</text></svg>
<figcaption>The same words, two prices. Anything that rewrites the start of a message moves tokens from the cheap column to the expensive one.</figcaption>
</figure>

The proxy shrinks the message by editing the *beginning* of it: the tool
definitions, the catalogue, the instructions that sit before everything else.
And the beginning of the message is exactly what the cache uses as its key.
Change one byte there and nothing after it can be reused. The whole conversation
gets stored again, at the expensive rate.

Worse, the amount it trims varies from request to request — twenty-eight tools
deferred on one call, twenty-one on the next, six on the one after. The prefix
never settles. So the cache never gets a chance to pay off.

What that looks like day by day:

<!-- FIG:DAILY -->
<figure class="diagram">
<svg viewBox="0 0 720 300" role="img" aria-label="Bar chart of twenty-one working days. The fifteen before the proxy sit between 0.4 and 7.6 percent; the six after it range from 13.1 to 37.5 percent." xmlns="http://www.w3.org/2000/svg" font-family="IBM Plex Sans, system-ui, sans-serif" color="#16233a"><rect x="60.0" y="239.4" width="26.7" height="10.6" fill="#c9d3df" rx="2"/><rect x="90.7" y="245.3" width="26.7" height="4.7" fill="#c9d3df" rx="2"/><rect x="121.3" y="231.8" width="26.7" height="18.2" fill="#c9d3df" rx="2"/><rect x="152.0" y="236.5" width="26.7" height="13.5" fill="#c9d3df" rx="2"/><rect x="182.7" y="245.9" width="26.7" height="4.1" fill="#c9d3df" rx="2"/><rect x="213.3" y="247.7" width="26.7" height="2.3" fill="#c9d3df" rx="2"/><rect x="244.0" y="243.0" width="26.7" height="7.0" fill="#c9d3df" rx="2"/><rect x="274.7" y="246.5" width="26.7" height="3.5" fill="#c9d3df" rx="2"/><rect x="305.3" y="241.2" width="26.7" height="8.8" fill="#c9d3df" rx="2"/><rect x="336.0" y="244.7" width="26.7" height="5.3" fill="#c9d3df" rx="2"/><rect x="366.7" y="235.9" width="26.7" height="14.1" fill="#c9d3df" rx="2"/><rect x="397.3" y="225.4" width="26.7" height="24.6" fill="#c9d3df" rx="2"/><rect x="428.0" y="224.2" width="26.7" height="25.8" fill="#c9d3df" rx="2"/><rect x="458.7" y="238.9" width="26.7" height="11.1" fill="#c9d3df" rx="2"/><rect x="489.3" y="205.4" width="26.7" height="44.6" fill="#c9d3df" rx="2"/><rect x="520.0" y="173.1" width="26.7" height="76.9" fill="#a4252c" rx="2"/><rect x="550.7" y="157.9" width="26.7" height="92.1" fill="#a4252c" rx="2"/><rect x="581.3" y="118.6" width="26.7" height="131.4" fill="#a4252c" rx="2"/><rect x="612.0" y="30.0" width="26.7" height="220.0" fill="#a4252c" rx="2"/><rect x="642.7" y="52.3" width="26.7" height="197.7" fill="#a4252c" rx="2"/><rect x="673.3" y="119.2" width="26.7" height="130.8" fill="#a4252c" rx="2"/><line x1="60" y1="250" x2="700" y2="250" stroke="#d5dde8" stroke-width="1.5"/><line x1="518.0" y1="22" x2="518.0" y2="250" stroke="#5d6b7d" stroke-width="1" stroke-dasharray="4 3"/><text x="524.0" y="18" font-size="11" fill="#5d6b7d">proxy switched on</text><text x="52" y="38" text-anchor="end" font-size="10.5" fill="#5d6b7d">40%</text><text x="52" y="137" text-anchor="end" font-size="10.5" fill="#5d6b7d">20%</text><text x="52" y="254" text-anchor="end" font-size="10.5" fill="#5d6b7d">0%</text><text x="60" y="270" font-size="10.5" fill="#5d6b7d">fifteen days before</text><text x="700" y="270" text-anchor="end" font-size="10.5" fill="#5d6b7d">six days after</text><text x="60" y="290" font-size="11" fill="#16233a">Stored again, as a share of what was reused — one bar per day.</text></svg>
<figcaption>The ratio of context stored again to context reused, per day. The median over the fifteen days before was 1.9%; the six days after ran between 13% and 37%.</figcaption>
</figure>

That is the whole mechanism. Less text, more money, no contradiction.

## The rules I wrote before I measured

Episode one committed to three numbers in advance, precisely so that I could not
bend them afterwards. Here is the scorecard.

| The rule I set | What the receipts say | |
|---|---|---|
| Tokens per request fall by **15% or more** | **6.4%** | missed |
| Re-reads and retrievals rise by **no more than a fifth** | re-reads **fell 31%**; retrievals were 28 events in 3,994 requests | met |
| Added latency under **4 seconds** at the ninetieth percentile | **9.5 seconds** (p99: 31s) | missed |

Two of three missed, and the rule I wrote said what to do in that case: fall back
to cache mode or lossless compaction, and say so. I am saying so.

## The part that actually taught me something

Look again at the middle row. It passed.

Re-reads did not rise — they *fell*, by nearly a third. Retrievals were a
rounding error. By the letter of my own rule, that criterion was met, and if I
had only watched what I said I would watch, I would have concluded that the
editor was behaving well.

Meanwhile, re-*writes* per request rose **527%**.

I built a rule to stop myself from moving the goalposts, and the rule had a blind
spot exactly where the money went. I was watching the cheap half of the cache and
had written nothing about the expensive half.

If you take one thing from this episode, take that one. Not "compression proxies
are bad" — they are not. **The measurement you design before the experiment is
itself a hypothesis, and it can be wrong in ways the experiment will not tell
you about.** Mine was.

## Where it does work

The same tool, the same week, three different models:

<!-- FIG:MODEL -->
<figure class="diagram">
<svg viewBox="0 0 720 250" role="img" aria-label="Three horizontal bars: Opus saves 5.4 percent and is 91 percent of the spend; Sonnet saves 32.6 percent and is 3 percent; Haiku saves 44.1 percent and is 0.3 percent." xmlns="http://www.w3.org/2000/svg" font-family="IBM Plex Sans, system-ui, sans-serif" color="#16233a"><text x="16" y="56" font-size="14" font-weight="600" fill="#16233a">Opus</text><text x="16" y="73" font-size="10.5" fill="#5d6b7d">share of spend: 91%</text><rect x="130" y="40" width="420" height="28" rx="6" fill="#eef2f7"/><rect x="130" y="40" width="45" height="28" rx="6" fill="#1d7a4a"/><text x="566" y="60" font-size="15" font-weight="700" fill="#1d7a4a">−5.4%</text><rect x="646" y="46" width="109" height="16" rx="3" fill="#a4252c"/><text x="16" y="118" font-size="14" font-weight="600" fill="#16233a">Sonnet</text><text x="16" y="135" font-size="10.5" fill="#5d6b7d">share of spend: 3%</text><rect x="130" y="102" width="420" height="28" rx="6" fill="#eef2f7"/><rect x="130" y="102" width="274" height="28" rx="6" fill="#1d7a4a"/><text x="566" y="122" font-size="15" font-weight="700" fill="#1d7a4a">−32.6%</text><rect x="646" y="108" width="4" height="16" rx="3" fill="#a4252c"/><text x="16" y="180" font-size="14" font-weight="600" fill="#16233a">Haiku</text><text x="16" y="197" font-size="10.5" fill="#5d6b7d">share of spend: 0.3%</text><rect x="130" y="164" width="420" height="28" rx="6" fill="#eef2f7"/><rect x="130" y="164" width="370" height="28" rx="6" fill="#1d7a4a"/><text x="566" y="184" font-size="15" font-weight="700" fill="#1d7a4a">−44.1%</text><rect x="646" y="170" width="3" height="16" rx="3" fill="#a4252c"/><text x="130" y="28" font-size="10.5" fill="#5d6b7d">text saved</text><text x="646" y="28" font-size="10.5" fill="#5d6b7d">share of spend</text><text x="16" y="238" font-size="11" fill="#16233a">It performs six to eight times better on the models that carry almost none of the bill.</text></svg>
<figcaption>Text saved per model against each model's share of my spend. The green bar is the saving; the red bar is where the money actually is.</figcaption>
</figure>

Six to eight times more effective on the cheap models than on the expensive one —
and the expensive one is where practically all the money is.

That is not a flaw in the tool, it is a mismatch between where it can reach and
where my spend lives. My sessions on the big model are long, and what fills them
is the accumulated conversation, not tool output. Across the whole period, tool
results were **under 1% of the traffic**. A proxy that compresses tool output
cannot move a number that is dominated by the conversation being re-read.

On short, cheap, disposable work — a subagent that reads three files and answers
— it does very well indeed.

## What I did not run

I have to be straight about the scope of this verdict, because it is narrower
than the headline.

I ran the basic setup: start the proxy, point the agent at it, protect file
contents from compression, truncate tool descriptions. That is what episode one
described, and it is what I measured.

It is not what the documentation describes. Four of the tool's capabilities were
never switched on, and one of them reduces the *answer* rather than the question
— the output side, which on the expensive model costs five times what input
costs, and which in my case has never produced a single measurement. The routing
is also incomplete: some of my sessions bypassed the proxy entirely, which means
these numbers understate the traffic and overstate the tool's share of the damage
at the same time.

So this is a reading of my configuration. It is not a verdict on the tool.

## Before you buy efficiency for your own AI spend

Five questions, in the order I wish I had asked them.

**Which unit does it optimise, and is that the unit on your invoice?** Tokens,
requests, context window and dollars are four different things, and an
optimisation can win on one while losing on another.

**If it touches the start of the prompt, measure the cache.** Anything that
rewrites the prefix invalidates everything after it. Watch stored-again against
reused, not just total volume.

**Compare money on comparable days.** My first attempt at this analysis announced
an 18% improvement that evaporated the moment I controlled for how the days were
structured. Percentages of text are easy and misleading; dollars per comparable
unit of work are harder and honest.

**Aim it where the spend actually is.** If 90% of your bill is one model, a tool
that performs beautifully on the other 10% will not show up on the invoice.

**Set a ceiling before you switch anything on.** I had none. An optimisation that
silently costs more is exactly the failure mode a ceiling catches.

## Episode three

Next week, the same tool, configured the way its documentation describes: the
output reducer switched on, routing made durable so that every session actually
goes through it, the work aimed at the models where it already performs, and a
spending ceiling in place.

Then I measure again and publish that number too, whichever way it goes. If it
earns the chair, I will say so. It has not earned it yet.

*Versions: Headroom 0.36.5, Claude Code 2.1.278, September 2026. The numbers come
from my own Claude Code transcripts and the proxy's request log, on one real
project that is not the subject and is not named. The $439 and the percentages
are measured; the ~$1,200 and the ~−$750 net are estimates — three independent
scopes put the excess between $1,110 and $1,271, and 290 idle gaps longer than an
hour over the period break the cache on their own, which makes that figure an
upper bound on what the proxy alone cost.*
