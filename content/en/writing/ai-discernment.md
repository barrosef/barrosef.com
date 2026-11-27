---
title: "Look before you trust: Discernment, the third D of AI Fluency"
seoTitle: "Judging AI output: product, process and performance"
date: 2026-11-27T10:00:00-04:00
draft: false
translationKey: "ai-fluency-discernment"
categories: ["Technology"]
tags: ["ai-fluency", "generative-ai"]
description: "Episode 4 of AI Fluency. Discernment, the craft of judging what AI gives back: whether the result is right, whether the reasoning behind it holds up and whether the way it works with you is serving you."
---

*Fourth episode of **AI Fluency**, a series that walks through the AI Fluency
Framework one competency at a time. [Episode 1](/writing/ai-fluency-mapped/) drew
the whole map, [episode 2](/writing/ai-delegation/) walked Delegation, the decision
made before you type, and [episode 3](/writing/ai-description/) walked Description,
what you type; this one is about what you do with the answer.*

---

It is Friday morning, and the coupon for Black Friday is due on Monday. On
Thursday evening you sent the AI a prompt you could be proud of, one that said
what you wanted back, asked for the edge cases before any code and told the
assistant to be brief, to ask instead of guessing and to point out the holes in
your plan. It listed the edge cases, you added the customer who opens two browser
tabs and applies the coupon in both, and you went to bed while it wrote the code.
The answer waiting for you now is everything a tired developer hopes to read:
"Done. The BLACKFRIDAY coupon is in checkout and all 14 tests pass", followed by
a tidy summary, a neat list of changed files and a green row of tests, and the
temptation is to merge it, close the laptop and enjoy the rest of the day.

That temptation is precisely what the next competency is about. The AI Fluency
Framework, developed by Rick Dakan, Joseph Feller and Anthropic, calls it
**Discernment**: accurately assessing the usefulness of AI outputs and behaviours,
or, in the fuller words of the framework's glossary, thoughtfully and critically
evaluating AI outputs, processes, behaviours and interactions, which includes
assessing quality, accuracy and appropriateness and deciding what to improve.
Description was about getting what is in your head into the box, and Discernment
is the reverse movement, taking what came out of the box and holding it up
against what you know, which is the one thing the AI never had access to in the
first place.

## The branch, up close

<figure class="diagram fluency-map fluency-map--main">
  <a href="/img/ai-fluency/discernment-map.en.svg">
    <picture>
      <source media="(max-width: 1099px)" srcset="/img/ai-fluency/discernment-map-narrow.en.svg">
      <img src="/img/ai-fluency/discernment-map.en.svg" width="1200" height="770" loading="lazy"
        alt="Mind map of Discernment, the third competency of the AI Fluency Framework: judging what comes back, and how it got there. Three branches. Product discernment, the output, accurate, fitting, coherent and relevant, with the questions: is it right or only tidy, is it what I asked for, what would break it. Process discernment, how AI arrived at its output, with the questions: does each step follow, what did it skip or assume, would I reason that way. Performance discernment, how AI behaves while you work together, with the questions: is its style working for me, did it ask or guess, is it only agreeing with me.">
    </picture>
  </a>
  <figcaption>Based on the AI Fluency Framework © 2025 Rick Dakan, Joseph Feller and Anthropic, CC BY-NC-SA 4.0. The skills are the framework's and the one-line summaries condense its definitions; the questions around them are my reading. Shared under the same license. Tap or click to open it full size.</figcaption>
</figure>

If the map looks familiar, it is meant to. Discernment splits along the same
three lines as Description, product, process and performance, so each thing you
asked for on Thursday becomes something you check on Friday: the result you
described is now a result to judge, the steps you asked for are now reasoning to
follow, and the way you asked the AI to behave is now behaviour you can observe.
The questions around each skill are mine, the ones I find most useful when an
answer looks finished, and like last episode's they are less a form to fill in
than a way of catching the thing that a quick glance lets through.

## Product discernment: is it right, or only tidy?

**Product discernment** is evaluating the quality of what the AI produces, and
the framework names four qualities to look for: accuracy, appropriateness,
coherence and relevance. The difficulty is that a modern assistant produces
answers that score very well on the qualities you can see at a glance, since the
code is well formatted, the names are sensible and the summary reads like it was
written by a careful colleague, while the quality that matters most, whether it
does the right thing for your business, can only be judged by someone who knows
the business. So you do the one thing the AI could not do for you, which is to
try the coupon the way a real customer would: you apply it, switch the payment
method to upfront payment, and watch the two discounts stack on top of each other,
exactly what your rule forbids.

What makes the moment instructive is the note that came with the code, which said
in a calm and confident sentence that stacking was impossible because the
upfront-payment discount is always applied after the coupon. The framework's
glossary has a word for this, hallucination, an AI stating something plausible
with confidence when it is not true, and the lesson is not that the assistant
lies but that the confidence of the wording tells you nothing about its accuracy.
A claim that matters, one the rest of the change depends on, deserves a check
against the real code or the real behaviour, however reasonable it sounds.

