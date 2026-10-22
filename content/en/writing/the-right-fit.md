---
title: "The Right Fit"
seoTitle: "Choosing an AI model and effort for each software task"
date: 2026-10-22T08:00:00-04:00
draft: false
translationKey: "right-fit"
categories: ["Technology"]
tags: ["ai-agents", "cost", "management", "software-delivery", "claude-code", "spending-less-on-ai"]
description: "Episode 5 of Spending Less on AI. Which model, at what effort, for which kind of software request — endpoints, bugs, refactoring, tests, code review, architecture — and how a lead with subagents makes that choice for you, so that efficiency stops depending on someone remembering to choose."
---

*Fifth episode of **Spending Less on AI**. Episodes 1 to 3 ({{< episode 1 >}},
{{< episode 2 >}}, {{< episode 3 >}}) tried a tool that sent fewer tokens and
made the bill heavier; episode 4, {{< episode 4 >}}, managed models instead and
measured the saving. This one is about how to choose.*

---

Episode 4 closed with a spreadsheet still open on my screen, and it stayed
open for a reason I only understood a few days later. Measuring had told us,
to the cent, how much we had overspent by letting the most expensive model do
everything; what it could not tell us was how to choose correctly the next
time a request came in, and the time after that, without opening the
spreadsheet again. An invoice is a verdict on the past, while what an IT
manager needs on Monday morning is a rule for the future.

So this episode is different from the four before it, and I would rather say
so at the start than let it borrow their authority: it is a guide, not a
measurement. The facts about the models come from Anthropic's own documentation, the few numbers about
our work are the ones episode 4 already published, and the rest is the
judgment we built while paying for our mistakes. Treat it as a starting point
to check against your own work, as the documentation itself recommends.

## Price times quantity

Every bill is price times quantity, and the AI bill is no exception, even
though people usually picture choosing a model as a single decision, from cheap
and weak to expensive and strong, pushed as far as the budget allows; there are
two factors, and most of the efficiency lives in how they multiply.

The first factor is the **model**, which sets the price, the rate every unit
of work is charged at, and with it how capable the worker is. Claude
comes in four sizes that matter for software work: Haiku, the smallest and
fastest; Sonnet, the everyday workhorse; Opus, the senior one; and Fable, the
most capable model Anthropic sells widely. Their list prices are further apart
than most people expect, because for the same amount of text read or written Opus
charges forty times what Haiku charges, and Fable charges two and a half times
what Opus charges, which means that the distance between the cheapest and the
most expensive worker on the same team is a factor of a hundred.

The second factor is **effort**, which sets the quantity: how long the worker
thinks before it acts and how many steps it allows itself along the way. It has five levels,
low, medium, high, xhigh and max, and it applies to everything the model
produces: its reasoning, the actions it takes on your systems, and the
explanation it writes at the end. At low effort the model goes straight to the
point; at the top it explores, double-checks and explains. Effort is a signal rather than a budget, the
documentation insists: even at low effort a model still thinks when a problem
is genuinely hard, only less.

Multiply the two and a counter-intuitive possibility appears. Because
Haiku is forty times cheaper per word than Opus, Haiku allowed to think for a
long time can still cost a fraction of Opus thinking briefly, and on a job that
is within its reach it will deliver the same result. The cheap model given
room to think is very often the efficient choice. There is one catch worth knowing, and it shapes everything in the second half
of this article: Haiku keeps that price only while the conversation it is
handed stays short, under roughly a hundred thousand tokens, the units the
provider counts text in, or about a three-hundred-page book; beyond that its price rises fivefold, and it is only eight times
cheaper than Opus. Haiku is the right worker for a small, well-defined job
handed over whole, and the wrong worker for a long session that keeps growing.

## Price the finished job, not the request

One idea changes how the matrix of six requests that follows should be read. The natural way to compare models is by what a single request costs, and it is
almost always the wrong comparison, because a cheap attempt that has to be
redone is not cheap, and a dear one that gets it right the first time is often
the bargain. What matters is the cost of a finished job, every attempt and
every hour of attention included.

That is why efficiency goes missing on both sides of the right fit. Above it,
you are **overpaying**, which means buying judgment the job did not need and
getting nothing back for it except a larger bill. Below it, you are
**underpowered**, which looks like saving until the rework arrives, and rework
is the most expensive line on any bill because it pays for both attempts and
for whoever had to notice. Anthropic's own coding
tests show a sensible middle path when there is a reliable way to tell success
from failure, such as automated tests: run everything at low effort and redo
only the failures at a higher one, which in their runs kept the quality of
running everything high, for a little over half the cost.

## Six requests

What follows are six typical requests a software team hands an AI agent
every week. They are composite examples, not reports of things that
happened to us, and each one is told as the request arriving and the choice it
deserves.

The first is an **endpoint**: a new address in the system that returns, say,
a customer's open orders, with one simple business rule about which orders
count as open. The rule is written down, the pattern exists in a dozen
neighbouring endpoints, and the work is mostly faithful repetition, so the
right fit is Haiku at high effort, which the documentation recommends for
strict instruction following. Opus at xhigh would be overpaying, the same
endpoint at many times the price, while Haiku at low effort on a vague rule would be underpowered, because a small
model hurrying through an ambiguous rule tends to guess. The moment the rule
is unclear, the right move is to step up, not to hope.

The second is a **bug**: a report that a total on an invoice is sometimes
wrong. A bug that can be reproduced is detective work with a confession
already on the table, and Sonnet at high effort is the right fit, with enough
judgment to follow the trail through several parts of the system. A bug that
cannot be reproduced, the kind that appears on Tuesdays under load, is where
you step up. Fable at max effort on a typo is
pure overpaying, and Haiku on an intermittent bug is underpowered in the most
expensive way, because it will find *something*, fix it with confidence, and
leave the real cause in place.

