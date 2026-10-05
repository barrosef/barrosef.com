---
title: "The Death of Tokens"
date: 2026-10-05T09:00:00-04:00
draft: false
translationKey: "death-of-tokens"
categories: ["Technology"]
tags: ["claude-code", "ai-assisted-development", "tooling", "cost", "prompt-caching", "spending-less-on-ai"]
description: "Episode 3 of Spending Less on AI. Every tool that promises to cut your AI bill shows you tokens going down. We opened the invoice line by line: tokens fell 46% and the bill rose 14%. Where the money actually lives, and why the number everyone quotes stopped meaning anything."
---

*Third episode of **Spending Less on AI**. Episode 1, {{< episode 1 >}},
set up a tool that promises a lighter bill by sending less text to the model.
Episode 2, {{< episode 2 >}}, reported the
first receipts. This one is not about the tool any more. It is about the number
every tool in this market shows you, and why that number no longer tells you
what you will pay.*

---

Every product that promises to cut your AI bill shows you the same chart: a
line called **tokens** going down. Sixty percent fewer. Ninety-five percent
fewer. The chart is usually true.

The bill is a different document. We opened ours line by line, over 44 working
days and four projects, and the two documents disagree. **On the project where
we sent less text to the model, the text it re-read fell by 46% per round of
work and the cost per round went up 14%.**

This episode is the anatomy of that disagreement. If you pay for AI by the
month, it changes which number you should be asking your team for.

## A token is not a price

A token is roughly three-quarters of a word. It is the unit the provider counts.
It is also, since 2024, **not the unit the provider charges**, and this is the
whole story.

A coding agent works in rounds. In each round it sends the model the entire
conversation so far (every instruction, every file it read, every result it got
back) and receives one answer. The conversation grows every round, so by the
afternoon each round carries hundreds of thousands of tokens.

Sending all of that at full price would be ruinous, so the provider offers a
deal called a cache. Text the model has already seen can be **re-read** at a
tenth of the price of new text. In exchange, the first time a stretch of text
is stored, you pay a premium to **write** it: 1.25 times the new-text price for
a five-minute cache, twice the price for an hour-long one. And the **answer**
the model writes costs five times what new text costs.

So one round of work is four lines on the invoice, at four different prices:

| What is billed | Price, relative to new text |
|---|---|
| text re-read from cache | 0.1× |
| new text, never seen | 1× |
| text written to cache (5 min / 1 hour) | 1.25× / 2× |
| the answer the model generates | 5× |

A token on the first line is worth one-fiftieth of a token on the last line.
"Tokens went down" is a sentence about the sum of four quantities that should
never have been added together.

## Where the tokens are, and where the money is

Here is our corpus: 44 days, four projects, 11.9 billion tokens, US$ 10,206 at
list price. The first bar is where the tokens are. The second is where the
money is.

<!-- FIG:SHARES -->
<figure class="diagram">
<svg viewBox="0 0 720 250" role="img" aria-label="Two bars. Where the tokens are: 96% cache reads. Where the money is: 50% cache reads, 42% cache writes, 8% answers." xmlns="http://www.w3.org/2000/svg" font-family="IBM Plex Sans, system-ui, sans-serif" color="#16233a"><text x="16" y="69" font-size="13.5" fill="#16233a">Where the tokens are</text><rect x="230.0" y="50" width="449.3" height="30" fill="#6b8ef2"/><text x="454.7" y="70" font-size="13" font-weight="700" text-anchor="middle" fill="#fff">95.6%</text><rect x="681.3" y="50" width="19.3" height="30" fill="#2a5bd7"/><rect x="702.6" y="50" width="1.5" height="30" fill="#1d7a4a"/><text x="16" y="139" font-size="13.5" fill="#16233a">Where the money is</text><rect x="230.0" y="120" width="237.3" height="30" fill="#6b8ef2"/><text x="348.7" y="140" font-size="13" font-weight="700" text-anchor="middle" fill="#fff">50.5%</text><rect x="469.4" y="120" width="195.5" height="30" fill="#2a5bd7"/><text x="567.1" y="140" font-size="13" font-weight="700" text-anchor="middle" fill="#fff">41.6%</text><rect x="666.9" y="120" width="37.1" height="30" fill="#1d7a4a"/><rect x="230" y="178" width="12" height="12" fill="#6b8ef2"/><text x="247" y="189" font-size="12" fill="#16233a">cache reads</text><rect x="400" y="178" width="12" height="12" fill="#2a5bd7"/><text x="417" y="189" font-size="12" fill="#16233a">cache writes</text><rect x="570" y="178" width="12" height="12" fill="#1d7a4a"/><text x="587" y="189" font-size="12" fill="#16233a">answers</text><text x="16" y="236" font-size="11" fill="#16233a">44 days, four projects, 11.9 billion tokens, US$ 10,206 at list price. New input is 0.03% of the money and is not drawn.</text></svg>
<figcaption>Ninety-six percent of the volume is cheap re-reads. Half the money is there; the other half is in the 4% that gets written, and the answers.</figcaption>
</figure>