## Process discernment: does the reasoning hold up?

**Process discernment** is evaluating how the AI arrived at its output, looking
for logical errors, lapses in attention or inappropriate reasoning steps, and this
is where Thursday's request to explain the plan before each change pays off,
because the plan is now on the page for you to read. Reading it with the
stacking bug in mind, you see where it went wrong: the plan checks the rule once,
at the moment the coupon is applied, and never again, as if the cart could not
change afterwards. That is a logical error in the reasoning, not a typo in the
code, and it explains why the tests did not catch it, since the same AI wrote all
fourteen of them from the same assumption, so the green row proves that the code
does what the AI believed, which is a different thing from what the business
needs.

The plan also shows a lapse in attention, the kind a human reviewer makes on a
long day: it never mentions guest checkout, where a customer buys without an
account, so the rule of one use per customer has no customer to count. Nothing in
the code is wrong there; something is simply missing, and missing things are the
hardest to see in a finished answer, because nothing on the screen points at
them. Reading the reasoning rather than only the result is how you find them, and
it is also why asking the AI to show its reasoning, in Description, and
questioning that reasoning, in Discernment, are two halves of the same habit.

## Performance discernment: is the way it works with you working?

**Performance discernment** is evaluating how the AI behaves during the
interaction, considering whether its communication style is effective for your
needs, and it is the one people rarely think about, even though Thursday's
prompt made it easy to check. You asked for brief answers and received three
pages, you asked to be asked when a rule was unclear and the AI guessed how to
round the discount instead, and you asked to hear about holes in your plan and
heard nothing, although the plan had at least two. None of this is a moral
failing on the machine's part, since assistants lean towards long, agreeable
answers by default, but noticing it matters, because an assistant that always
agrees with you is pleasant to work with and very poor at the job you gave it.

Performance discernment feeds straight back into performance description: once
you see that the assistant is guessing instead of asking, you say so again, more
firmly, or you tell it to list its assumptions before writing anything, and on a
long task you check again after a while, since behaviour tends to drift back
towards the defaults as a conversation grows.

## What the review caught

<figure class="diagram fluency-map fluency-map--split">
  <a href="/img/ai-fluency/discernment-review.en.svg">
    <img src="/img/ai-fluency/discernment-review.en.svg" width="400" height="683" loading="lazy"
      alt="The AI's answer and what a review caught. What came back: Done, the BLACKFRIDAY coupon is in checkout and all 14 tests pass. What the review caught, in four parts. Product: switch the payment method after the coupon, and it stacks with the upfront-payment discount. Process: its plan checks the rule once, when the coupon is applied, and the 14 tests share that assumption. Process: it skipped guest checkout, where one use per customer has no customer to count. Performance: three pages after you asked for brief, a guess about rounding instead of a question, and no hole flagged in your plan.">
  </a>
  <figcaption>An example; the tags are my reading of the framework's three Discernment skills, AI Fluency Framework, CC BY-NC-SA 4.0.</figcaption>
</figure>

Put the three skills together and the cheerful one-line answer from Friday
morning turns into the review in the figure, four findings that took perhaps
twenty minutes to reach and that would have taken a good deal longer to reach on
the Saturday after Black Friday, with real customers and real refunds involved.
One finding is about the product, two are about the process that produced it and
one is about the way the AI worked with you, and only the first would have shown
up in a quick look at the screen; the other three needed you to read the
reasoning and to remember what you had asked for.

## What the research sees

<figure class="diagram fluency-map fluency-map--split">
  <a href="/img/ai-fluency/discernment-index.en.svg">
    <img src="/img/ai-fluency/discernment-index.en.svg" width="400" height="530" loading="lazy"
      alt="Bar chart from The AI Fluency Index, share of 9,830 conversations on Claude.ai. Spots missing context 20.3%. Questions weak reasoning 15.8%. Checks facts that matter 8.7%. With and without iteration: spots missing context 22.8% against 5.7%; questions weak reasoning 17.9% against 3.2%.">
  </a>
  <figcaption>Source: The AI Fluency Index, Anthropic, February 2026, a sample of conversations from January 2026, which calls these the three discernment behaviours. Labels shortened by me.</figcaption>
</figure>

Anthropic's AI Fluency Index, the study published in February 2026 that
classified fluency behaviours in 9,830 conversations on Claude.ai, measured three
behaviours that it groups as discernment, and all three are rare. In about one
conversation in five, 20.3%, people noticed that the AI might be missing
context; in 15.8% they questioned reasoning that did not hold up; and in only
8.7% did they check the facts and claims that mattered. Compared with the
description behaviours of the last episode, where half of all conversations
clarified the goal, judging the answer turns out to be much less common than
asking for it.