The third is a **refactoring**, reorganising code without changing what it
does. When it is mechanical, such as renaming a concept across the system or
splitting a file that grew too large, Sonnet at medium effort carries it
comfortably, and putting Opus on a rename buys nothing. The step up comes
when the structure itself changes, when the question stops being *what do we
call this* and becomes *where should this live*. The underpowered version
here is the most dangerous of the six: a cheap model sweeping across many
files with no tests to catch it, producing a change that looks tidy and
breaks quietly.

The fourth is **tests**, and writing tests against a clear specification is
careful, thorough work rather than inspired work, and Sonnet at high effort is
the right fit, with the effort spent on covering the cases rather than on
seniority. When the rules are critical, such as money, compliance or personal
data, you step up. Fable on routine tests is overpaying, while the
underpowered case is not about model size at all: it is a test written by the
same worker that wrote the code, which tends to test what it built rather
than what was asked, and so shares every blind spot the code has.

The fifth is **code review**, and here the matrix turns around. A reviewer
weaker than the author can only review spelling, as the configuration of our
own team puts it, so the right fit is the author's model or a stronger one, at
high effort; review is one of the places where the expensive model is the
efficient one, because a defect it catches costs nothing compared to the same
defect found in production, and you step up again when the change touches
security, money or data. Fable at max on a one-line change is still overpaying,
but the costly mistake is the cheap reviewer that approves what it did not
understand and gives everyone a false sense of safety.

The sixth is **architecture**: a decision about how the system will be built,
which database, which boundary between services, which way the data flows.
Opus at xhigh is the right fit, and when the decision will be expensive to
undo, so that a mistake would only surface months later, it is worth moving
to Fable at max, because no amount of saving on the decision repays a wrong
foundation. Fable at max on a choice that can be reversed next week is
overpaying, and Sonnet or Haiku deciding the architecture is underpowered in
a way the bill will not show for a long time, which makes it the worst kind.

