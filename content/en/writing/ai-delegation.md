---
title: "Before you type: Delegation, the first D of AI Fluency"
seoTitle: "AI delegation: what to hand over to AI, and what to keep"
date: 2026-11-10T11:00:00-04:00
draft: false
translationKey: "ai-fluency-delegation"
categories: ["Technology"]
tags: ["ai-fluency", "generative-ai"]
description: "Episode 2 of AI Fluency. Delegation, the decision made before the prompt: knowing the problem, knowing the tool, and splitting the work so each side does what it does best."
---

*Second episode of **AI Fluency**, a series that walks through the AI Fluency
Framework one competency at a time. [Episode 1](/writing/ai-fluency-mapped/) drew
the whole map; this one walks its first branch.*

---

Picture a Thursday evening with a feature due on Monday. The online store needs
a new coupon rule at checkout in time for Black Friday, and everything you need
to know about it is scattered across the ticket, a couple of chat threads, a
spreadsheet from finance and your notes from three meetings. The week has left
you with very little energy, so you open an AI assistant and type something like
"add the coupon rule to our checkout". The answer arrives in seconds and it looks
like code: a tidy function, a handful of tests, even comments. On a second look,
though, it calls a payment function your system has never had, it is written for
an older version of the library you use, and it lets the coupon stack with the
discount for paying upfront, which is exactly what finance said in the second
meeting must never happen. The tests pass only because they check what the code
does rather than what the business asked for, and a good part of your weekend
goes into pulling it apart.

The instinct at that point is to blame the prompt and to look for a better way
of asking, which is a real skill and the subject of the next episode. Yet the
trouble in that scene began a step earlier, before a single word was typed, at
the moment you handed over the whole job, including the parts only you could do.
The AI Fluency Framework, developed by Rick Dakan, Joseph Feller and Anthropic,
calls that earlier step **Delegation**: setting goals and deciding whether, when
and how to engage with AI, which in practice means deciding what work should be
done by people, what work should be done by AI and how to distribute it between
them. Of the four competencies on the map it is, in my reading, the one that
usually comes first and the one that is easiest to skip, because skipping it
feels like saving time.

## The branch, up close

<figure class="diagram fluency-map fluency-map--main">
  <a href="/img/ai-fluency/delegation-map.en.svg">
    <picture>
      <source media="(max-width: 1099px)" srcset="/img/ai-fluency/delegation-map-narrow.en.svg">
      <img src="/img/ai-fluency/delegation-map.en.svg" width="1200" height="770" loading="lazy"
        alt="Mind map of Delegation, the first competency of the AI Fluency Framework: deciding whether, when and how to bring AI in. Three branches. Problem awareness, your goal and the work before AI, with the questions: what does done look like, who is it for and what is at stake, what do I know that AI doesn't. Platform awareness, what this AI does well and its limits, with the questions: what is this tool good at, what can't it know or see, where might it make things up. Task delegation, splitting the work by strengths, with the questions: which parts need my judgement, which parts can AI do or draft, and automation, augmentation or agency.">
    </picture>
  </a>
  <figcaption>Based on the AI Fluency Framework © 2025 Rick Dakan, Joseph Feller and Anthropic, CC BY-NC-SA 4.0. The skills are the framework's and the one-line summaries condense its definitions; the questions around them are my reading. Shared under the same license. Tap or click to open it full size.</figcaption>
</figure>

The framework splits Delegation into three skills, and the map adds, around each
one, the questions I find myself asking when I practise it. The skills are the
framework's and the one-line summaries condense its definitions, while the
questions are mine, offered as a way in rather than as part of the official
text. Read from the upper left, round to the right and down, the branches go from
the work to the tool and then to the split between the two, which is also the
order in which the decisions tend to happen.

## Problem awareness: knowing what you are actually asking for