The same pattern as before appears when the study compares conversations that
went back and forth with those that stopped at the first answer, only stronger.
People who iterated spotted missing context in 22.8% of conversations against
5.7% for those who did not, and questioned the reasoning in 17.9% against 3.2%,
which the authors describe as being 5.6 times more likely to question Claude's
reasoning and 4 times more likely to identify missing context. As always with
this study, these are correlations, and the authors are careful to say that
people may well be evaluating the output outside the conversation, by testing it
or using it, which the classifiers cannot see. For a developer that caveat is
real, since running the code is a form of discernment, but it only counts when
the tests are ones you wrote or at least read, not the fourteen the AI wrote from
its own assumption.

<figure class="diagram fluency-map fluency-map--split">
  <a href="/img/ai-fluency/discernment-finished.en.svg">
    <img src="/img/ai-fluency/discernment-finished.en.svg" width="400" height="606" loading="lazy"
      alt="When the work looks finished, conversations where AI produced code or a document against those where it did not. Spots missing context 15.8% against 21.0%. Questions weak reasoning 13.0% against 16.2%. Checks facts that matter 5.5% against 9.2%. The moment to pause, three questions: is this accurate, is anything missing, does this reasoning hold up.">
  </a>
  <figcaption>Source: The AI Fluency Index, Anthropic, February 2026; the three questions are the study's own advice. Labels shortened by me.</figcaption>
</figure>

The most useful finding for this episode is the one the last episode ended on.
In conversations where the AI produced an artifact, such as code or a document,
people described their request more carefully at the start, yet all three
discernment behaviours fell: spotting missing context from 21% to 15.8%,
questioning reasoning from 16.2% to 13% and checking facts from 9.2% to 5.5%.
The authors suggest that polished, functional-looking outputs may make further
questions feel unnecessary, and they put it in one plain sentence, that if the
work looks finished, users might treat it as such. Their advice for that moment
is just as plain: when the AI produces something that looks good, pause and ask
whether it is accurate, whether anything is missing and whether the reasoning
holds up, three questions that line up neatly, in my reading, with the three
behaviours they measured.

## The loop that closes on Friday

<figure class="diagram fluency-map fluency-map--split">
  <a href="/img/ai-fluency/discernment-loop.en.svg">
    <img src="/img/ai-fluency/discernment-loop.en.svg" width="400" height="578" loading="lazy"
      alt="The Description–Discernment loop on Friday morning, four steps on a ring: describe, Thursday's prompt; AI answers, code and 14 green tests; discern, it stacks with the upfront discount; refine, check again when payment changes. In the middle: 5.6 times more likely to question the reasoning when people iterate.">
  </a>
  <figcaption>The loop is from the AI Fluency Framework, CC BY-NC-SA 4.0; the ratio is from The AI Fluency Index, Anthropic, 2026. The steps are an example.</figcaption>
</figure>

Episode 3 drew Description and Discernment as one loop, the moment-to-moment
craft of working with AI, and Friday morning is that loop closing. Thursday's
description produced code and fourteen green tests, Friday's discernment found
the stacking discount, the single check and the missing guest, and each finding
becomes a line in the next description: check the rule again whenever the
payment method changes, cover guest checkout by email address, write tests for
both cases before touching the code, and list every assumption before writing
anything. The second round comes back closer, you judge it again, and somewhere
in the third round the answer is not only tidy but right.

## Back to Friday morning

Replay the morning once more. The answer arrived looking finished, and instead
of treating it as finished you tried it the way a customer would, read the plan
the way a reviewer would, and compared the assistant's behaviour with what you
had asked for, which turned a cheerful "all 14 tests pass" into four concrete
fixes and a much quieter weekend. The same three questions, is it right, does the
reasoning hold up and is the way it works with me working, apply just as well to
a database migration, a contract summary or a market report, and the Index's
authors make a point worth keeping in mind: as AI gets better at producing
polished outputs, the ability to evaluate them becomes more valuable, not less.

What Discernment cannot settle on its own is who answers for the coupon when it
goes live on Monday, who gets told that an AI wrote most of it, and whether the
tool you used was the right one to trust with the payment code in the first
place. That is the subject of the last episode, on Diligence: owning the result,
from creation to transparency to deployment.

*Sources: Anthropic's [AI Fluency Framework](https://www-cdn.anthropic.com/b383cf6baddbfc72fdf8b0ed533a518e2872d531.pdf)
and [Key Terminology Cheat Sheet](https://www-cdn.anthropic.com/4396730ed190e691a3712cf2fd6bfe35509deca2.pdf),
© 2025 Rick Dakan, Joseph Feller and Anthropic, CC BY-NC-SA 4.0; the course
[AI Fluency: Framework & Foundations](https://anthropic.skilljar.com/ai-fluency-framework-foundations);
and [The AI Fluency Index](https://www.anthropic.com/research/AI-fluency-index)
(Swanson, Bent, Ludwig, Dakan and Feller, February 2026). This article is an
independent explainer, not an Anthropic publication.*
