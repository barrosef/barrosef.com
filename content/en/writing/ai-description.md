---
title: "Say what you mean: Description, the second D of AI Fluency"
seoTitle: "Describing to AI: product, process and performance"
date: 2026-11-18T09:00:00-04:00
draft: false
translationKey: "ai-fluency-description"
categories: ["Technology"]
tags: ["ai-fluency", "generative-ai"]
description: "Episode 3 of AI Fluency. Description, the craft of saying what you need: the product you want back, the process the AI should follow and the way it should work with you."
---

*Third episode of **AI Fluency**, a series that walks through the AI Fluency
Framework one competency at a time. [Episode 1](/writing/ai-fluency-mapped/) drew
the whole map and [episode 2](/writing/ai-delegation/) walked Delegation, the
decision made before you type; this one is about what you type.*

---

Let us go back to that Thursday evening with the Black Friday coupon due on
Monday. Last time you did the hard part before opening the assistant: you wrote
down what the rule is really for, you remembered that the tool cannot see your
repository or your meetings, and you decided to keep the business rules and the
review with you while handing the first version of the code and the tests to the
AI. The cursor is now blinking in an empty box, and the old habit is still there,
ready to type "add the coupon rule to our checkout" and hope for the best. The
decision behind the request is a good one this time, yet a good decision said
badly still lands in the wrong place, because the AI only knows what you put into
words, and everything you leave out it fills in with a guess that sounds
reasonable and is usually average.

The AI Fluency Framework, developed by Rick Dakan, Joseph Feller and Anthropic,
calls that craft **Description**: effectively describing goals to prompt useful AI
behaviours and outputs, or, in the words of the framework's glossary, effectively
communicating with AI systems by clearly defining outputs, guiding AI processes
and specifying the behaviour you want during the collaboration. It is the
competency most people know by its popular name, prompting, and the framework
does something useful with it, which is to split it into three questions you can
answer one at a time, so that a good prompt stops being a matter of inspiration
and becomes a matter of not forgetting anything.

## The branch, up close

<figure class="diagram fluency-map fluency-map--main">
  <a href="/img/ai-fluency/description-map.en.svg">
    <picture>
      <source media="(max-width: 1099px)" srcset="/img/ai-fluency/description-map-narrow.en.svg">
      <img src="/img/ai-fluency/description-map.en.svg" width="1200" height="770" loading="lazy"
        alt="Mind map of Description, the second competency of the AI Fluency Framework: saying what you need so AI can deliver it. Three branches. Product description, the output, its format, audience and style, with the questions: what should come back and in what shape, who will read or run it, can I show an example of good. Process description, how AI approaches your request, with the questions: which steps and in what order, what context and rules does it need, think first or answer straight away. Performance description, how AI behaves while you work together, with the questions: brief or detailed, challenge me or support me, ask me or assume.">
    </picture>
  </a>
  <figcaption>Based on the AI Fluency Framework © 2025 Rick Dakan, Joseph Feller and Anthropic, CC BY-NC-SA 4.0. The skills are the framework's and the one-line summaries condense its definitions; the questions around them are my reading. Shared under the same license. Tap or click to open it full size.</figcaption>
</figure>

The three skills on the map are the framework's, and they divide the request
along a line that is easy to remember once you have seen it: what you want back,
how the AI should get there and how it should behave with you along the way. The
questions around each skill are mine, the ones I find myself running through
before I press enter, and they work less as a template to fill in than as a
checklist that catches the thing you were about to leave out.

## Product description: what should come back

**Product description** is defining what you want in terms of outputs, format,
audience and style, and it is the part most people already do, if only halfway.
"Add the coupon rule" names a product, but it leaves the AI to decide what kind
of change it is, which files it touches, whether tests come with it and in what
shape the whole thing should arrive, so it answers with what an average
developer might write for an average shop, which is precisely what you do not
have. Saying what should come back, the change itself, the tests next to it and
a short note on what was left out, already narrows the guess a great deal, and
saying who it is for narrows it further, since code that a colleague will review
tomorrow and a sketch you will throw away tonight are not written the same way.

The most underrated tool in this part is the example. The framework's glossary
calls it few-shot learning, teaching the AI by showing examples of the pattern
you want, and in a codebase the example is usually already there: a coupon that
follows the house style, a test written the way the team likes them, an error
message in the tone the product uses. Pointing to one of those does more than a
paragraph of adjectives, because it shows the AI what good looks like in your
world instead of asking it to imagine it. The rules belong here too, and they are
the part that only you know: one use per customer, never on top of the discount
for paying upfront, and nothing that makes checkout slower on the busiest day of
the year.

## Process description: how to get there

