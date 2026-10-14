---
title: "The most expensive model, doing the cheapest work"
date: 2026-10-14T08:00:00-04:00
draft: false
translationKey: "model-effort"
categories: ["Technology"]
tags: ["ai-agents", "cost", "management", "delegation", "software-delivery", "spending-less-on-ai"]
description: "Episode 4 of Spending Less on AI. Five weeks of an AI coding agent, task by task, all on the most expensive model because nobody had chosen otherwise. What four tasks revealed about where the money goes, the lead-and-helpers setup that replaced one model for everything, and what the invoice said after: the average round of work fell from about 40 cents to about 10."
---

*Fourth episode of **Spending Less on AI**. Episodes 1 and 2, {{< episode 1 >}}
and {{< episode 2 >}}, tested a tool that promises a lighter bill. Episode 3,
{{< episode 3 >}}, showed that the number every such tool reports is not the
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

<figure class="diagram"><svg viewBox="0 0 720 336" role="img" aria-label="Bar chart of 36 tasks sorted by number of rounds, from 1 to 2,450, with a gold median line at 242 and four navy bars labelled A, B, C and D." xmlns="http://www.w3.org/2000/svg" font-family="IBM Plex Sans, system-ui, sans-serif" color="#16233a"><defs><marker id="m-ink" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1,1 L9,5 L1,9 z" fill="#16233a"/></marker><marker id="m-navy" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1,1 L9,5 L1,9 z" fill="#1d4e89"/></marker><marker id="m-forbid" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1,1 L9,5 L1,9 z" fill="#b3261e"/></marker><marker id="m-muted" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1,1 L9,5 L1,9 z" fill="#5d6b7d"/></marker><marker id="m-gold" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1,1 L9,5 L1,9 z" fill="#b7791f"/></marker></defs><path d="M 56,296 L 696,296" fill="none" stroke="#b9c5d4" stroke-width="1" stroke-linecap="round" stroke-linejoin="round"/><path d="M 56,296.0 L 696,296.0" fill="none" stroke="#d5dde8" stroke-width="1" stroke-linecap="round" stroke-linejoin="round"/><text x="48" y="300.0" text-anchor="end" font-size="10.5" font-weight="400" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">0</text><path d="M 56,244.0 L 696,244.0" fill="none" stroke="#d5dde8" stroke-width="1" stroke-linecap="round" stroke-linejoin="round"/><text x="48" y="248.0" text-anchor="end" font-size="10.5" font-weight="400" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">500</text><path d="M 56,192.0 L 696,192.0" fill="none" stroke="#d5dde8" stroke-width="1" stroke-linecap="round" stroke-linejoin="round"/><text x="48" y="196.0" text-anchor="end" font-size="10.5" font-weight="400" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">1 000</text><path d="M 56,140.0 L 696,140.0" fill="none" stroke="#d5dde8" stroke-width="1" stroke-linecap="round" stroke-linejoin="round"/><text x="48" y="144.0" text-anchor="end" font-size="10.5" font-weight="400" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">1 500</text><path d="M 56,88.0 L 696,88.0" fill="none" stroke="#d5dde8" stroke-width="1" stroke-linecap="round" stroke-linejoin="round"/><text x="48" y="92.0" text-anchor="end" font-size="10.5" font-weight="400" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">2 000</text><path d="M 56,36.0 L 696,36.0" fill="none" stroke="#d5dde8" stroke-width="1" stroke-linecap="round" stroke-linejoin="round"/><text x="48" y="40.0" text-anchor="end" font-size="10.5" font-weight="400" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">2 500</text><rect x="58.0" y="295.9" width="13.8" height="0.1" fill="#c9d6e6"/><rect x="75.8" y="295.8" width="13.8" height="0.2" fill="#c9d6e6"/><rect x="93.6" y="295.2" width="13.8" height="0.8" fill="#c9d6e6"/><rect x="111.3" y="292.0" width="13.8" height="4.0" fill="#c9d6e6"/><rect x="129.1" y="291.6" width="13.8" height="4.4" fill="#1d4e89"/><text x="136.0" y="283.632" text-anchor="middle" font-size="12.5" font-weight="700" fill="#1d4e89">A</text><rect x="146.9" y="291.1" width="13.8" height="4.9" fill="#c9d6e6"/><rect x="164.7" y="290.2" width="13.8" height="5.8" fill="#c9d6e6"/><rect x="182.4" y="289.6" width="13.8" height="6.4" fill="#c9d6e6"/><rect x="200.2" y="289.3" width="13.8" height="6.7" fill="#c9d6e6"/><rect x="218.0" y="285.9" width="13.8" height="10.1" fill="#c9d6e6"/><rect x="235.8" y="285.9" width="13.8" height="10.1" fill="#c9d6e6"/><rect x="253.6" y="285.8" width="13.8" height="10.2" fill="#c9d6e6"/><rect x="271.3" y="285.7" width="13.8" height="10.3" fill="#c9d6e6"/><rect x="289.1" y="281.8" width="13.8" height="14.2" fill="#c9d6e6"/><rect x="306.9" y="280.0" width="13.8" height="16.0" fill="#c9d6e6"/><rect x="324.7" y="279.7" width="13.8" height="16.3" fill="#c9d6e6"/><rect x="342.4" y="274.3" width="13.8" height="21.7" fill="#c9d6e6"/><rect x="360.2" y="270.8" width="13.8" height="25.2" fill="#c9d6e6"/><rect x="378.0" y="269.0" width="13.8" height="27.0" fill="#c9d6e6"/><rect x="395.8" y="266.6" width="13.8" height="29.4" fill="#c9d6e6"/><rect x="413.6" y="265.9" width="13.8" height="30.1" fill="#c9d6e6"/><rect x="431.3" y="265.6" width="13.8" height="30.4" fill="#c9d6e6"/><rect x="449.1" y="264.5" width="13.8" height="31.5" fill="#c9d6e6"/><rect x="466.9" y="256.1" width="13.8" height="39.9" fill="#c9d6e6"/><rect x="484.7" y="255.4" width="13.8" height="40.6" fill="#c9d6e6"/><rect x="502.4" y="255.3" width="13.8" height="40.7" fill="#c9d6e6"/><rect x="520.2" y="244.4" width="13.8" height="51.6" fill="#c9d6e6"/><rect x="538.0" y="242.0" width="13.8" height="54.0" fill="#c9d6e6"/><rect x="555.8" y="236.6" width="13.8" height="59.4" fill="#c9d6e6"/><rect x="573.6" y="201.3" width="13.8" height="94.7" fill="#1d4e89"/><text x="580.4444444444445" y="193.256" text-anchor="middle" font-size="12.5" font-weight="700" fill="#1d4e89">C</text><rect x="591.3" y="197.6" width="13.8" height="98.4" fill="#c9d6e6"/><rect x="609.1" y="194.9" width="13.8" height="101.1" fill="#c9d6e6"/><rect x="626.9" y="154.9" width="13.8" height="141.1" fill="#c9d6e6"/><rect x="644.7" y="133.0" width="13.8" height="163.0" fill="#c9d6e6"/><rect x="662.4" y="88.3" width="13.8" height="207.7" fill="#1d4e89"/><text x="669.3333333333334" y="80.31200000000001" text-anchor="middle" font-size="12.5" font-weight="700" fill="#1d4e89">B</text><rect x="680.2" y="41.2" width="13.8" height="254.8" fill="#1d4e89"/><text x="687.1111111111112" y="33.19999999999999" text-anchor="middle" font-size="12.5" font-weight="700" fill="#1d4e89">D</text><path d="M 56,270.832 L 696,270.832" fill="none" stroke="#b7791f" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="6 5"/><text x="692" y="264.832" text-anchor="end" font-size="11" font-weight="600" fill="#b7791f">median · 242</text><text x="56" y="320" text-anchor="start" font-size="11.5" font-weight="400" fill="#5d6b7d">36 tasks, five weeks — one bar per task</text><text x="696" y="320" text-anchor="end" font-size="11.5" font-weight="400" fill="#5d6b7d">sorted by size</text><text x="56" y="24" text-anchor="start" font-size="11.5" font-weight="400" fill="#5d6b7d">rounds of work (each one re-sends the whole conversation)</text></svg><figcaption>Thirty-six tasks, one bar each. The smallest cost nine dollars, the largest 945, and between them sits every kind of work a delivery team does in five weeks. The four the article follows are in navy. All thirty-six ran on the same model.</figcaption></figure>

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