<!-- fig:matrix -->
<figure class="diagram"><svg class="wide" viewBox="0 0 720 494" role="img" aria-label="Matrix of six software requests — endpoint, bug, refactoring, tests, code review, architecture — each with its right model and effort, when to step up, what overpaying looks like and what being underpowered looks like." xmlns="http://www.w3.org/2000/svg" font-family="IBM Plex Sans, system-ui, sans-serif" color="#16233a"><defs><marker id="h-ink" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1,1 L9,5 L1,9 z" fill="#16233a"/></marker><marker id="h-navy" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1,1 L9,5 L1,9 z" fill="#1d4e89"/></marker><marker id="h-muted" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1,1 L9,5 L1,9 z" fill="#5d6b7d"/></marker><marker id="h-gold" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1,1 L9,5 L1,9 z" fill="#b7791f"/></marker></defs><rect x="8" y="8" width="344" height="150" rx="8" fill="#fff" stroke="#b9c5d4" stroke-width="1.2"/><rect x="8" y="8" width="344" height="34" rx="8" fill="#eef2f7"/><rect x="8" y="34" width="344" height="8" fill="#eef2f7"/><text x="22" y="31" text-anchor="start" font-size="15" font-weight="600" fill="#16233a">Endpoint</text><rect x="22" y="55" width="4" height="14" rx="2" fill="#1d4e89"/><text x="32" y="66" text-anchor="start" font-size="11" font-weight="600" fill="#5d6b7d">Right fit</text><text x="136" y="66" text-anchor="start" font-size="13" font-weight="600" fill="#16233a">Haiku · high</text><rect x="22" y="81" width="4" height="14" rx="2" fill="#5d6b7d"/><text x="32" y="92" text-anchor="start" font-size="11" font-weight="600" fill="#5d6b7d">Step up when</text><text x="136" y="92" text-anchor="start" font-size="13" font-weight="400" fill="#5d6b7d">the rule is ambiguous</text><rect x="22" y="107" width="4" height="14" rx="2" fill="#b7791f"/><text x="32" y="118" text-anchor="start" font-size="11" font-weight="600" fill="#5d6b7d">Overpaying</text><text x="136" y="118" text-anchor="start" font-size="13" font-weight="400" fill="#b7791f">Opus · xhigh</text><rect x="22" y="133" width="4" height="14" rx="2" fill="#b3261e"/><text x="32" y="144" text-anchor="start" font-size="11" font-weight="600" fill="#5d6b7d">Underpowered</text><text x="136" y="144" text-anchor="start" font-size="13" font-weight="400" fill="#b3261e">Haiku · low, vague rule</text><rect x="368" y="8" width="344" height="150" rx="8" fill="#fff" stroke="#b9c5d4" stroke-width="1.2"/><rect x="368" y="8" width="344" height="34" rx="8" fill="#eef2f7"/><rect x="368" y="34" width="344" height="8" fill="#eef2f7"/><text x="382" y="31" text-anchor="start" font-size="15" font-weight="600" fill="#16233a">Bug</text><rect x="382" y="55" width="4" height="14" rx="2" fill="#1d4e89"/><text x="392" y="66" text-anchor="start" font-size="11" font-weight="600" fill="#5d6b7d">Right fit</text><text x="496" y="66" text-anchor="start" font-size="13" font-weight="600" fill="#16233a">Sonnet · high</text><rect x="382" y="81" width="4" height="14" rx="2" fill="#5d6b7d"/><text x="392" y="92" text-anchor="start" font-size="11" font-weight="600" fill="#5d6b7d">Step up when</text><text x="496" y="92" text-anchor="start" font-size="13" font-weight="400" fill="#5d6b7d">it can't be reproduced</text><rect x="382" y="107" width="4" height="14" rx="2" fill="#b7791f"/><text x="392" y="118" text-anchor="start" font-size="11" font-weight="600" fill="#5d6b7d">Overpaying</text><text x="496" y="118" text-anchor="start" font-size="13" font-weight="400" fill="#b7791f">Fable · max on a typo</text><rect x="382" y="133" width="4" height="14" rx="2" fill="#b3261e"/><text x="392" y="144" text-anchor="start" font-size="11" font-weight="600" fill="#5d6b7d">Underpowered</text><text x="496" y="144" text-anchor="start" font-size="13" font-weight="400" fill="#b3261e">Haiku, intermittent bug</text><rect x="8" y="172" width="344" height="150" rx="8" fill="#fff" stroke="#b9c5d4" stroke-width="1.2"/><rect x="8" y="172" width="344" height="34" rx="8" fill="#eef2f7"/><rect x="8" y="198" width="344" height="8" fill="#eef2f7"/><text x="22" y="195" text-anchor="start" font-size="15" font-weight="600" fill="#16233a">Refactoring</text><rect x="22" y="219" width="4" height="14" rx="2" fill="#1d4e89"/><text x="32" y="230" text-anchor="start" font-size="11" font-weight="600" fill="#5d6b7d">Right fit</text><text x="136" y="230" text-anchor="start" font-size="13" font-weight="600" fill="#16233a">Sonnet · medium</text><rect x="22" y="245" width="4" height="14" rx="2" fill="#5d6b7d"/><text x="32" y="256" text-anchor="start" font-size="11" font-weight="600" fill="#5d6b7d">Step up when</text><text x="136" y="256" text-anchor="start" font-size="13" font-weight="400" fill="#5d6b7d">the structure changes</text><rect x="22" y="271" width="4" height="14" rx="2" fill="#b7791f"/><text x="32" y="282" text-anchor="start" font-size="11" font-weight="600" fill="#5d6b7d">Overpaying</text><text x="136" y="282" text-anchor="start" font-size="13" font-weight="400" fill="#b7791f">Opus on a rename</text><rect x="22" y="297" width="4" height="14" rx="2" fill="#b3261e"/><text x="32" y="308" text-anchor="start" font-size="11" font-weight="600" fill="#5d6b7d">Underpowered</text><text x="136" y="308" text-anchor="start" font-size="13" font-weight="400" fill="#b3261e">many files, no tests</text><rect x="368" y="172" width="344" height="150" rx="8" fill="#fff" stroke="#b9c5d4" stroke-width="1.2"/><rect x="368" y="172" width="344" height="34" rx="8" fill="#eef2f7"/><rect x="368" y="198" width="344" height="8" fill="#eef2f7"/><text x="382" y="195" text-anchor="start" font-size="15" font-weight="600" fill="#16233a">Tests</text><rect x="382" y="219" width="4" height="14" rx="2" fill="#1d4e89"/><text x="392" y="230" text-anchor="start" font-size="11" font-weight="600" fill="#5d6b7d">Right fit</text><text x="496" y="230" text-anchor="start" font-size="13" font-weight="600" fill="#16233a">Sonnet · high</text><rect x="382" y="245" width="4" height="14" rx="2" fill="#5d6b7d"/><text x="392" y="256" text-anchor="start" font-size="11" font-weight="600" fill="#5d6b7d">Step up when</text><text x="496" y="256" text-anchor="start" font-size="13" font-weight="400" fill="#5d6b7d">the rules are critical</text><rect x="382" y="271" width="4" height="14" rx="2" fill="#b7791f"/><text x="392" y="282" text-anchor="start" font-size="11" font-weight="600" fill="#5d6b7d">Overpaying</text><text x="496" y="282" text-anchor="start" font-size="13" font-weight="400" fill="#b7791f">Fable on routine tests</text><rect x="382" y="297" width="4" height="14" rx="2" fill="#b3261e"/><text x="392" y="308" text-anchor="start" font-size="11" font-weight="600" fill="#5d6b7d">Underpowered</text><text x="496" y="308" text-anchor="start" font-size="13" font-weight="400" fill="#b3261e">written by the code's author</text><rect x="8" y="336" width="344" height="150" rx="8" fill="#fff" stroke="#b9c5d4" stroke-width="1.2"/><rect x="8" y="336" width="344" height="34" rx="8" fill="#eef2f7"/><rect x="8" y="362" width="344" height="8" fill="#eef2f7"/><text x="22" y="359" text-anchor="start" font-size="15" font-weight="600" fill="#16233a">Code review</text><rect x="22" y="383" width="4" height="14" rx="2" fill="#1d4e89"/><text x="32" y="394" text-anchor="start" font-size="11" font-weight="600" fill="#5d6b7d">Right fit</text><text x="136" y="394" text-anchor="start" font-size="13" font-weight="600" fill="#16233a">author's model or above · high</text><rect x="22" y="409" width="4" height="14" rx="2" fill="#5d6b7d"/><text x="32" y="420" text-anchor="start" font-size="11" font-weight="600" fill="#5d6b7d">Step up when</text><text x="136" y="420" text-anchor="start" font-size="13" font-weight="400" fill="#5d6b7d">security, money, data</text><rect x="22" y="435" width="4" height="14" rx="2" fill="#b7791f"/><text x="32" y="446" text-anchor="start" font-size="11" font-weight="600" fill="#5d6b7d">Overpaying</text><text x="136" y="446" text-anchor="start" font-size="13" font-weight="400" fill="#b7791f">Fable · max on one line</text><rect x="22" y="461" width="4" height="14" rx="2" fill="#b3261e"/><text x="32" y="472" text-anchor="start" font-size="11" font-weight="600" fill="#5d6b7d">Underpowered</text><text x="136" y="472" text-anchor="start" font-size="13" font-weight="400" fill="#b3261e">reviewer below the author</text><rect x="368" y="336" width="344" height="150" rx="8" fill="#fff" stroke="#b9c5d4" stroke-width="1.2"/><rect x="368" y="336" width="344" height="34" rx="8" fill="#eef2f7"/><rect x="368" y="362" width="344" height="8" fill="#eef2f7"/><text x="382" y="359" text-anchor="start" font-size="15" font-weight="600" fill="#16233a">Architecture</text><rect x="382" y="383" width="4" height="14" rx="2" fill="#1d4e89"/><text x="392" y="394" text-anchor="start" font-size="11" font-weight="600" fill="#5d6b7d">Right fit</text><text x="496" y="394" text-anchor="start" font-size="13" font-weight="600" fill="#16233a">Opus · xhigh</text><rect x="382" y="409" width="4" height="14" rx="2" fill="#5d6b7d"/><text x="392" y="420" text-anchor="start" font-size="11" font-weight="600" fill="#5d6b7d">Step up when</text><text x="496" y="420" text-anchor="start" font-size="13" font-weight="400" fill="#5d6b7d">hard to undo: Fable · max</text><rect x="382" y="435" width="4" height="14" rx="2" fill="#b7791f"/><text x="392" y="446" text-anchor="start" font-size="11" font-weight="600" fill="#5d6b7d">Overpaying</text><text x="496" y="446" text-anchor="start" font-size="13" font-weight="400" fill="#b7791f">Fable · max, reversible</text><rect x="382" y="461" width="4" height="14" rx="2" fill="#b3261e"/><text x="392" y="472" text-anchor="start" font-size="11" font-weight="600" fill="#5d6b7d">Underpowered</text><text x="496" y="472" text-anchor="start" font-size="13" font-weight="400" fill="#b3261e">Sonnet or Haiku</text></svg><svg class="narrow" viewBox="0 0 360 986" role="img" aria-label="Matrix of six software requests — endpoint, bug, refactoring, tests, code review, architecture — each with its right model and effort, when to step up, what overpaying looks like and what being underpowered looks like." xmlns="http://www.w3.org/2000/svg" font-family="IBM Plex Sans, system-ui, sans-serif" color="#16233a"><defs><marker id="h-ink" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1,1 L9,5 L1,9 z" fill="#16233a"/></marker><marker id="h-navy" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1,1 L9,5 L1,9 z" fill="#1d4e89"/></marker><marker id="h-muted" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1,1 L9,5 L1,9 z" fill="#5d6b7d"/></marker><marker id="h-gold" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1,1 L9,5 L1,9 z" fill="#b7791f"/></marker></defs><rect x="8" y="8" width="344" height="150" rx="8" fill="#fff" stroke="#b9c5d4" stroke-width="1.2"/><rect x="8" y="8" width="344" height="34" rx="8" fill="#eef2f7"/><rect x="8" y="34" width="344" height="8" fill="#eef2f7"/><text x="22" y="31" text-anchor="start" font-size="15" font-weight="600" fill="#16233a">Endpoint</text><rect x="22" y="55" width="4" height="14" rx="2" fill="#1d4e89"/><text x="32" y="66" text-anchor="start" font-size="11" font-weight="600" fill="#5d6b7d">Right fit</text><text x="136" y="66" text-anchor="start" font-size="13" font-weight="600" fill="#16233a">Haiku · high</text><rect x="22" y="81" width="4" height="14" rx="2" fill="#5d6b7d"/><text x="32" y="92" text-anchor="start" font-size="11" font-weight="600" fill="#5d6b7d">Step up when</text><text x="136" y="92" text-anchor="start" font-size="13" font-weight="400" fill="#5d6b7d">the rule is ambiguous</text><rect x="22" y="107" width="4" height="14" rx="2" fill="#b7791f"/><text x="32" y="118" text-anchor="start" font-size="11" font-weight="600" fill="#5d6b7d">Overpaying</text><text x="136" y="118" text-anchor="start" font-size="13" font-weight="400" fill="#b7791f">Opus · xhigh</text><rect x="22" y="133" width="4" height="14" rx="2" fill="#b3261e"/><text x="32" y="144" text-anchor="start" font-size="11" font-weight="600" fill="#5d6b7d">Underpowered</text><text x="136" y="144" text-anchor="start" font-size="13" font-weight="400" fill="#b3261e">Haiku · low, vague rule</text><rect x="8" y="172" width="344" height="150" rx="8" fill="#fff" stroke="#b9c5d4" stroke-width="1.2"/><rect x="8" y="172" width="344" height="34" rx="8" fill="#eef2f7"/><rect x="8" y="198" width="344" height="8" fill="#eef2f7"/><text x="22" y="195" text-anchor="start" font-size="15" font-weight="600" fill="#16233a">Bug</text><rect x="22" y="219" width="4" height="14" rx="2" fill="#1d4e89"/><text x="32" y="230" text-anchor="start" font-size="11" font-weight="600" fill="#5d6b7d">Right fit</text><text x="136" y="230" text-anchor="start" font-size="13" font-weight="600" fill="#16233a">Sonnet · high</text><rect x="22" y="245" width="4" height="14" rx="2" fill="#5d6b7d"/><text x="32" y="256" text-anchor="start" font-size="11" font-weight="600" fill="#5d6b7d">Step up when</text><text x="136" y="256" text-anchor="start" font-size="13" font-weight="400" fill="#5d6b7d">it can't be reproduced</text><rect x="22" y="271" width="4" height="14" rx="2" fill="#b7791f"/><text x="32" y="282" text-anchor="start" font-size="11" font-weight="600" fill="#5d6b7d">Overpaying</text><text x="136" y="282" text-anchor="start" font-size="13" font-weight="400" fill="#b7791f">Fable · max on a typo</text><rect x="22" y="297" width="4" height="14" rx="2" fill="#b3261e"/><text x="32" y="308" text-anchor="start" font-size="11" font-weight="600" fill="#5d6b7d">Underpowered</text><text x="136" y="308" text-anchor="start" font-size="13" font-weight="400" fill="#b3261e">Haiku, intermittent bug</text><rect x="8" y="336" width="344" height="150" rx="8" fill="#fff" stroke="#b9c5d4" stroke-width="1.2"/><rect x="8" y="336" width="344" height="34" rx="8" fill="#eef2f7"/><rect x="8" y="362" width="344" height="8" fill="#eef2f7"/><text x="22" y="359" text-anchor="start" font-size="15" font-weight="600" fill="#16233a">Refactoring</text><rect x="22" y="383" width="4" height="14" rx="2" fill="#1d4e89"/><text x="32" y="394" text-anchor="start" font-size="11" font-weight="600" fill="#5d6b7d">Right fit</text><text x="136" y="394" text-anchor="start" font-size="13" font-weight="600" fill="#16233a">Sonnet · medium</text><rect x="22" y="409" width="4" height="14" rx="2" fill="#5d6b7d"/><text x="32" y="420" text-anchor="start" font-size="11" font-weight="600" fill="#5d6b7d">Step up when</text><text x="136" y="420" text-anchor="start" font-size="13" font-weight="400" fill="#5d6b7d">the structure changes</text><rect x="22" y="435" width="4" height="14" rx="2" fill="#b7791f"/><text x="32" y="446" text-anchor="start" font-size="11" font-weight="600" fill="#5d6b7d">Overpaying</text><text x="136" y="446" text-anchor="start" font-size="13" font-weight="400" fill="#b7791f">Opus on a rename</text><rect x="22" y="461" width="4" height="14" rx="2" fill="#b3261e"/><text x="32" y="472" text-anchor="start" font-size="11" font-weight="600" fill="#5d6b7d">Underpowered</text><text x="136" y="472" text-anchor="start" font-size="13" font-weight="400" fill="#b3261e">many files, no tests</text><rect x="8" y="500" width="344" height="150" rx="8" fill="#fff" stroke="#b9c5d4" stroke-width="1.2"/><rect x="8" y="500" width="344" height="34" rx="8" fill="#eef2f7"/><rect x="8" y="526" width="344" height="8" fill="#eef2f7"/><text x="22" y="523" text-anchor="start" font-size="15" font-weight="600" fill="#16233a">Tests</text><rect x="22" y="547" width="4" height="14" rx="2" fill="#1d4e89"/><text x="32" y="558" text-anchor="start" font-size="11" font-weight="600" fill="#5d6b7d">Right fit</text><text x="136" y="558" text-anchor="start" font-size="13" font-weight="600" fill="#16233a">Sonnet · high</text><rect x="22" y="573" width="4" height="14" rx="2" fill="#5d6b7d"/><text x="32" y="584" text-anchor="start" font-size="11" font-weight="600" fill="#5d6b7d">Step up when</text><text x="136" y="584" text-anchor="start" font-size="13" font-weight="400" fill="#5d6b7d">the rules are critical</text><rect x="22" y="599" width="4" height="14" rx="2" fill="#b7791f"/><text x="32" y="610" text-anchor="start" font-size="11" font-weight="600" fill="#5d6b7d">Overpaying</text><text x="136" y="610" text-anchor="start" font-size="13" font-weight="400" fill="#b7791f">Fable on routine tests</text><rect x="22" y="625" width="4" height="14" rx="2" fill="#b3261e"/><text x="32" y="636" text-anchor="start" font-size="11" font-weight="600" fill="#5d6b7d">Underpowered</text><text x="136" y="636" text-anchor="start" font-size="13" font-weight="400" fill="#b3261e">written by the code's author</text><rect x="8" y="664" width="344" height="150" rx="8" fill="#fff" stroke="#b9c5d4" stroke-width="1.2"/><rect x="8" y="664" width="344" height="34" rx="8" fill="#eef2f7"/><rect x="8" y="690" width="344" height="8" fill="#eef2f7"/><text x="22" y="687" text-anchor="start" font-size="15" font-weight="600" fill="#16233a">Code review</text><rect x="22" y="711" width="4" height="14" rx="2" fill="#1d4e89"/><text x="32" y="722" text-anchor="start" font-size="11" font-weight="600" fill="#5d6b7d">Right fit</text><text x="136" y="722" text-anchor="start" font-size="13" font-weight="600" fill="#16233a">author's model or above · high</text><rect x="22" y="737" width="4" height="14" rx="2" fill="#5d6b7d"/><text x="32" y="748" text-anchor="start" font-size="11" font-weight="600" fill="#5d6b7d">Step up when</text><text x="136" y="748" text-anchor="start" font-size="13" font-weight="400" fill="#5d6b7d">security, money, data</text><rect x="22" y="763" width="4" height="14" rx="2" fill="#b7791f"/><text x="32" y="774" text-anchor="start" font-size="11" font-weight="600" fill="#5d6b7d">Overpaying</text><text x="136" y="774" text-anchor="start" font-size="13" font-weight="400" fill="#b7791f">Fable · max on one line</text><rect x="22" y="789" width="4" height="14" rx="2" fill="#b3261e"/><text x="32" y="800" text-anchor="start" font-size="11" font-weight="600" fill="#5d6b7d">Underpowered</text><text x="136" y="800" text-anchor="start" font-size="13" font-weight="400" fill="#b3261e">reviewer below the author</text><rect x="8" y="828" width="344" height="150" rx="8" fill="#fff" stroke="#b9c5d4" stroke-width="1.2"/><rect x="8" y="828" width="344" height="34" rx="8" fill="#eef2f7"/><rect x="8" y="854" width="344" height="8" fill="#eef2f7"/><text x="22" y="851" text-anchor="start" font-size="15" font-weight="600" fill="#16233a">Architecture</text><rect x="22" y="875" width="4" height="14" rx="2" fill="#1d4e89"/><text x="32" y="886" text-anchor="start" font-size="11" font-weight="600" fill="#5d6b7d">Right fit</text><text x="136" y="886" text-anchor="start" font-size="13" font-weight="600" fill="#16233a">Opus · xhigh</text><rect x="22" y="901" width="4" height="14" rx="2" fill="#5d6b7d"/><text x="32" y="912" text-anchor="start" font-size="11" font-weight="600" fill="#5d6b7d">Step up when</text><text x="136" y="912" text-anchor="start" font-size="13" font-weight="400" fill="#5d6b7d">hard to undo: Fable · max</text><rect x="22" y="927" width="4" height="14" rx="2" fill="#b7791f"/><text x="32" y="938" text-anchor="start" font-size="11" font-weight="600" fill="#5d6b7d">Overpaying</text><text x="136" y="938" text-anchor="start" font-size="13" font-weight="400" fill="#b7791f">Fable · max, reversible</text><rect x="22" y="953" width="4" height="14" rx="2" fill="#b3261e"/><text x="32" y="964" text-anchor="start" font-size="11" font-weight="600" fill="#5d6b7d">Underpowered</text><text x="136" y="964" text-anchor="start" font-size="13" font-weight="400" fill="#b3261e">Sonnet or Haiku</text></svg><figcaption>Six requests and the right fit for each, as model · effort. Above it you overpay; below it you risk the rework.</figcaption></figure>