The framework defines **problem awareness** as clearly understanding your goals
and the nature of the work before involving AI. It sounds obvious until you
notice how easily it slips under pressure, because the goal in the checkout
scene was never "a coupon feature"; it was a Black Friday promotion that could
not eat into the margin, which meant a coupon that does not stack with the
upfront-payment discount, one use per customer, and a checkout that cannot get
slower on the busiest day of the year. Once the goal is put that way, the nature
of the work changes too, since a good part of it turns out to be pinning down
rules and edge cases that only the team knows, and very little of it is typing
code.

The questions on the map are a short way of getting there. What does done look
like, so that you would recognise it if you saw it, the way a good acceptance
criterion does? Who is it for, and what breaks if it goes wrong? And what do I
know that the AI doesn't, the history of the code, the decision taken in that
meeting, the rule nobody wrote down, which no system will guess on its own?
Anthropic's own research suggests this step is far from universal. In the AI
Fluency Index, a study published in February 2026 that classified fluency
behaviours in 9,830 conversations on Claude.ai, the behaviour I read as closest
to problem awareness, clarifying the goal before asking for help, appeared in
about half of them, 51.1%, which means that in the other half the goal was never
put into words before the request, much as it was not on that Thursday evening.

## Platform awareness: knowing the colleague you are briefing

The second skill, **platform awareness**, is understanding the capabilities and
limitations of different AI systems, and it asks for no deep technical
knowledge. It is closer to what you would want to know about a capable new
colleague on their first day on the team before giving them a task: what they
are good at, what they cannot possibly know yet and where they tend to bluff.
The framework's own glossary gives the vocabulary for the limits. A model has a
**knowledge cutoff**, a date after which it has no built-in knowledge of the
world, which is why it may write code for an older version of a library than the
one you use. It has a **context window**, a limit on how much information it can
consider at once, which varies from one model to the next. And it can
**hallucinate**, stating something plausible and confident that is simply
wrong, such as a function that sounds as if it ought to exist and doesn't.

Each of those limits translates directly into a delegation decision: the AI in
the checkout scene could not see your repository unless you showed it the code
involved, so it guessed at a payment function instead of using the real one;
it knew nothing of the three meetings, so it had no way of knowing the coupon
must not stack. Tools also differ from each other, since some can read your
whole project, run the tests or look up the documentation while others only see
what you paste into the chat, so the same task can be a good delegation to one
system and a poor one to another. Platform awareness is simply the habit of
asking, before you hand something over, whether this tool is the right one for
this part of the work.

## Task delegation: splitting the work by strengths

The third skill, **task delegation**, is where the first two meet: thoughtfully
distributing work between people and AI so as to use the strengths of each.
Anthropic's lesson on the subject adds a line I find useful, that effective
delegation requires both domain expertise and an understanding of what AI can
do. In my reading, that is why a developer who has spent years on the payment
system delegates that work better than one who joined last week, and why the
same experienced developer still needs to know the tool before the split can be
a good one.

<figure class="diagram fluency-map fluency-map--split">
  <a href="/img/ai-fluency/delegation-split.en.svg">
    <img src="/img/ai-fluency/delegation-split.en.svg" width="400" height="734" loading="lazy"
      alt="Mind map of one task, split: a new checkout rule in the centre and its six steps around it. One, decide what done means, the rule and its acceptance criteria: you. Two, point to the code involved and what the meetings decided: you. Three, think through the solution and the edge cases: together, augmentation. Four, write the code and the tests from the agreed plan: AI, automation. Five, review every line and run the tests: you. Six, approve it and ship it: you.">
  </a>
  <figcaption>An example of task delegation; the split is mine, not the framework's. The modes are from the AI Fluency Framework, CC BY-NC-SA 4.0.</figcaption>
</figure>