<figure class="diagram"><svg viewBox="0 0 720 388" role="img" aria-label="A conversation of 509,000 tokens enters a navy model box and a 1,000-token answer leaves; below, a cost bar split 73% re-reading, 20% caching, 7% answer; a dashed panel lists the two levers." xmlns="http://www.w3.org/2000/svg" font-family="IBM Plex Sans, system-ui, sans-serif" color="#16233a"><defs><marker id="m-ink" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1,1 L9,5 L1,9 z" fill="#16233a"/></marker><marker id="m-navy" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1,1 L9,5 L1,9 z" fill="#1d4e89"/></marker><marker id="m-forbid" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1,1 L9,5 L1,9 z" fill="#b3261e"/></marker><marker id="m-muted" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1,1 L9,5 L1,9 z" fill="#5d6b7d"/></marker><marker id="m-gold" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1,1 L9,5 L1,9 z" fill="#b7791f"/></marker></defs><rect x="16" y="16" width="688" height="150" rx="10" fill="#eef2f7" stroke="#d5dde8" stroke-width="1"/><text x="32" y="40" text-anchor="start" font-size="12.5" font-weight="600" fill="#5d6b7d">one round of work</text><rect x="32" y="56" width="190" height="90" rx="6" fill="#fff" stroke="#b9c5d4" stroke-width="1.2"/><text x="127.0" y="98.0" text-anchor="middle" font-size="13" font-weight="600" fill="#16233a">the conversation</text><text x="127.0" y="115.0" text-anchor="middle" font-size="11" font-weight="400" fill="#5d6b7d">tokens re-sent, average</text><text x="127" y="130" text-anchor="middle" font-size="15" font-weight="700" fill="#1d4e89" font-family="IBM Plex Mono, ui-monospace, monospace">509 000</text><path d="M 224,100 L 262,100" fill="none" stroke="#1d4e89" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" marker-end="url(#m-navy)"/><rect x="264" y="56" width="190" height="90" rx="6" fill="#1d4e89" stroke="#173d6e" stroke-width="1.2"/><text x="359.0" y="98.0" text-anchor="middle" font-size="13" font-weight="600" fill="#fff">the model</text><text x="359.0" y="115.0" text-anchor="middle" font-size="11" font-weight="400" fill="#cfe0f5">reads all of it, again</text><path d="M 456,100 L 494,100" fill="none" stroke="#1d4e89" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" marker-end="url(#m-navy)"/><rect x="496" y="56" width="190" height="90" rx="6" fill="#fff" stroke="#b9c5d4" stroke-width="1.2"/><text x="591.0" y="98.0" text-anchor="middle" font-size="13" font-weight="600" fill="#16233a">the answer</text><text x="591.0" y="115.0" text-anchor="middle" font-size="11" font-weight="400" fill="#5d6b7d">tokens written, average</text><text x="591" y="130" text-anchor="middle" font-size="15" font-weight="700" fill="#1d4e89" font-family="IBM Plex Mono, ui-monospace, monospace">1 000</text><text x="16" y="188" text-anchor="start" font-size="12.5" font-weight="600" fill="#5d6b7d">where the 37 cents go</text><rect x="16.0" y="196" width="502.2" height="34" fill="#1d4e89"/><text x="267.12" y="218" text-anchor="middle" font-size="11.5" font-weight="600" fill="#fff">re-reading what it already saw · 73%</text><rect x="518.2" y="196" width="137.6" height="34" fill="#5b8fd6"/><text x="587.04" y="218" text-anchor="middle" font-size="11.5" font-weight="600" fill="#fff">caching · 20%</text><rect x="655.8" y="196" width="48.2" height="34" fill="#c9d6e6"/><text x="704.0" y="190" text-anchor="end" font-size="11.5" font-weight="600" fill="#5d6b7d">the answer · 7%</text><text x="16" y="254" text-anchor="start" font-size="11.5" font-weight="400" fill="#5d6b7d">Thinking lives inside that 7%. What an agent costs is not what it writes — it is what it re-reads.</text><rect x="16" y="276" width="688" height="96" rx="10" fill="#eef2f7" stroke="#d5dde8" stroke-width="1" stroke-dasharray="6 5"/><text x="32" y="300" text-anchor="start" font-size="12.5" font-weight="600" fill="#1d4e89">which leaves exactly two levers</text><text x="32" y="322" text-anchor="start" font-size="11.5" font-weight="400" fill="#16233a">The model sets the price of every line: at the time, Opus $5, Sonnet $2, Haiku $1 per million tokens read.</text><text x="32" y="340" text-anchor="start" font-size="11.5" font-weight="400" fill="#16233a">The effort level sets how many rounds there are: lower effort, fewer and larger steps, fewer rounds.</text><text x="32" y="358" text-anchor="start" font-size="11.5" font-weight="400" fill="#5d6b7d" font-style="italic">Average round across the five weeks: 509,000 tokens in, 1,000 out, 37 cents.</text></svg><figcaption>One round of work, taken apart. The agent re-sends half a million tokens in order to write a thousand — so three quarters of the bill is re-reading, and the model you choose sets the price of every re-read.</figcaption></figure>

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

