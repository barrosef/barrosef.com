---
title: "The Culture You Can Install"
date: 2026-10-16T17:00:00-04:00
draft: false
translationKey: "foreman-culture"
categories: ["Technology"]
tags: ["ai-agents", "software-delivery", "engineering-culture", "foreman", "dop"]
description: "Every AI-first project began with the same explanation of who decides, who builds and who checks. foreman writes it down once and installs it in two steps."
---

Every project I have run with an AI agent at the keyboard began the same way,
and for a long time I did not notice that it did. Before the first line of code,
there was a conversation about how the work would happen: who decides what a
request really asks for, who writes the change, who looks at it with a
sceptical eye, when the agent should stop and ask instead of guessing, and what
"done" means to the person paying for it. I had that conversation with myself,
then with the agent, then again on the next project, and each time it came out a
little different, because it lived in whoever had done the previous one, and that
person was tired, or in a hurry, or had simply forgotten half of it.

The agent, meanwhile, did what agents do when the rules arrive late or
incomplete: it filled the gaps with its best guess. Sometimes the guess was fine.
Sometimes it reviewed its own work and approved it, which is not a review but the
same reasoning agreeing with itself; sometimes it ran a test by hand in a way
nobody could repeat; sometimes it asked me a question I had already answered in
another project, and sometimes it did not ask the one question that mattered. None
of this was the agent's fault. The way of working had never been written down,
so there was nothing for it to follow.

## Writing it down once

On a client platform, after months of this, the conversation finally became a
document, and the document turned out to have three layers that I had been
mixing together all along.

The first layer is the **rules**, written for any agent, in a file that names no
vendor and no model. It says, in plain sentences, that whoever decides does not
execute, that whoever executes touches only what the task names, that the plan
goes through someone whose job is to object before anyone starts building, that
the result is attacked afterwards by a team that did not write it, and that
there is exactly one human gate, which sits after the work is live and not
before. It also says the thing that made all the difference on a bad afternoon:
ask for nothing you can decide. A question to the human is an interruption, to
be spent only when the rules genuinely do not cover the case.

The second layer is the **roles**, four of them, written as contracts rather than
as programs. An architect, who reads the request, doubts it, holds it against the
code, writes what will change and why, and splits the work. A reviewer, who works
at the architect's own level, because a reviewer one notch below can only review
spelling, and whose success is measured in objections that changed the plan,
never in plans approved quickly. Executors, who receive a boundary and hand back
what they found, including the one line that says they ran into something they
were not asked to touch. And a quality team with a lead of its own, which decides
what the testing must cover and how large the attack may be, and which reports a
weakness even when it is not a defect of this particular piece of work. The roles
pull against each other on purpose, and when they disagree the architect decides
and writes down why, so that the same objection does not return a month later
with nobody able to say what happened to it.

The third layer is the one I had never separated out, and it is where the
culture meets the project: five **records** of facts a culture cannot know on
its own. Which codebases exist and how they relate. How work travels through
branches to a running environment, and what "delivered" means there. How the
application is brought up, taken down and tested. Where a request lives while it
is being worked on, and which event moves it from one state to the next. And how
quality is held, which layers of testing a change owes, and with which tools. The
rules said something uncomfortable about these five: if any of them is missing,
you stop. You do not start a request, you do not guess the convention, you do
not infer it from the code. You say which record is missing, and you wait.

That rule was the point. It was also the problem, for anyone new.

## Making it something you install