Read together, the six show a pattern: the cheap end of the matrix is where
the work is already decided and only needs doing, the expensive end is where
the work *is* the deciding, and none of the cells is a law, only a place to
start before your own work moves a row up or down.

## The team that chooses for you

A matrix is only useful if someone consults it, and the lesson of episode 4
is that, left alone, nobody does: the default wins, and the default is the
most expensive model, which is where **subagent-driven development** comes in.

A **subagent** is a second AI worker that the main one hands a piece of work
to. It starts with a clean slate: it reads only what it needs for its piece,
does the heavy lifting on its own, and hands back a short result, so the main
conversation stays small and focused. That clean slate is the point of the
design and also its demand, because a subagent knows nothing the hand-off does
not tell it. It is also exactly the small,
well-defined job that keeps a cheap model at its cheap price.
Subagent-driven development is organising the work this way on purpose: a
**lead** that understands the request, decides the plan and checks the
result, and **helpers**, the subagents, that each do one kind of work at the
model and effort that kind of work deserves.

Our team, which [The Culture You Can Install]({{< relref "the-culture-you-can-install.md" >}})
describes in full, has five helpers, and their settings are the matrix
written into the team itself.

<!-- fig:team -->
<figure class="diagram"><svg class="wide" viewBox="0 0 720 224" role="img" aria-label="Diagram of the lead on top handing work to five helpers below: reader on Sonnet at low effort, builder on Sonnet at medium, tester on Sonnet at high, reviewer and QA lead on the lead's model at high." xmlns="http://www.w3.org/2000/svg" font-family="IBM Plex Sans, system-ui, sans-serif" color="#16233a"><defs><marker id="h-ink" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1,1 L9,5 L1,9 z" fill="#16233a"/></marker><marker id="h-navy" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1,1 L9,5 L1,9 z" fill="#1d4e89"/></marker><marker id="h-muted" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1,1 L9,5 L1,9 z" fill="#5d6b7d"/></marker><marker id="h-gold" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1,1 L9,5 L1,9 z" fill="#b7791f"/></marker></defs><rect x="240" y="12" width="240" height="70" rx="6" fill="#1d4e89" stroke="#173d6e" stroke-width="1.2"/><text x="360.0" y="38.0" text-anchor="middle" font-size="15" font-weight="600" fill="#fff">Lead</text><text x="360.0" y="54.0" text-anchor="middle" font-size="10.5" font-weight="400" fill="#cfe0f5">decides, plans, checks</text><text x="360.0" y="68.0" text-anchor="middle" font-size="10.5" font-weight="400" fill="#cfe0f5">Opus</text><path d="M 360,82 L 360,112" fill="none" stroke="#1d4e89" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/><path d="M 76,112 L 644,112" fill="none" stroke="#1d4e89" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/><text x="368" y="104" text-anchor="start" font-size="11" font-weight="600" fill="#1d4e89">hands each piece over, choosing the model</text><path d="M 76.0,112 L 76.0,130" fill="none" stroke="#1d4e89" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" marker-end="url(#h-navy)"/><rect x="10.0" y="134" width="132" height="78" rx="6" fill="#fff" stroke="#b9c5d4" stroke-width="1.2"/><text x="76.0" y="164.0" text-anchor="middle" font-size="14" font-weight="600" fill="#16233a">Reader</text><text x="76.0" y="180.0" text-anchor="middle" font-size="10.5" font-weight="400" fill="#5d6b7d">Sonnet · low</text><text x="76.0" y="194.0" text-anchor="middle" font-size="10.5" font-weight="400" fill="#5d6b7d">reads and reports</text><path d="M 218.0,112 L 218.0,130" fill="none" stroke="#1d4e89" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" marker-end="url(#h-navy)"/><rect x="152.0" y="134" width="132" height="78" rx="6" fill="#fff" stroke="#b9c5d4" stroke-width="1.2"/><text x="218.0" y="164.0" text-anchor="middle" font-size="14" font-weight="600" fill="#16233a">Builder</text><text x="218.0" y="180.0" text-anchor="middle" font-size="10.5" font-weight="400" fill="#5d6b7d">Sonnet · medium</text><text x="218.0" y="194.0" text-anchor="middle" font-size="10.5" font-weight="400" fill="#5d6b7d">Haiku for trivial changes</text><path d="M 360.0,112 L 360.0,130" fill="none" stroke="#1d4e89" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" marker-end="url(#h-navy)"/><rect x="294.0" y="134" width="132" height="78" rx="6" fill="#fff" stroke="#b9c5d4" stroke-width="1.2"/><text x="360.0" y="164.0" text-anchor="middle" font-size="14" font-weight="600" fill="#16233a">Tester</text><text x="360.0" y="180.0" text-anchor="middle" font-size="10.5" font-weight="400" fill="#5d6b7d">Sonnet · high</text><text x="360.0" y="194.0" text-anchor="middle" font-size="10.5" font-weight="400" fill="#5d6b7d">attacks the work</text><path d="M 502.0,112 L 502.0,130" fill="none" stroke="#1d4e89" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" marker-end="url(#h-navy)"/><rect x="436.0" y="134" width="132" height="78" rx="6" fill="#fff" stroke="#b9c5d4" stroke-width="1.2"/><text x="502.0" y="164.0" text-anchor="middle" font-size="14" font-weight="600" fill="#16233a">Reviewer</text><text x="502.0" y="180.0" text-anchor="middle" font-size="10.5" font-weight="400" fill="#5d6b7d">lead's model · high</text><text x="502.0" y="194.0" text-anchor="middle" font-size="10.5" font-weight="400" fill="#5d6b7d">never below the author</text><path d="M 644.0,112 L 644.0,130" fill="none" stroke="#1d4e89" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" marker-end="url(#h-navy)"/><rect x="578.0" y="134" width="132" height="78" rx="6" fill="#fff" stroke="#b9c5d4" stroke-width="1.2"/><text x="644.0" y="164.0" text-anchor="middle" font-size="14" font-weight="600" fill="#16233a">QA lead</text><text x="644.0" y="180.0" text-anchor="middle" font-size="10.5" font-weight="400" fill="#5d6b7d">lead's model · high</text><text x="644.0" y="194.0" text-anchor="middle" font-size="10.5" font-weight="400" fill="#5d6b7d">decides what tests cover</text></svg><svg class="narrow" viewBox="0 0 360 462" role="img" aria-label="Diagram of the lead on top handing work to five helpers below: reader on Sonnet at low effort, builder on Sonnet at medium, tester on Sonnet at high, reviewer and QA lead on the lead's model at high." xmlns="http://www.w3.org/2000/svg" font-family="IBM Plex Sans, system-ui, sans-serif" color="#16233a"><defs><marker id="h-ink" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1,1 L9,5 L1,9 z" fill="#16233a"/></marker><marker id="h-navy" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1,1 L9,5 L1,9 z" fill="#1d4e89"/></marker><marker id="h-muted" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1,1 L9,5 L1,9 z" fill="#5d6b7d"/></marker><marker id="h-gold" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1,1 L9,5 L1,9 z" fill="#b7791f"/></marker></defs><rect x="8" y="8" width="344" height="70" rx="6" fill="#1d4e89" stroke="#173d6e" stroke-width="1.2"/><text x="180.0" y="34.0" text-anchor="middle" font-size="15" font-weight="600" fill="#fff">Lead</text><text x="180.0" y="50.0" text-anchor="middle" font-size="10.5" font-weight="400" fill="#cfe0f5">decides, plans, checks</text><text x="180.0" y="64.0" text-anchor="middle" font-size="10.5" font-weight="400" fill="#cfe0f5">Opus</text><text x="36" y="100" text-anchor="start" font-size="11" font-weight="600" fill="#1d4e89">hands each piece over, choosing the model</text><path d="M 22,78 L 22,424" fill="none" stroke="#1d4e89" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/><path d="M 22,144 L 34,144" fill="none" stroke="#1d4e89" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" marker-end="url(#h-navy)"/><rect x="38" y="112" width="314" height="62" rx="6" fill="#fff" stroke="#b9c5d4" stroke-width="1.2"/><text x="195.0" y="134.0" text-anchor="middle" font-size="14" font-weight="600" fill="#16233a">Reader</text><text x="195.0" y="150.0" text-anchor="middle" font-size="10.5" font-weight="400" fill="#5d6b7d">Sonnet · low</text><text x="195.0" y="164.0" text-anchor="middle" font-size="10.5" font-weight="400" fill="#5d6b7d">reads and reports</text><path d="M 22,214 L 34,214" fill="none" stroke="#1d4e89" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" marker-end="url(#h-navy)"/><rect x="38" y="182" width="314" height="62" rx="6" fill="#fff" stroke="#b9c5d4" stroke-width="1.2"/><text x="195.0" y="204.0" text-anchor="middle" font-size="14" font-weight="600" fill="#16233a">Builder</text><text x="195.0" y="220.0" text-anchor="middle" font-size="10.5" font-weight="400" fill="#5d6b7d">Sonnet · medium</text><text x="195.0" y="234.0" text-anchor="middle" font-size="10.5" font-weight="400" fill="#5d6b7d">Haiku for trivial changes</text><path d="M 22,284 L 34,284" fill="none" stroke="#1d4e89" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" marker-end="url(#h-navy)"/><rect x="38" y="252" width="314" height="62" rx="6" fill="#fff" stroke="#b9c5d4" stroke-width="1.2"/><text x="195.0" y="274.0" text-anchor="middle" font-size="14" font-weight="600" fill="#16233a">Tester</text><text x="195.0" y="290.0" text-anchor="middle" font-size="10.5" font-weight="400" fill="#5d6b7d">Sonnet · high</text><text x="195.0" y="304.0" text-anchor="middle" font-size="10.5" font-weight="400" fill="#5d6b7d">attacks the work</text><path d="M 22,354 L 34,354" fill="none" stroke="#1d4e89" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" marker-end="url(#h-navy)"/><rect x="38" y="322" width="314" height="62" rx="6" fill="#fff" stroke="#b9c5d4" stroke-width="1.2"/><text x="195.0" y="344.0" text-anchor="middle" font-size="14" font-weight="600" fill="#16233a">Reviewer</text><text x="195.0" y="360.0" text-anchor="middle" font-size="10.5" font-weight="400" fill="#5d6b7d">lead's model · high</text><text x="195.0" y="374.0" text-anchor="middle" font-size="10.5" font-weight="400" fill="#5d6b7d">never below the author</text><path d="M 22,424 L 34,424" fill="none" stroke="#1d4e89" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" marker-end="url(#h-navy)"/><rect x="38" y="392" width="314" height="62" rx="6" fill="#fff" stroke="#b9c5d4" stroke-width="1.2"/><text x="195.0" y="414.0" text-anchor="middle" font-size="14" font-weight="600" fill="#16233a">QA lead</text><text x="195.0" y="430.0" text-anchor="middle" font-size="10.5" font-weight="400" fill="#5d6b7d">lead's model · high</text><text x="195.0" y="444.0" text-anchor="middle" font-size="10.5" font-weight="400" fill="#5d6b7d">decides what tests cover</text></svg><figcaption>The lead and its five helpers. Effort is fixed in each role; the model is chosen by the lead for each request.</figcaption></figure>