<figure class="diagram"><svg viewBox="0 0 720 404" role="img" aria-label="Top lane: a long navy arrow of 1,997 rounds with five red flags marking human corrections. Bottom lane: an Opus box writes a rule, fans out to fourteen Haiku boxes working in parallel, and two results return for review." xmlns="http://www.w3.org/2000/svg" font-family="IBM Plex Sans, system-ui, sans-serif" color="#16233a"><defs><marker id="m-ink" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1,1 L9,5 L1,9 z" fill="#16233a"/></marker><marker id="m-navy" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1,1 L9,5 L1,9 z" fill="#1d4e89"/></marker><marker id="m-forbid" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1,1 L9,5 L1,9 z" fill="#b3261e"/></marker><marker id="m-muted" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1,1 L9,5 L1,9 z" fill="#5d6b7d"/></marker><marker id="m-gold" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1,1 L9,5 L1,9 z" fill="#b7791f"/></marker></defs><rect x="16" y="16" width="688" height="120" rx="10" fill="#eef2f7" stroke="#d5dde8" stroke-width="1"/><text x="32" y="40" text-anchor="start" font-size="12.5" font-weight="600" fill="#5d6b7d">what happened — one model, one conversation</text><path d="M 40,80 L 680,80" fill="none" stroke="#1d4e89" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" marker-end="url(#m-navy)"/><path d="M 180,76 L 180,52 L 196,58 L 180,64" fill="#b3261e" stroke="none"/><path d="M 260,76 L 260,52 L 276,58 L 260,64" fill="#b3261e" stroke="none"/><path d="M 380,76 L 380,52 L 396,58 L 380,64" fill="#b3261e" stroke="none"/><path d="M 470,76 L 470,52 L 486,58 L 470,64" fill="#b3261e" stroke="none"/><path d="M 560,76 L 560,52 L 576,58 L 560,64" fill="#b3261e" stroke="none"/><text x="40" y="106" text-anchor="start" font-size="11.5" font-weight="400" fill="#5d6b7d">five times I had to pull it back on course; two tasks tangled in one thread</text><text x="680" y="106" text-anchor="end" font-size="13" font-weight="700" fill="#1d4e89" font-family="IBM Plex Mono, ui-monospace, monospace">1 997</text><rect x="16" y="156" width="688" height="232" rx="10" fill="#eef2f7" stroke="#d5dde8" stroke-width="1"/><text x="32" y="180" text-anchor="start" font-size="12.5" font-weight="600" fill="#5d6b7d">what the work actually was</text><rect x="24" y="200" width="170" height="60" rx="6" fill="#1d4e89" stroke="#173d6e" stroke-width="1.2"/><text x="109.0" y="227.0" text-anchor="middle" font-size="13" font-weight="600" fill="#fff">Opus</text><text x="109.0" y="244.0" text-anchor="middle" font-size="11" font-weight="400" fill="#cfe0f5">writes the rule, once</text><rect x="222" y="196" width="48" height="26" rx="5" fill="#fff" stroke="#b9c5d4" stroke-width="1.1"/><text x="246" y="213" text-anchor="middle" font-size="10.5" font-weight="400" fill="#16233a" font-family="IBM Plex Mono, ui-monospace, monospace">w1</text><rect x="282" y="196" width="48" height="26" rx="5" fill="#fff" stroke="#b9c5d4" stroke-width="1.1"/><text x="306" y="213" text-anchor="middle" font-size="10.5" font-weight="400" fill="#16233a" font-family="IBM Plex Mono, ui-monospace, monospace">w2</text><rect x="342" y="196" width="48" height="26" rx="5" fill="#fff" stroke="#b9c5d4" stroke-width="1.1"/><text x="366" y="213" text-anchor="middle" font-size="10.5" font-weight="400" fill="#16233a" font-family="IBM Plex Mono, ui-monospace, monospace">w3</text><rect x="402" y="196" width="48" height="26" rx="5" fill="#fff" stroke="#b9c5d4" stroke-width="1.1"/><text x="426" y="213" text-anchor="middle" font-size="10.5" font-weight="400" fill="#16233a" font-family="IBM Plex Mono, ui-monospace, monospace">w4</text><rect x="462" y="196" width="48" height="26" rx="5" fill="#fff" stroke="#b9c5d4" stroke-width="1.1"/><text x="486" y="213" text-anchor="middle" font-size="10.5" font-weight="400" fill="#16233a" font-family="IBM Plex Mono, ui-monospace, monospace">w5</text><rect x="522" y="196" width="48" height="26" rx="5" fill="#fff" stroke="#b9c5d4" stroke-width="1.1"/><text x="546" y="213" text-anchor="middle" font-size="10.5" font-weight="400" fill="#16233a" font-family="IBM Plex Mono, ui-monospace, monospace">w6</text><rect x="582" y="196" width="48" height="26" rx="5" fill="#fff" stroke="#b9c5d4" stroke-width="1.1"/><text x="606" y="213" text-anchor="middle" font-size="10.5" font-weight="400" fill="#16233a" font-family="IBM Plex Mono, ui-monospace, monospace">w7</text><rect x="222" y="232" width="48" height="26" rx="5" fill="#fff" stroke="#b9c5d4" stroke-width="1.1"/><text x="246" y="249" text-anchor="middle" font-size="10.5" font-weight="400" fill="#16233a" font-family="IBM Plex Mono, ui-monospace, monospace">w8</text><rect x="282" y="232" width="48" height="26" rx="5" fill="#fff" stroke="#b9c5d4" stroke-width="1.1"/><text x="306" y="249" text-anchor="middle" font-size="10.5" font-weight="400" fill="#16233a" font-family="IBM Plex Mono, ui-monospace, monospace">w9</text><rect x="342" y="232" width="48" height="26" rx="5" fill="#fff" stroke="#b9c5d4" stroke-width="1.1"/><text x="366" y="249" text-anchor="middle" font-size="10.5" font-weight="400" fill="#16233a" font-family="IBM Plex Mono, ui-monospace, monospace">w10</text><rect x="402" y="232" width="48" height="26" rx="5" fill="#fff" stroke="#b9c5d4" stroke-width="1.1"/><text x="426" y="249" text-anchor="middle" font-size="10.5" font-weight="400" fill="#16233a" font-family="IBM Plex Mono, ui-monospace, monospace">w11</text><rect x="462" y="232" width="48" height="26" rx="5" fill="#fff" stroke="#b9c5d4" stroke-width="1.1"/><text x="486" y="249" text-anchor="middle" font-size="10.5" font-weight="400" fill="#16233a" font-family="IBM Plex Mono, ui-monospace, monospace">w12</text><rect x="522" y="232" width="48" height="26" rx="5" fill="#fff" stroke="#b9c5d4" stroke-width="1.1"/><text x="546" y="249" text-anchor="middle" font-size="10.5" font-weight="400" fill="#16233a" font-family="IBM Plex Mono, ui-monospace, monospace">w13</text><rect x="582" y="232" width="48" height="26" rx="5" fill="#fff" stroke="#b9c5d4" stroke-width="1.1"/><text x="606" y="249" text-anchor="middle" font-size="10.5" font-weight="400" fill="#16233a" font-family="IBM Plex Mono, ui-monospace, monospace">w14</text><path d="M 196,230 L 216,230" fill="none" stroke="#1d4e89" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" marker-end="url(#m-navy)"/><text x="222" y="286" text-anchor="start" font-size="11.5" font-weight="400" fill="#5d6b7d">14 × Haiku · in parallel, one item each</text><text x="222" y="304" text-anchor="start" font-size="11.5" font-weight="400" fill="#5d6b7d">a clean context every time, so nothing can get tangled</text><rect x="24" y="300" width="170" height="60" rx="6" fill="#fff" stroke="#b9c5d4" stroke-width="1.2"/><text x="109.0" y="327.0" text-anchor="middle" font-size="13" font-weight="600" fill="#16233a">Opus</text><text x="109.0" y="344.0" text-anchor="middle" font-size="11" font-weight="400" fill="#5d6b7d">reviews the two real ones</text><path d="M 216,300 L 196,318" fill="none" stroke="#1d4e89" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" marker-end="url(#m-navy)"/><text x="222" y="318" text-anchor="start" font-size="11.5" font-weight="600" fill="#1d4e89">2 come back</text><text x="222" y="336" text-anchor="start" font-size="11.5" font-weight="400" fill="#5d6b7d">the other 12 were the same mistake</text></svg><figcaption>The repeated task, drawn twice. Above, the $660 as it was actually spent, with a flag wherever I had to pull the conversation back on course. Below, the shape the work had all along: write the rule once, apply it fourteen times, judge twice.</figcaption></figure>

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