A culture that stops when a record is missing is a culture that, on a fresh
project, stops immediately. Writing the five records by hand took me the better
part of a week on the first platform, with the project's history in front of me.
Nobody adopting the way of working for the first time was going to do that, and
I did not want to explain it again myself. So the document became a tool, and
the tool is called **foreman**, after the architect's role: the one who decides
and does not execute. It is [public](https://github.com/barrosef/foreman), and
adopting it is two steps. The first installs it. The second, run inside any
project, does the rest.

What "the rest" means is the part I am proudest of, because it inverts the rule
without breaking it. foreman first reads the project, which it is allowed to do
as long as it only reads what the project tracks: it finds the pieces and how
they are stitched together, which branches exist and what the recent history says
about how the team works, the commands that start things and run tests, whether
the commit messages are in English or Portuguese, whether there is a place where
decisions are already recorded. Then it asks, and it asks as little as it can.
At most five questions, one per record, in plain language, each with the answer
it detected already marked as the recommended one, and the very first question
offers to accept every default at once. Then it writes the five records, filled
in, with every value either detected, answered or defaulted, and each record says
on its first page how it was filled, so that nobody later mistakes a default for
a decision somebody made about their project.

The agent that opens the project the next morning finds all five records in
place, and the rule that says "if any is missing, you stop" is satisfied without
anyone having been stopped. The project edits the records whenever it disagrees,
because they are plain files in its own codebase, and foreman never asks again.
Changing a record is editing a file.

### How foreman itself was built

I want to tell this part because foreman was built the way the culture says
software should be built, and the afternoon it took was the best argument I have
seen for the culture.

It started with a design document, and before I wrote a line of the tool, a
reader who had never seen the conversation was handed that document and asked
only one thing: what would you still need to know before you could build this?
Four questions came back, and three of them were real. One of them, about what
happens when the tool meets a project made of several codebases rather than one,
changed the design.

Then came a plan in which every piece arrived with its test first. The detection
of the project's shape, the interview, the writing of files into someone else's
project without ever overwriting a byte that was already there: each one existed
as a failing test before it existed as code, and the test was watched failing, so
that when it passed there was a reason to believe it. By the end there were a
hundred and ninety-five of those checks, and they run against four small
pretend projects built fresh each time, one empty, one ordinary, one made of
several pieces with the awkward details real projects have, and one that had
already been through the tool.

Then a reviewer who had seen none of it read the whole thing. It found one way
the tool would crash on the most common kind of laptop, and ten more defects
worth fixing, and every one of them was fixed the same afternoon, each with its
own test written first. I did not re-read my own work and call it reviewed; the
culture does not allow that, and it was right.

And then the first client found three more. Before a single file was written
into it, foreman read [DOP](/about/), the platform I am building, which has the
opposite shape from the project the culture was born in: six pieces instead of
one, three programming languages, two dozen architecture decisions already
recorded, and a different model entirely playing the reviewer. The reading found
a project that mentioned its own decision numbers in commit messages and was
mistaken for one that used a ticketing system; a project with a place for issues
that had never held one; and a top-level codebase that only ever moved pointers
and documentation, and was therefore not the kind of place where code changes,
which the tool had refused to believe. Three fixes, three tests, one more release,
and then the install, which asked me exactly one question, because I accepted
the defaults, and left the records I then spent half an hour refining by hand.

## A request, end to end

With the culture installed, this is what a request goes through, and where the
human appears.

<div class="path" role="img" aria-label="Seven steps: the human states the request; the architect reads and doubts it, writes the plan; the reviewer objects before any work; executors build within boundaries; the quality team attacks the result; delivery goes out through the project's tooling; the human sees it working and says done.">
  <div class="path-step path-step-human"><span class="path-n">1</span><span class="path-name">The request is stated</span><span class="path-who">by a human, with what and why</span></div>
  <div class="path-step"><span class="path-n">2</span><span class="path-name">The architect reads and doubts</span><span class="path-who">holds the request against the code, writes what changes and how it splits</span></div>
  <div class="path-step"><span class="path-n">3</span><span class="path-name">The reviewer objects</span><span class="path-who">before anyone builds; a fast approval is a failure</span></div>
  <div class="path-step"><span class="path-n">4</span><span class="path-name">Executors build within boundaries</span><span class="path-who">one task each; the unexpected is handed back, not resolved</span></div>
  <div class="path-step"><span class="path-n">5</span><span class="path-name">The quality team attacks</span><span class="path-who">a lead sizes the run; a red caused by the product stays red</span></div>
  <div class="path-step"><span class="path-n">6</span><span class="path-name">Delivery goes out through the tooling</span><span class="path-who">with the team's verdict attached</span></div>
  <div class="path-step path-step-human"><span class="path-n">7</span><span class="path-name">The human sees it working</span><span class="path-who">and says done; nothing else closes it</span></div>
</div>

Two of the seven steps are the human's, and they are the first and the last. In
between, the architect does not ask whether it may proceed; it announces what it
decided and why, on screen, so that a person reading over its shoulder can
redirect early if they want to, and otherwise it keeps going. The reviewer is not
the architect's assistant and does not approve by default. The executors do not
widen the task, however tempting the refactor two files over. The quality team
does not fix what it finds. And "done" does not mean the tests passed, which is
a precondition and not a delivery; it means the person who asked saw the thing
working where it is meant to run, and said so.

Each role also works at the level of capability and effort it deserves, which
the culture calls seniority and debit so that it never has to name a vendor: the
architect and the reviewer at the top, because a reviewer below the architect
reviews spelling; the executors lower, because a task with no judgment left in it
does not need judgment; the quality lead wherever the architect sets it, leaning
capable, because a lead that only runs what you specified finds nothing you did
not already know. The mechanism file, which is the one file that does name the
models, is the project's to edit, and on DOP the reviewer's row already points at
something other than the default.

## Tools, not discipline

There is one more principle in the rules, and it is the one that took me
longest to understand. *Governance is honoured through tooling, not through
discipline.*

Every project has a handful of operations that happen dozens of times a day and
must happen the same way every time: bringing the environment up and taking it
down, running the tests of one piece or all of them, moving the request from one
state to the next, opening the delivery. An agent will do each of these by hand
if you let it, and it will do them slightly differently each time, because that
is what doing things by hand means. Telling it to be careful does not help; it
was being careful. What helps is giving the project a tool with a verb for each
of those operations, writing in the environment record which verbs exist, and
stating one rule: when the tool has a verb for an action, the action does not
happen outside it. A missing verb is a gap to report, not an invitation to
improvise, and if the tool cannot bring the environment up, the work stops and
says so rather than finding another way.

On DOP this is now the next piece of work, and the culture itself is doing it.
The platform has an operational tool that was written for another client and is
being rebuilt to carry exactly the verbs the environment record names: up, down,
status, logs, test, reset, one piece at a time. The brief that starts that work
was written on the day the culture was installed, and it tells the architect
session what the records already decided, in which order the pieces come, which
seven things must be true for the work to be accepted, and the five things it
must not do, among them building anything the records do not name. The agent
will read it the way it reads any request: with doubt, and then with a plan
that someone else gets to object to first.

That is what I wanted from the beginning, without knowing how to say it. Not an
agent that is told to be careful, but a project that already knows how work is
done here, written down once, carried from project to project, and installed
rather than explained. The explanation finally stays.