The **reader** runs on Sonnet at low effort, because it reads and reports and
decides nothing, which is the documentation's own example of what low effort
is for. The **builder** runs on Sonnet at medium, because by the time it
receives a change the change is already decided, and the lead can hand a
trivial one to Haiku. The **tester** runs on Sonnet at high, because attacking
work needs depth and patience more than seniority. The **reviewer** and the
**QA lead**, which decides what the testing must cover, both work at the
lead's own model and at high effort, because they are the two places where a
weaker worker would let the lead's mistakes through.

There is a principle hidden in that arrangement, and it is the one I would
take from this article if I took only one: **effort belongs to the role, and
the model belongs to the request.** Each helper's effort is fixed in its own
description, because the kind of thinking a job needs is a property of the
job, while the model is chosen by the lead each time it hands work over,
because how hard *this* change is depends on the change. So the team does not hit
every cell of the matrix exactly: the endpoint that the matrix
puts on Haiku at high comes out as the builder on Haiku at its usual medium,
and that is a trade we accept on purpose, because a team whose roles behave
the same way every time is predictable and cheap to run, and a little
precision is a fair price for that. When one request truly needs a different
effort, the tooling allows it to be set for that one hand-off.

Episode 4 told the story of what happens without this. Our tester had no
model named in its description, so for 1,441 rounds of work it silently
inherited the most expensive one, at 13 cents a round; once it was named, the
same job cost under 5 cents. Nobody had chosen badly; nobody had chosen at
all.