<figure class="diagram"><svg viewBox="0 0 720 318" role="img" aria-label="A horizontal timeline of the fourth task in five segments coloured by nature of work, with a legend and a closing note below." xmlns="http://www.w3.org/2000/svg" font-family="IBM Plex Sans, system-ui, sans-serif" color="#16233a"><defs><marker id="m-ink" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1,1 L9,5 L1,9 z" fill="#16233a"/></marker><marker id="m-navy" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1,1 L9,5 L1,9 z" fill="#1d4e89"/></marker><marker id="m-forbid" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1,1 L9,5 L1,9 z" fill="#b3261e"/></marker><marker id="m-muted" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1,1 L9,5 L1,9 z" fill="#5d6b7d"/></marker><marker id="m-gold" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1,1 L9,5 L1,9 z" fill="#b7791f"/></marker></defs><text x="16" y="28" text-anchor="start" font-size="12.5" font-weight="600" fill="#5d6b7d">the fourth task · ten days · $945</text><rect x="16.0" y="44" width="110.1" height="54" fill="#c9d6e6" stroke="#fff" stroke-width="2"/><text x="71.03999999999999" y="75.0" text-anchor="middle" font-size="11" font-weight="600" fill="#16233a">read it</text><rect x="126.1" y="44" width="206.4" height="54" fill="#1d4e89" stroke="#fff" stroke-width="2"/><text x="229.28" y="75.0" text-anchor="middle" font-size="11" font-weight="600" fill="#fff">3 of 4 already existed</text><rect x="332.5" y="44" width="165.1" height="54" fill="#5b8fd6" stroke="#fff" stroke-width="2"/><text x="415.04" y="75.0" text-anchor="middle" font-size="11" font-weight="600" fill="#fff">investigate</text><rect x="497.6" y="44" width="123.8" height="54" fill="#c9d6e6" stroke="#fff" stroke-width="2"/><text x="559.52" y="75.0" text-anchor="middle" font-size="11" font-weight="600" fill="#16233a">build the screen</text><rect x="621.4" y="44" width="82.6" height="54" fill="#1d4e89" stroke="#fff" stroke-width="2"/><text x="662.72" y="75.0" text-anchor="middle" font-size="11" font-weight="600" fill="#fff">renegotiate</text><text x="16" y="118" text-anchor="start" font-size="10.5" font-weight="400" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">day 1</text><text x="704" y="118" text-anchor="end" font-size="10.5" font-weight="400" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">day 10</text><rect x="16" y="146" width="18" height="18" rx="3" fill="#c9d6e6"/><text x="42" y="160" text-anchor="start" font-size="11.5" font-weight="400" fill="#16233a">mechanical — Haiku territory</text><rect x="16" y="170" width="18" height="18" rx="3" fill="#5b8fd6"/><text x="42" y="184" text-anchor="start" font-size="11.5" font-weight="400" fill="#16233a">volume — one pattern, many places</text><rect x="16" y="194" width="18" height="18" rx="3" fill="#1d4e89"/><text x="42" y="208" text-anchor="start" font-size="11.5" font-weight="400" fill="#16233a">judgment — the request was wrong</text><rect x="16" y="232" width="688" height="70" rx="10" fill="#eef2f7" stroke="#d5dde8" stroke-width="1" stroke-dasharray="6 5"/><text x="32" y="258" text-anchor="start" font-size="12" font-weight="600" fill="#16233a">Pick one model on day one and you are wrong by day four.</text><text x="32" y="280" text-anchor="start" font-size="11.5" font-weight="400" fill="#5d6b7d">The choice has to be made per task, while the work runs — which means somebody has to be making it.</text></svg><figcaption>The largest task, coloured by the kind of work each stretch demanded. It opens in judgment, turns to volume, goes mechanical, and ends in judgment again. No single choice made at the start survives the middle.</figcaption></figure>