Ninety-six percent of every token we sent was a re-read from cache. That is the
mass a compression tool sees, and the mass it compresses. It carries half the
money.

The other half sits in two places a token count barely registers. Cache
*writes* are 4% of the tokens and 42% of the money. The model's own answers are
0.3% of the tokens and 8% of the money.

This is the first death. A tool that trims the big bar can only ever touch
half the bill, and it has to trim a lot of cheap tokens to move it.

## Four days, same tokens, three prices

The second death is simpler to see. Take four ordinary working days from one
project, on the same model, chosen because each round of work sent almost
exactly the same amount of text to the model. If tokens were the price, the
four days would cost the same.

<!-- FIG:DAYS -->
<figure class="diagram">
<svg viewBox="0 0 720 330" role="img" aria-label="Four working days with almost the same tokens per round, 576 to 627 thousand, and a cost per round that goes from 34 cents to 1 dollar and 2 cents. The only thing that grew with the cost is how much text was written to cache." xmlns="http://www.w3.org/2000/svg" font-family="IBM Plex Sans, system-ui, sans-serif" color="#16233a"><text x="150" y="22" font-size="12" font-weight="700" fill="#16233a">tokens sent per round</text><text x="470" y="22" font-size="12" font-weight="700" fill="#16233a">cost per round</text><text x="16" y="66" font-size="13.5" font-weight="700" fill="#16233a">day 1</text><rect x="150" y="46" width="237" height="30" rx="4" fill="#6b8ef2"/><text x="395" y="66" font-size="13" fill="#16233a">593k</text><rect x="470" y="46" width="53" height="30" rx="4" fill="#a4252c"/><text x="531" y="66" font-size="14" font-weight="700" fill="#a4252c">US$ 0.34</text><text x="150" y="92" font-size="11" fill="#16233a" fill-opacity="0.75">of which written to cache: 3k</text><line x1="16" y1="102" x2="704" y2="102" stroke="#d5dde8"/><text x="16" y="132" font-size="13.5" font-weight="700" fill="#16233a">day 2</text><rect x="150" y="112" width="230" height="30" rx="4" fill="#6b8ef2"/><text x="388" y="132" font-size="13" fill="#16233a">576k</text><rect x="470" y="112" width="79" height="30" rx="4" fill="#a4252c"/><text x="557" y="132" font-size="14" font-weight="700" fill="#a4252c">US$ 0.51</text><text x="150" y="158" font-size="11" fill="#16233a" fill-opacity="0.75">of which written to cache: 22k</text><line x1="16" y1="168" x2="704" y2="168" stroke="#d5dde8"/><text x="16" y="198" font-size="13.5" font-weight="700" fill="#16233a">day 3</text><rect x="150" y="178" width="242" height="30" rx="4" fill="#6b8ef2"/><text x="400" y="198" font-size="13" fill="#16233a">605k</text><rect x="470" y="178" width="96" height="30" rx="4" fill="#a4252c"/><text x="574" y="198" font-size="14" font-weight="700" fill="#a4252c">US$ 0.62</text><text x="150" y="224" font-size="11" fill="#16233a" fill-opacity="0.75">of which written to cache: 31k</text><line x1="16" y1="234" x2="704" y2="234" stroke="#d5dde8"/><text x="16" y="264" font-size="13.5" font-weight="700" fill="#16233a">day 4</text><rect x="150" y="244" width="251" height="30" rx="4" fill="#6b8ef2"/><text x="409" y="264" font-size="13" fill="#16233a">627k</text><rect x="470" y="244" width="158" height="30" rx="4" fill="#a4252c"/><text x="636" y="264" font-size="14" font-weight="700" fill="#a4252c">US$ 1.02</text><text x="150" y="290" font-size="11" fill="#16233a" fill-opacity="0.75">of which written to cache: 72k</text><text x="16" y="320" font-size="11" fill="#16233a">Same project, same model, same price list. Tokens within 4% of each other; cost three times apart.</text></svg>
<figcaption>Four days, the same volume of tokens, and a cost per round that triples. The only line that grew with the cost is the one token charts never show: how much was written to cache.</figcaption>
</figure>