## The lead is the next lever

Episode 4 ended by pointing at the lead itself, which after the helpers moved
to cheaper models had become about seventy per cent of a quiet day's bill. The
matrix answers that in theory, because the lead is a worker like any other and
its model can be chosen per working session. A session spent on architecture,
or on a change that needs a demanding review, keeps Opus as the lead, while a
day of routine endpoints and small fixes can be led by Sonnet.

There is a risk in that, and it is worth naming plainly: the reviewer and the
QA lead follow the lead's model, so when the lead steps down they step down
with it. Lowering the lead is right only on days where a Sonnet-level review is
enough, which is most days and not every day. This is a recommendation we have
not measured yet, and when we have the receipt it will be an episode.

## The right fit

The spreadsheet is closed now, because what it was really saying fits on one
page. Efficiency with AI is not
the cheapest model or the most capable one. It is a choice made per request,
on price and quantity, by asking how hard the job is and how expensive a mistake would
be, and it fails on both sides: you either pay for judgment you did not use,
or you pay twice for the judgment you did not buy. The default is what costs
money, because the default is the most expensive model doing everything, and
the cure is structure, a lead and its helpers with the choice written into
each role, so that the right fit happens even on the
Monday nobody remembers to think about it.

---

*Sources. Prices and effort levels are Anthropic's published list prices and
documentation as of October 2026; the run-low-then-redo result comes from
Anthropic's own coding tests; the figures about our work are episode 4's.*