The investigation was the third task all over again. The screen was the
first task, thirty times. The instrumentation was the second task: one
pattern, repeated in five places.

Ten days, three kinds of work already described, one setting for all of it.

## Two questions

<figure class="diagram"><svg viewBox="0 0 720 380" role="img" aria-label="A two-by-two map with doubt vertical and amount of work horizontal; task A bottom-left Sonnet low, B bottom-right Opus then fourteen Haiku, C top-left Opus max, D top-right with a dashed gold arc crossing the map." xmlns="http://www.w3.org/2000/svg" font-family="IBM Plex Sans, system-ui, sans-serif" color="#16233a"><defs><marker id="m-ink" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1,1 L9,5 L1,9 z" fill="#16233a"/></marker><marker id="m-navy" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1,1 L9,5 L1,9 z" fill="#1d4e89"/></marker><marker id="m-forbid" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1,1 L9,5 L1,9 z" fill="#b3261e"/></marker><marker id="m-muted" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1,1 L9,5 L1,9 z" fill="#5d6b7d"/></marker><marker id="m-gold" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1,1 L9,5 L1,9 z" fill="#b7791f"/></marker></defs><rect x="150" y="30" width="520" height="300" fill="#fff" stroke="#b9c5d4" stroke-width="1"/><path d="M 410.0,30 L 410.0,330" fill="none" stroke="#d5dde8" stroke-width="1" stroke-linecap="round" stroke-linejoin="round"/><path d="M 150,180.0 L 670,180.0" fill="none" stroke="#d5dde8" stroke-width="1" stroke-linecap="round" stroke-linejoin="round"/><text x="410.0" y="358" text-anchor="middle" font-size="12" font-weight="600" fill="#5d6b7d">how much work</text><text x="156" y="344" text-anchor="start" font-size="10.5" font-weight="400" fill="#5d6b7d">one place</text><text x="664" y="344" text-anchor="end" font-size="10.5" font-weight="400" fill="#5d6b7d">many places, one pattern</text><text transform="translate(122,180.0) rotate(-90)" text-anchor="middle" font-size="12" font-weight="600" fill="#5d6b7d">how much doubt</text><text x="142" y="326" text-anchor="end" font-size="10.5" font-weight="400" fill="#5d6b7d">the request is right</text><text x="142" y="42" text-anchor="end" font-size="10.5" font-weight="400" fill="#5d6b7d">the request may be wrong</text><text x="162" y="52" text-anchor="start" font-size="11" font-weight="600" fill="#5d6b7d">find the truth</text><text x="422.0" y="52" text-anchor="start" font-size="11" font-weight="600" fill="#5d6b7d">find it, then repeat it</text><text x="162" y="202.0" text-anchor="start" font-size="11" font-weight="600" fill="#5d6b7d">just do it</text><text x="422.0" y="202.0" text-anchor="start" font-size="11" font-weight="600" fill="#5d6b7d">do it many times</text><circle cx="240" cy="270" r="15" fill="#1d4e89" stroke="#173d6e" stroke-width="1.5"/><text x="240" y="275" text-anchor="middle" font-size="13" font-weight="700" fill="#fff">A</text><rect x="234" y="292" width="99" height="22" rx="11" fill="#eef2f7" stroke="#d5dde8" stroke-width="1"/><text x="283.5" y="307" text-anchor="middle" font-size="11" font-weight="400" fill="#16233a" font-family="IBM Plex Mono, ui-monospace, monospace">Sonnet · low</text><circle cx="560" cy="250" r="15" fill="#1d4e89" stroke="#173d6e" stroke-width="1.5"/><text x="560" y="255" text-anchor="middle" font-size="13" font-weight="700" fill="#fff">B</text><rect x="405" y="272" width="161" height="22" rx="11" fill="#eef2f7" stroke="#d5dde8" stroke-width="1"/><text x="485.5" y="287" text-anchor="middle" font-size="11" font-weight="400" fill="#16233a" font-family="IBM Plex Mono, ui-monospace, monospace">Opus, then 14 × Haiku</text><circle cx="260" cy="100" r="15" fill="#1d4e89" stroke="#173d6e" stroke-width="1.5"/><text x="260" y="105" text-anchor="middle" font-size="13" font-weight="700" fill="#fff">C</text><rect x="254" y="122" width="86" height="22" rx="11" fill="#eef2f7" stroke="#d5dde8" stroke-width="1"/><text x="297.0" y="137" text-anchor="middle" font-size="11" font-weight="400" fill="#16233a" font-family="IBM Plex Mono, ui-monospace, monospace">Opus · max</text><circle cx="550" cy="90" r="15" fill="#1d4e89" stroke="#173d6e" stroke-width="1.5"/><text x="550" y="95" text-anchor="middle" font-size="13" font-weight="700" fill="#fff">D</text><rect x="402" y="112" width="154" height="22" rx="11" fill="#eef2f7" stroke="#d5dde8" stroke-width="1"/><text x="479.0" y="127" text-anchor="middle" font-size="11" font-weight="400" fill="#16233a" font-family="IBM Plex Mono, ui-monospace, monospace">moves while you work</text><path d="M 250,260 C 350,290 450,70 540,92" fill="none" stroke="#b7791f" stroke-width="1.6" stroke-dasharray="6 5" marker-end="url(#m-gold)"/><text x="390.0" y="122.0" text-anchor="middle" font-size="11" font-weight="600" fill="#b7791f">the fourth crosses the map</text></svg><figcaption>Two questions, four answers. Doubt buys the model; volume buys the effort level and, past a point, more hands. Three of the four tasks sit still in one square. The fourth does not — and that is the whole argument for a lead.</figcaption></figure>

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