Day 1 and day 4 sent the same text and day 4 cost three times as much. The
difference is entirely in one line of the invoice: on day 1, three thousand
tokens per round were written to cache; on day 4, seventy-two thousand.
Everything else, the re-reads and the answers, is nearly identical.

Across all thirty days of this project on this model family, knowing the
tokens a day sent explains about half of what it cost. Knowing how much it
wrote to cache explains nearly all of it.

Nothing here is a verdict on any tool. It is a description of the invoice. The
bill follows the writes. Volume is a bystander.

## What the tool does to those four lines

Now the tool. A proxy sits between the agent and the model and shortens what
the agent sends: it trims a long log, folds a repeated listing, replaces a
verbose search result with a summary that can be expanded on request. It does
this well. On our traffic it removed text exactly as advertised.

The question is what that does to the invoice. Below is one round of work,
line by line, on the same project at the same price list: the grey bar is a
round without the proxy, the blue bar is a round with it.

<!-- FIG:PAIR -->
<figure class="diagram">
<svg viewBox="0 0 720 380" role="img" aria-label="The invoice per round of work, without the proxy and with it. Text re-read from cache at 0.1 times: 543,963 tokens without, 293,047 with, minus 46 percent. Text written to cache at 1.25 to 2 times: 6,273 without, 17,759 with, plus 183 percent. Answer generated at 5 times: 874 without, 1,209 with, plus 38 percent. Cost per round: 17.6 cents without, 20.1 cents with, plus 14 percent." xmlns="http://www.w3.org/2000/svg" font-family="IBM Plex Sans, system-ui, sans-serif" color="#16233a"><text x="16" y="22" font-size="12" font-weight="700" fill="#16233a">invoice line</text><text x="250" y="22" font-size="12" font-weight="700" fill="#16233a">price</text><text x="330" y="22" font-size="12" font-weight="700" fill="#16233a">tokens per round of work</text><rect x="330" y="30" width="11" height="11" fill="#9aa5b5"/><text x="346" y="40" font-size="11" fill="#16233a">without the proxy</text><rect x="470" y="30" width="11" height="11" fill="#6b8ef2"/><text x="486" y="40" font-size="11" fill="#16233a">with the proxy</text><text x="16" y="72" font-size="13.5" fill="#16233a">text re-read from cache</text><text x="250" y="72" font-size="12.5" fill="#16233a" fill-opacity="0.8">0,1×</text><rect x="330" y="58" width="250" height="18" rx="3" fill="#9aa5b5"/><text x="586" y="71" font-size="12" fill="#16233a">543,963</text><rect x="330" y="82" width="135" height="18" rx="3" fill="#6b8ef2"/><text x="471" y="95" font-size="12" fill="#16233a">293,047 <tspan font-weight="700" fill="#1d7a4a">-46%</tspan></text><line x1="16" y1="114" x2="704" y2="114" stroke="#d5dde8"/><text x="16" y="148" font-size="13.5" fill="#16233a">text written to cache</text><text x="250" y="148" font-size="12.5" fill="#16233a" fill-opacity="0.8">1,25× / 2×</text><rect x="330" y="134" width="88" height="18" rx="3" fill="#9aa5b5"/><text x="424" y="147" font-size="12" fill="#16233a">6,273</text><rect x="330" y="158" width="250" height="18" rx="3" fill="#6b8ef2"/><text x="586" y="171" font-size="12" fill="#16233a">17,759 <tspan font-weight="700" fill="#a4252c">+183%</tspan></text><line x1="16" y1="190" x2="704" y2="190" stroke="#d5dde8"/><text x="16" y="224" font-size="13.5" fill="#16233a">answer generated</text><text x="250" y="224" font-size="12.5" fill="#16233a" fill-opacity="0.8">5×</text><rect x="330" y="210" width="181" height="18" rx="3" fill="#9aa5b5"/><text x="517" y="223" font-size="12" fill="#16233a">874</text><rect x="330" y="234" width="250" height="18" rx="3" fill="#6b8ef2"/><text x="586" y="247" font-size="12" fill="#16233a">1,209 <tspan font-weight="700" fill="#a4252c">+38%</tspan></text><line x1="16" y1="266" x2="704" y2="266" stroke="#d5dde8"/><text x="16" y="308" font-size="14" font-weight="700" fill="#16233a">cost per round</text><rect x="330" y="292" width="219" height="18" rx="3" fill="#9aa5b5"/><text x="555" y="305" font-size="13" font-weight="700" fill="#16233a">US$ 0.176</text><rect x="330" y="316" width="250" height="18" rx="3" fill="#a4252c"/><text x="586" y="329" font-size="13" font-weight="700" fill="#a4252c">US$ 0.201 +14%</text><text x="16" y="370" font-size="11" fill="#16233a">Same project, same price list. Without the proxy: 13 days, 3,915 rounds. With it: 2 days, 618 rounds.</text></svg>
<figcaption>One round of work, line by line, without the proxy (grey) and with it (blue). The 0.1× line fell by nearly half. The 2× line nearly tripled. The round cost 14% more.</figcaption>
</figure>