The figure replays the checkout rule with the task in the centre and the work
split into six steps around it, clockwise from the top, which is very close to
the exercise Anthropic's course gives its learners: take a project with several
steps, break it into tasks and plan which ones you will do yourself and which
ones you will do with AI. In my split, deciding what done means, the rule and its
acceptance criteria, stays with you, because it depends on what was agreed with
the business, and so does pointing to the code involved and to what the
meetings decided, because that lives in your repository and in your notes and
not in the model. Thinking through the solution and the edge cases is done
together, as a conversation. Writing the code and the tests from the agreed plan
goes to the AI, which is fast and tireless at exactly that. Reviewing every line
and running the tests comes back to you, and so, finally, does approving the
change and shipping it, since it goes to production with your name on it.
Nothing in that list is sophisticated, and that is the point: the same tool,
given the fourth step instead of the whole job, produces something you can
actually use.

## Choosing how, and choosing not to

The labels on the figure point to the last decision on the branch. The framework
describes three ways people and AI work together: **automation**, where the AI
carries out a specific task on your specific instructions; **augmentation**,
where you think together in a back-and-forth to which both contribute; and
**agency**, where you set the AI up to work on its own on your behalf. In my
reading, choosing among them is part of the "how" in "whether, when and how",
so it belongs squarely to Delegation, and the same piece of work can call for a
different mode at each step, as it does in the checkout rule. The AI Fluency
Index found that the most common expression of fluency it observed was
augmentative, treating the AI as a thought partner rather than handing work over
entirely. It also found that only about one conversation in ten, 10.1%, included
the user consulting the AI on the approach before asking it to execute, which in
my reading is perhaps the cheapest delegation question there is, much like
asking a colleague for the plan before you ask for the code.

The "whether" in that definition deserves its own moment, because Delegation
includes deciding to keep work. Some parts of a task carry judgement that is
yours to exercise, such as which business rule wins when two of them collide or
which design the team will have to live with for years; some carry
responsibility that cannot be passed on, such as what goes to production; and
some, for someone starting out above all, exist precisely so that you learn the
system by doing them, in which case handing them over defeats the purpose. A
good delegation leaves those with you on purpose, not by accident, and it is
often the parts you keep that make the parts you hand over worth having.

## The loop that brings you back

Episode 1 showed Delegation joined to Diligence in one of the framework's two
loops, which covers the strategic and ethical decisions about using AI. In my
reading, the loop closes because owning the result teaches you what to delegate
next time: the weekend spent hunting for a function that never existed is
exactly what makes you show the AI the real code, and keep the business rules
with you, on the next feature. Delegation is therefore not a decision made once
and filed away but one you revise each time a result comes back, and the fifth
episode, on Diligence, will walk the other half of that loop.

## Back to Thursday evening

Return to the checkout and replay the evening with the branch in mind. Before
opening the assistant, you spend a few minutes writing down what the rule is
really for and how you will know it works; you remember that the tool cannot see
your repository or your meetings, so you decide to show it the code involved and
to bring the rules yourself; you split the work, think the solution and the edge
cases through together, leave the first version of the code and the tests to
the AI and keep the review for yourself. The prompt you finally type is not
especially clever, yet it lands in a much better place, because the decision
behind it, made before you typed and called Delegation by the framework, was a
good one, and that decision works the same way for a database migration, a bug
fix, a code review or a technical spec, and just as well outside code.

What it does not tell you is how to say what you need once you have decided to
ask, and that is the subject of the next episode, on Description: how to describe
the product you want, the process the AI should follow and the way it should
work with you.

*Sources: Anthropic's [AI Fluency Framework](https://www-cdn.anthropic.com/b383cf6baddbfc72fdf8b0ed533a518e2872d531.pdf)
and [Key Terminology Cheat Sheet](https://www-cdn.anthropic.com/4396730ed190e691a3712cf2fd6bfe35509deca2.pdf),
© 2025 Rick Dakan, Joseph Feller and Anthropic, CC BY-NC-SA 4.0; the course
[AI Fluency: Framework & Foundations](https://anthropic.skilljar.com/ai-fluency-framework-foundations);
and [The AI Fluency Index](https://www.anthropic.com/research/AI-fluency-index)
(Swanson, Bent, Ludwig, Dakan and Feller, February 2026). This article is an
independent explainer, not an Anthropic publication.*