<figure class="diagram"><svg viewBox="0 0 720 370" role="img" aria-label="A navy lead box connects to five helper boxes labelled reader, builder, tester, reviewer and QA lead, each showing configuration lines for model, effort and turn limit." xmlns="http://www.w3.org/2000/svg" font-family="IBM Plex Sans, system-ui, sans-serif" color="#16233a"><defs><marker id="m-ink" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1,1 L9,5 L1,9 z" fill="#16233a"/></marker><marker id="m-navy" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1,1 L9,5 L1,9 z" fill="#1d4e89"/></marker><marker id="m-forbid" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1,1 L9,5 L1,9 z" fill="#b3261e"/></marker><marker id="m-muted" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1,1 L9,5 L1,9 z" fill="#5d6b7d"/></marker><marker id="m-gold" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1,1 L9,5 L1,9 z" fill="#b7791f"/></marker></defs><rect x="260" y="14" width="200" height="62" rx="6" fill="#1d4e89" stroke="#173d6e" stroke-width="1.2"/><text x="360.0" y="42.0" text-anchor="middle" font-size="13" font-weight="600" fill="#fff">the lead</text><text x="360.0" y="59.0" text-anchor="middle" font-size="11" font-weight="400" fill="#cfe0f5">Opus · the session itself</text><text x="360" y="92" text-anchor="middle" font-size="11" font-weight="400" fill="#5d6b7d">reads the request, splits the work, holds the scope, judges what comes back</text><path d="M 360,76 L 360,104" fill="none" stroke="#1d4e89" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round"/><path d="M 80,104 L 640,104" fill="none" stroke="#1d4e89" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round"/><path d="M 80,104 L 80,118" fill="none" stroke="#1d4e89" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round" marker-end="url(#m-navy)"/><rect x="16" y="122" width="128" height="124" rx="6" fill="#fff" stroke="#b9c5d4" stroke-width="1.2"/><text x="80" y="144" text-anchor="middle" font-size="12.5" font-weight="600" fill="#16233a">reader</text><text x="26" y="168" text-anchor="start" font-size="10.5" font-weight="400" fill="#1d4e89" font-family="IBM Plex Mono, ui-monospace, monospace">model: sonnet</text><text x="26" y="185" text-anchor="start" font-size="10.5" font-weight="400" fill="#1d4e89" font-family="IBM Plex Mono, ui-monospace, monospace">effort: low</text><text x="26" y="202" text-anchor="start" font-size="10.5" font-weight="400" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">maxTurns: 25</text><text x="26" y="219" text-anchor="start" font-size="10" font-weight="400" fill="#5d6b7d" font-style="italic">reads, never writes</text><path d="M 220,104 L 220,118" fill="none" stroke="#1d4e89" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round" marker-end="url(#m-navy)"/><rect x="156" y="122" width="128" height="124" rx="6" fill="#fff" stroke="#b9c5d4" stroke-width="1.2"/><text x="220" y="144" text-anchor="middle" font-size="12.5" font-weight="600" fill="#16233a">builder</text><text x="166" y="168" text-anchor="start" font-size="10.5" font-weight="400" fill="#1d4e89" font-family="IBM Plex Mono, ui-monospace, monospace">model: sonnet</text><text x="166" y="185" text-anchor="start" font-size="10.5" font-weight="400" fill="#1d4e89" font-family="IBM Plex Mono, ui-monospace, monospace">effort: medium</text><text x="166" y="202" text-anchor="start" font-size="10.5" font-weight="400" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">maxTurns: 80</text><text x="166" y="219" text-anchor="start" font-size="10" font-weight="400" fill="#5d6b7d" font-style="italic">one settled change</text><path d="M 360,104 L 360,118" fill="none" stroke="#1d4e89" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round" marker-end="url(#m-navy)"/><rect x="296" y="122" width="128" height="124" rx="6" fill="#fff" stroke="#b9c5d4" stroke-width="1.2"/><text x="360" y="144" text-anchor="middle" font-size="12.5" font-weight="600" fill="#16233a">tester</text><text x="306" y="168" text-anchor="start" font-size="10.5" font-weight="400" fill="#1d4e89" font-family="IBM Plex Mono, ui-monospace, monospace">model: sonnet</text><text x="306" y="185" text-anchor="start" font-size="10.5" font-weight="400" fill="#1d4e89" font-family="IBM Plex Mono, ui-monospace, monospace">effort: high</text><text x="306" y="202" text-anchor="start" font-size="10.5" font-weight="400" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">maxTurns: 120</text><text x="306" y="219" text-anchor="start" font-size="10" font-weight="400" fill="#5d6b7d" font-style="italic">level set at hand-off</text><path d="M 500,104 L 500,118" fill="none" stroke="#1d4e89" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round" marker-end="url(#m-navy)"/><rect x="436" y="122" width="128" height="124" rx="6" fill="#fff" stroke="#b9c5d4" stroke-width="1.2"/><text x="500" y="144" text-anchor="middle" font-size="12.5" font-weight="600" fill="#16233a">reviewer</text><text x="446" y="168" text-anchor="start" font-size="10.5" font-weight="400" fill="#1d4e89" font-family="IBM Plex Mono, ui-monospace, monospace">model: inherit</text><text x="446" y="185" text-anchor="start" font-size="10.5" font-weight="400" fill="#1d4e89" font-family="IBM Plex Mono, ui-monospace, monospace">effort: high</text><text x="446" y="202" text-anchor="start" font-size="10.5" font-weight="400" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">maxTurns: 40</text><text x="446" y="219" text-anchor="start" font-size="10" font-weight="400" fill="#5d6b7d" font-style="italic">the lead's own level</text><path d="M 640,104 L 640,118" fill="none" stroke="#1d4e89" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round" marker-end="url(#m-navy)"/><rect x="576" y="122" width="128" height="124" rx="6" fill="#fff" stroke="#b9c5d4" stroke-width="1.2"/><text x="640" y="144" text-anchor="middle" font-size="12.5" font-weight="600" fill="#16233a">QA lead</text><text x="586" y="168" text-anchor="start" font-size="10.5" font-weight="400" fill="#1d4e89" font-family="IBM Plex Mono, ui-monospace, monospace">model: inherit</text><text x="586" y="185" text-anchor="start" font-size="10.5" font-weight="400" fill="#1d4e89" font-family="IBM Plex Mono, ui-monospace, monospace">effort: high</text><text x="586" y="202" text-anchor="start" font-size="10.5" font-weight="400" fill="#5d6b7d" font-family="IBM Plex Mono, ui-monospace, monospace">maxTurns: 160</text><text x="586" y="219" text-anchor="start" font-size="10" font-weight="400" fill="#5d6b7d" font-style="italic">dispatches the testers</text><rect x="16" y="262" width="688" height="92" rx="10" fill="#eef2f7" stroke="#d5dde8" stroke-width="1" stroke-dasharray="6 5"/><text x="32" y="286" text-anchor="start" font-size="12.5" font-weight="600" fill="#1d4e89">and the lead can override the model on any single hand-off</text><text x="32" y="308" text-anchor="start" font-size="11.5" font-weight="400" fill="#16233a" font-style="italic">“This batch is trivial — run it on Sonnet.”</text><text x="32" y="328" text-anchor="start" font-size="11.5" font-weight="400" fill="#16233a">The file sets the default. The hand-off sets the exception. The lead holds both.</text><text x="32" y="346" text-anchor="start" font-size="11.5" font-weight="400" fill="#5d6b7d" font-style="italic">These are the real settings of the five helper files, not a metaphor.</text></svg><figcaption>What replaced one model for everything, as it was actually configured: a lead that decides and never executes, three helpers on the cheaper model that read, build and test, and two adversaries — the reviewer and the QA lead — that deliberately run at the lead's own level.</figcaption></figure>

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