Read it top to bottom.

**First line, re-reads, priced at 0.1×.** This is what the proxy compresses,
and it worked: nearly half the volume gone. That is the chart the product
shows you.

**Second line, writes, priced at up to 2×.** This is the price of compressing.
The provider's cache is a promise that *this exact text* will be seen again.
The moment the proxy changes the text, the provider sees new text, stores it
again, and charges the write premium. Writes nearly tripled.

**Third line, the answer, priced at 5×.** Longer answers. Part of that is the
newer model, not the proxy; it is here because it is on the invoice.

**Last line, the total.** A token saved on the first line is worth one-twentieth
of a token added on the second. The round costs 14% more.

Nothing in this is a defect in anyone's code. A tool whose job is to change
what the model sees is, by construction, a tool that forces re-writes. It
saves on the 0.1× line and spends on the 2× line.

Two days on the proxied side is a short run, and the two sides ran on sibling
models, which is why the chart says "same price list" rather than "same
model". We will keep measuring. But the direction has held on every cut we
have made, and it is the same direction an independent study found in July:
across paid, controlled runs of the same coding agent, the configuration that
cut delivered tokens by 38% **raised the bill by 6.8%**, and the correlation
between tokens cut and money saved was 0.15. Their estimate of the most that
compressing visible text can ever save, given how the cache dominates the
bill: about 5%.

## What the dashboard calls savings

If the bill goes up, why does every user of these tools report savings? Because
the tool's own dashboard is the receipt most people read, and the dashboard
counts differently.

<!-- FIG:DASH -->
<figure class="diagram">
<svg viewBox="0 0 720 250" role="img" aria-label="What the proxy's dashboard reports as savings, and what its own counters say happened." xmlns="http://www.w3.org/2000/svg" font-family="IBM Plex Sans, system-ui, sans-serif" color="#16233a"><text x="16" y="28" font-size="12" font-weight="700" fill="#16233a">Dollars the dashboard calls savings</text><text x="16" y="56" font-size="13" fill="#16233a">from compressing text</text><rect x="300" y="40" width="11" height="24" rx="4" fill="#1d7a4a"/><text x="319" y="57" font-size="14" font-weight="700" fill="#1d7a4a">US$ 14</text><text x="16" y="92" font-size="13" fill="#16233a">the provider's own cache discount</text><rect x="300" y="76" width="400" height="24" rx="4" fill="#8a94a3"/><text x="500" y="93" font-size="14" font-weight="700" text-anchor="middle" fill="#fff">US$ 1,667</text><text x="16" y="138" font-size="12" font-weight="700" fill="#16233a">Tokens, by the proxy's own counters</text><text x="16" y="166" font-size="13" fill="#16233a">removed by compression</text><rect x="300" y="150" width="252" height="24" rx="4" fill="#1d7a4a"/><text x="560" y="167" font-size="14" font-weight="700" fill="#1d7a4a">1.79 M</text><text x="16" y="202" font-size="13" fill="#16233a">lost to cache re-writes it caused</text><rect x="300" y="186" width="400" height="24" rx="4" fill="#a4252c"/><text x="500" y="203" font-size="14" font-weight="700" text-anchor="middle" fill="#fff">2.84 M</text><text x="16" y="240" font-size="11" fill="#16233a">3,200 requests. The proxy's own report ends with: net tokens negative.</text></svg>
<figcaption>Top: the two numbers the dashboard adds up as "saved". Bottom: the tool's own accounting of tokens removed against tokens lost to the re-writes it caused.</figcaption>
</figure>