**Process description** is defining how the AI approaches your request, for
example by giving it step-by-step instructions to follow, and it is where the
decision you made in Delegation turns into words. You decided last time that the
edge cases would be thought through together before any code was written, so the
process you describe says exactly that: first list the edge cases you can see,
then wait for my answer, and only then write the code and the tests. That one
sentence turns a single long answer, which you would have to untangle on your
own, into a short conversation in which your knowledge enters at the moment it
is needed.

Process is also where context goes, which in software means showing the code
involved instead of describing it from memory, and where you can ask the AI to
reason before it answers. The glossary has names for both habits: chain-of-thought,
encouraging the AI to work through a problem step by step, and the think-first
approach, explicitly asking it to work through its reasoning before giving a
final answer. In practice they are as simple as "explain your plan before you
change anything", and they matter because a plan you can read in thirty seconds
is the cheapest place to catch a wrong assumption, long before it is buried in
two hundred lines of tidy code.

## Performance description: how it should work with you

**Performance description** is defining the AI's behaviour during the
collaboration, such as whether it should be concise or detailed, challenging or
supportive, and it is the part almost everyone skips. Without it the assistant
falls back on its defaults, which tend towards long answers, a polite tone and a
readiness to fill any gap with an assumption rather than a question. Those
defaults suit some moments and get in the way of others: on a Thursday evening
with little energy left you may want short answers, you certainly want to be
asked rather than guessed at when a rule is unclear, and you may well want to be
told when your own plan has a hole in it, which is something a supportive
assistant will rarely volunteer unless you ask it to.

The framework's glossary includes one more tool that lives on this branch in my
reading, the role or persona, specifying a particular character, level of
expertise or communication style for the AI to adopt. "Review this as the
developer who has maintained our payment system for five years" changes what the
AI pays attention to and how bluntly it says it, and that, too, is a way of
describing performance.

## The same prompt, before and after

<figure class="diagram fluency-map fluency-map--split">
  <a href="/img/ai-fluency/description-prompt.en.svg">
    <img src="/img/ai-fluency/description-prompt.en.svg" width="400" height="821" loading="lazy"
      alt="The checkout prompt before and after. Before: add the coupon rule to our checkout. After, in six parts. Product: add a Black Friday coupon to checkout, here are CouponService and the pricing code it touches. Product: one use per customer, it never stacks with the upfront-payment discount. Product: follow the WELCOME10 coupon, which already uses our pattern. Process: first list the edge cases and wait for my OK, then write the code and the tests. Process: explain your reasoning before each change. Performance: be brief; if a rule is unclear, ask me instead of guessing, and tell me if my plan has a hole.">
  </a>
  <figcaption>An example; the tags are my reading of the framework's three Description skills, AI Fluency Framework, CC BY-NC-SA 4.0.</figcaption>
</figure>

Put the three skills together and the one-liner from Thursday evening becomes
the prompt in the figure, which is longer but hardly clever. Half of it is
product, because that is where your knowledge of the business lives: what to
build, the code it touches, the rules nobody else knows and an existing coupon to
copy. Two lines are process, asking for the edge cases first and for the
reasoning before each change, and one line is performance, asking for brevity,
for questions instead of guesses and for honesty about the plan. None of it
requires a special vocabulary, and all of it was already in your head; the only
thing Description adds is the habit of getting it out of your head and into the
box before the AI starts filling the silence for you.

## The toolbox

<figure class="diagram fluency-map fluency-map--split">
  <a href="/img/ai-fluency/description-toolbox.en.svg">
    <img src="/img/ai-fluency/description-toolbox.en.svg" width="400" height="716" loading="lazy"
      alt="Mind map of prompting techniques, grouped by skill. Product description: output constraints, format, length and structure; few-shot examples, showing what good looks like. Process description: step by step, breaking the task into steps; think first, reasoning before the answer. Performance description: role or persona, who it should sound like.">
  </a>
  <figcaption>Terms from the AI Fluency Key Terminology Cheat Sheet, CC BY-NC-SA 4.0; the grouping by skill is my reading.</figcaption>
</figure>

The prompting techniques you read about online fit neatly onto the same three
branches, which is a good reason to learn the branches first and the techniques
second. The framework's glossary names five of them, and in my reading they
group like this: output constraints, stating the format, length and structure
you need, and few-shot examples both serve the product; step-by-step
instructions and the think-first approach both shape the process; and the role
or persona mostly shapes the performance. Seen this way, a technique is never an
end in itself but an answer to one of the questions on the map, which also tells
you when not to bother: a quick question needs no persona, and a throwaway sketch
needs no format.

## What the research sees