<figure class="diagram"><svg viewBox="0 0 720 374" role="img" aria-label="Horizontal bar chart of US dollars per round: one bar before at 0.52, then eight bars after, from the lead at 0.24 down to the builder on Haiku at 0.01; the tester while inheriting the lead's model is highlighted in red at 0.13." xmlns="http://www.w3.org/2000/svg" font-family="IBM Plex Sans, system-ui, sans-serif" color="#16233a"><defs><marker id="m-ink" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1,1 L9,5 L1,9 z" fill="#16233a"/></marker><marker id="m-navy" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1,1 L9,5 L1,9 z" fill="#1d4e89"/></marker><marker id="m-forbid" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1,1 L9,5 L1,9 z" fill="#b3261e"/></marker><marker id="m-muted" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1,1 L9,5 L1,9 z" fill="#5d6b7d"/></marker><marker id="m-gold" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1,1 L9,5 L1,9 z" fill="#b7791f"/></marker></defs><text x="16" y="28" text-anchor="start" font-size="12.5" font-weight="600" fill="#5d6b7d">what one round cost, before and after</text><text x="704" y="28" text-anchor="end" font-size="11" font-weight="400" fill="#5d6b7d">US$ per round · list price</text><text x="16" y="59" text-anchor="start" font-size="11.5" font-weight="600" fill="#16233a">before · the session alone, on Opus</text><rect x="252" y="44" width="416.0" height="22" fill="#1d4e89"/><text x="676.0" y="59" text-anchor="start" font-size="12" font-weight="700" fill="#1d4e89" font-family="IBM Plex Mono, ui-monospace, monospace">0.52</text><path d="M16,84 L704,84" stroke="#b9c5d4" stroke-width="1" stroke-dasharray="3 3"/><text x="16" y="109" text-anchor="start" font-size="11.5" font-weight="600" fill="#16233a">after · by role</text><text x="242" y="109" text-anchor="end" font-size="11" font-weight="400" fill="#16233a">the lead</text><rect x="252" y="94" width="192.0" height="20" fill="#5b8fd6"/><text x="452.0" y="108" text-anchor="start" font-size="11.5" font-weight="600" fill="#16233a" font-family="IBM Plex Mono, ui-monospace, monospace">0.24</text><text x="242" y="135" text-anchor="end" font-size="11" font-weight="400" fill="#16233a">QA lead · lead's level</text><rect x="252" y="120" width="120.0" height="20" fill="#5b8fd6"/><text x="380.0" y="134" text-anchor="start" font-size="11.5" font-weight="600" fill="#16233a" font-family="IBM Plex Mono, ui-monospace, monospace">0.15</text><text x="242" y="161" text-anchor="end" font-size="11" font-weight="400" fill="#c44536" font-style="italic">tester, while it inherited the lead's model</text><rect x="252" y="146" width="104.0" height="20" fill="#c44536"/><text x="364.0" y="160" text-anchor="start" font-size="11.5" font-weight="600" fill="#16233a" font-family="IBM Plex Mono, ui-monospace, monospace">0.13</text><text x="242" y="187" text-anchor="end" font-size="11" font-weight="400" fill="#16233a">reviewer · lead's level</text><rect x="252" y="172" width="48.0" height="20" fill="#5b8fd6"/><text x="308.0" y="186" text-anchor="start" font-size="11.5" font-weight="600" fill="#16233a" font-family="IBM Plex Mono, ui-monospace, monospace">0.06</text><text x="242" y="213" text-anchor="end" font-size="11" font-weight="400" fill="#16233a">tester · Sonnet</text><rect x="252" y="198" width="37.6" height="20" fill="#9fc0e8"/><text x="297.6" y="212" text-anchor="start" font-size="11.5" font-weight="600" fill="#16233a" font-family="IBM Plex Mono, ui-monospace, monospace">0.047</text><text x="242" y="239" text-anchor="end" font-size="11" font-weight="400" fill="#16233a">builder · Sonnet</text><rect x="252" y="224" width="32.0" height="20" fill="#9fc0e8"/><text x="292.0" y="238" text-anchor="start" font-size="11.5" font-weight="600" fill="#16233a" font-family="IBM Plex Mono, ui-monospace, monospace">0.04</text><text x="242" y="265" text-anchor="end" font-size="11" font-weight="400" fill="#16233a">reader · Sonnet</text><rect x="252" y="250" width="28.0" height="20" fill="#9fc0e8"/><text x="288.0" y="264" text-anchor="start" font-size="11.5" font-weight="600" fill="#16233a" font-family="IBM Plex Mono, ui-monospace, monospace">0.035</text><text x="242" y="291" text-anchor="end" font-size="11" font-weight="400" fill="#16233a">builder · Haiku, by hand-off</text><rect x="252" y="276" width="8.0" height="20" fill="#9fc0e8"/><text x="268.0" y="290" text-anchor="start" font-size="11.5" font-weight="600" fill="#16233a" font-family="IBM Plex Mono, ui-monospace, monospace">0.01</text><rect x="16" y="310" width="688" height="48" rx="10" fill="#eef2f7" stroke="#d5dde8" stroke-width="1" stroke-dasharray="6 5"/><text x="32" y="330" text-anchor="start" font-size="11.5" font-weight="600" fill="#1d4e89">rounds on the most expensive model: nine in ten before, about one in three after</text><text x="32" y="348" text-anchor="start" font-size="11" font-weight="400" fill="#5d6b7d" font-style="italic">the weekly average round fell from about 40 cents to about 10</text></svg><figcaption>The invoice, per round, before and after the lead and the helpers went in. Before, every round was the session itself on the expensive model. After, the lead's rounds cost half as much and the rounds that moved to the helpers cost a tenth. The red bar is the tester during the weeks it silently inherited the lead's model.</figcaption></figure>

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