Our proxy's dashboard, after 3,200 requests, reported US$ 14 saved by
compression and US$ 1,667 saved by caching. The second number is the
provider's own discount: the 0.1× line, which every user gets with or without
a proxy. Presented side by side, the discount is the headline and the
compression is a rounding error, and a reader who does not know the invoice
sees a tool that saved sixteen hundred dollars.

The more honest number is three screens deeper, in the tool's own counters: it
removed 1.79 million tokens by compression and **lost 2.84 million to cache
re-writes it caused**. The counter is labelled *net tokens: negative*. The tool
knows. It just does not lead with it.

We are not the first to notice. A developer who ran the same tool for several
days found US$ 47 of his US$ 57 "saved" was the provider's discount, and that
only 2% of his traffic was ever compressed. His advice was to read the
breakdown instead of the front page. The study above makes the same point in
its title.

## A correction, in the same spirit

Measuring this cost us a lesson we owe the reader. Until this week, every total
in this series was **about twice too high**. The agent's log writes one line
per piece of an answer, and each line repeats the cost of the whole answer; we
were counting lines. We found it while building a screen that lets you open a
bill line by line, where identical answers two seconds apart looked wrong. We
confirmed it against an independent request log and recounted everything.

The totals in episodes 1 and 2 halve. The conclusions survive, because they
were already stated per round and both sides of every comparison were inflated
by the same factor. We say it here because the point of this episode is that
counting tokens is treacherous, and we are not exempt.

## What to ask for instead

For a manager, an executive or a small business owner paying for this, the
practical outcome is a change of question.

**Do not ask how many tokens were saved.** It is the quantity the tools
optimise, and it is the quantity the invoice cares least about.

Ask for three things:

1. **Cost per round of work, by model, per day.** It is the only number that
   survives changes in the amount of work, and the only one on which a
   before-and-after means anything. Ours is on a screen that opens from one
   total down to every request, with the arithmetic shown on each line.
2. **The share of the bill that is cache writes.** It is the line that moved
   our bill, and the line no token chart shows. If it rises, something is
   changing the text between rounds: a tool, a long pause, a prompt that
   embeds the time of day.
3. **Which model answered which kind of task.** Across our days, the choice of
   model moved the bill more than any proxy did, in both directions. It is a
   lever you own and it costs nothing to pull.

The tool from episodes 1 and 2 stays installed for now, on one project, under
a clean test, because two days is not a verdict and we promised to publish the
number whichever way it goes. But the series has changed subject. The token is
the wrong unit, and the rest of these episodes will be written in the right
one.

---

*Method, in brief. Four projects, 44 working days, every model answer read
from the agent's own logs and priced at the provider's published list rates,
including the separate rates for five-minute and one-hour cache writes.
Answers deduplicated by response id. The proxied project is compared only
against itself, per round, on one model family at one price list. Days in
which the proxy ran a configuration later found to be wrong are excluded from
the before-and-after and shown nowhere as evidence. All figures are
list-price equivalents: we pay a flat monthly plan, and this series is the
study we are running before moving to metered use.*

*Sources: S. Weinberger and A. Hozez, "Token Reduction Is Not Cost Reduction:
An Empirical Study of End-to-End Efficiency in API-Based Coding Agents",
arXiv:2607.12161, July 2026. The field report with the US$ 47 of US$ 57 is at
russ.cloud, June 2026.*