<figure class="diagram fluency-map fluency-map--split">
  <a href="/img/ai-fluency/description-index.en.svg">
    <img src="/img/ai-fluency/description-index.en.svg" width="400" height="720" loading="lazy"
      alt="Bar chart from The AI Fluency Index, share of 9,830 conversations on Claude.ai. Clarifies the goal 51.1%. Gives examples of good 41.1%. Specifies format 30.0%. Sets the interaction mode 30.0%. States tone and style 22.7%. Defines the audience 17.6%. With and without iteration: clarifies the goal 54.5% against 30.9%; gives examples 44.4% against 21.8%; specifies format 32.4% against 16.1%.">
  </a>
  <figcaption>Source: The AI Fluency Index, Anthropic, February 2026, a sample of conversations from January 2026. Grouping these behaviours as Description is my reading.</figcaption>
</figure>

Anthropic's AI Fluency Index, the study published in February 2026 that
classified fluency behaviours in 9,830 conversations on Claude.ai, gives a rare
look at how often people actually do these things, and the picture is uneven.
The behaviours I read as Description fall in a clear order: about half the
conversations clarified the goal before asking for help, 51.1%, about four in
ten gave an example of what good looks like, 41.1%, three in ten specified the
format they needed, and the same three in ten told the AI how they wanted it to
interact with them, which is the closest thing in the study to performance
description. Tone and style came up in 22.7% of conversations and the audience
in only 17.6%, so the further a skill sits from the product itself, the less
often people bother to describe it.

The second half of the figure is the more interesting one. In conversations
where people went back and forth refining the result, which was 85.7% of them,
every one of these description behaviours appeared far more often than in
conversations that stopped at the first answer: goal clarification at 54.5%
against 30.9%, examples at 44.4% against 21.8% and format at 32.4% against
16.1%. The study reports correlation, not cause, and I would not read more into
it than that, but it fits what most of us learn by doing, which is that people
who describe well tend to keep the conversation going, and people who keep it
going end up describing better.

The study also carries a warning. In conversations where the AI produced
something concrete, such as code or a document, people described more at the
start, yet they were less likely to notice missing context, check facts or
question the AI's reasoning afterwards, and the authors note that this
directiveness did not come with more evaluation. A well-described request, in
other words, can make the answer look finished, and that is exactly where the
next competency comes in.

## The loop that keeps it honest

<figure class="diagram fluency-map fluency-map--split">
  <a href="/img/ai-fluency/description-loop.en.svg">
    <img src="/img/ai-fluency/description-loop.en.svg" width="400" height="568" loading="lazy"
      alt="The Description–Discernment loop, four steps on a ring: describe the product, process and performance; the AI answers with a draft, a plan or code; discern whether it is right and how it got there; refine and describe again, better. In the middle: 85.7% of conversations went back and forth.">
  </a>
  <figcaption>The loop is from the AI Fluency Framework, CC BY-NC-SA 4.0; the share is from The AI Fluency Index, Anthropic, 2026.</figcaption>
</figure>

Episode 1 showed Description joined to Discernment in one of the framework's two
loops, the one that covers the moment-to-moment craft of working with AI. You
describe, the AI answers, you judge what came back and how it got there, and what
you learn from that judgement goes into the next description, so a prompt is
rarely right the first time and does not need to be. On Thursday evening the loop
might go like this: the AI lists the edge cases, you notice it has missed the
customer who opens two browser tabs and applies the coupon in both, and the next
description adds that case, which the AI would never have guessed and you would
never have remembered without seeing the list.

## Back to Thursday evening

Replay the evening one more time. The decision behind the request was made in
Delegation, so the prompt you type now says what you want back and points to the
code and the coupon to copy, asks for the edge cases before any code and for the
reasoning before each change, and tells the AI to be brief, to ask rather than
guess and to point out holes in your plan. It takes perhaps three minutes longer
to write than the one-liner, and it saves the weekend, not because the words are
magic but because the AI is no longer filling your silence with an average guess.
The same three questions, what should come back, how to get there and how to work
with me, apply just as well to a database migration, a code review or a technical
spec, and just as well outside code.

What Description cannot do on its own is tell you whether the answer is any good,
and the Index suggests that a well-described request makes that question easier
to forget. That is the subject of the next episode, on Discernment: how to judge
the product, the process and the performance that come back.

*Sources: Anthropic's [AI Fluency Framework](https://www-cdn.anthropic.com/b383cf6baddbfc72fdf8b0ed533a518e2872d531.pdf)
and [Key Terminology Cheat Sheet](https://www-cdn.anthropic.com/4396730ed190e691a3712cf2fd6bfe35509deca2.pdf),
© 2025 Rick Dakan, Joseph Feller and Anthropic, CC BY-NC-SA 4.0; the course
[AI Fluency: Framework & Foundations](https://anthropic.skilljar.com/ai-fluency-framework-foundations);
and [The AI Fluency Index](https://www.anthropic.com/research/AI-fluency-index)
(Swanson, Bent, Ludwig, Dakan and Feller, February 2026). This article is an
independent explainer, not an Anthropic publication.*
