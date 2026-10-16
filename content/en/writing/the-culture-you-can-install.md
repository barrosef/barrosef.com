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

<!-- fig:layers -->
<figure class="diagram"><svg viewBox="0 0 720 404" role="img" aria-label="Diagram of what foreman installs: a top band with three passes, detect, ask and write; a left zone with the culture, rules, four roles and the mechanism plus five agents; a right zone with the five records, each marked as detected, answered or default." xmlns="http://www.w3.org/2000/svg" font-family="IBM Plex Sans, system-ui, sans-serif" color="#16233a"><defs><marker id="h-ink" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1,1 L9,5 L1,9 z" fill="#16233a"/></marker><marker id="h-navy" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1,1 L9,5 L1,9 z" fill="#1d4e89"/></marker><marker id="h-muted" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1,1 L9,5 L1,9 z" fill="#5d6b7d"/></marker><marker id="h-gold" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1,1 L9,5 L1,9 z" fill="#b7791f"/></marker></defs><rect x="16" y="16" width="688" height="84" rx="10" fill="#eef2f7" stroke="#d5dde8" stroke-width="1"/><text x="32" y="38" text-anchor="start" font-size="12" font-weight="600" fill="#5d6b7d">the install, in three passes</text><rect x="32" y="40" width="196" height="48" rx="6" fill="#fff" stroke="#b9c5d4" stroke-width="1.2"/><text x="130.0" y="61.0" text-anchor="middle" font-size="13" font-weight="600" fill="#16233a">detects</text><text x="130.0" y="78.0" text-anchor="middle" font-size="10.5" font-weight="400" fill="#5d6b7d">reads only what the project tracks</text><rect x="262" y="40" width="196" height="48" rx="6" fill="#fff" stroke="#b9c5d4" stroke-width="1.2"/><text x="360.0" y="61.0" text-anchor="middle" font-size="13" font-weight="600" fill="#16233a">asks</text><text x="360.0" y="78.0" text-anchor="middle" font-size="10.5" font-weight="400" fill="#5d6b7d">five questions at most, answer marked</text><rect x="492" y="40" width="196" height="48" rx="6" fill="#fff" stroke="#b9c5d4" stroke-width="1.2"/><text x="590.0" y="61.0" text-anchor="middle" font-size="13" font-weight="600" fill="#16233a">writes</text><text x="590.0" y="78.0" text-anchor="middle" font-size="10.5" font-weight="400" fill="#5d6b7d">never over a byte that was there</text><path d="M 230,64 L 258,64" fill="none" stroke="#1d4e89" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" marker-end="url(#h-navy)"/><path d="M 460,64 L 488,64" fill="none" stroke="#1d4e89" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" marker-end="url(#h-navy)"/><rect x="16" y="118" width="330" height="266" rx="10" fill="#eef2f7" stroke="#d5dde8" stroke-width="1"/><text x="32" y="140" text-anchor="start" font-size="12" font-weight="600" fill="#5d6b7d">the culture · identical in every project</text><rect x="32" y="144" width="298" height="54" rx="6" fill="#fff" stroke="#b9c5d4" stroke-width="1.2"/><text x="181.0" y="162.0" text-anchor="middle" font-size="13" font-weight="600" fill="#16233a">the rules</text><text x="181.0" y="178.0" text-anchor="middle" font-size="10.5" font-weight="400" fill="#5d6b7d">principles, the cycle,</text><text x="181.0" y="192.0" text-anchor="middle" font-size="10.5" font-weight="400" fill="#5d6b7d">one human gate</text><rect x="32" y="206" width="298" height="54" rx="6" fill="#fff" stroke="#b9c5d4" stroke-width="1.2"/><text x="181.0" y="224.0" text-anchor="middle" font-size="13" font-weight="600" fill="#16233a">four roles as contracts</text><text x="181.0" y="240.0" text-anchor="middle" font-size="10.5" font-weight="400" fill="#5d6b7d">architect · reviewer ·</text><text x="181.0" y="254.0" text-anchor="middle" font-size="10.5" font-weight="400" fill="#5d6b7d">executors · quality team</text><rect x="32" y="268" width="298" height="54" rx="6" fill="#1d4e89" stroke="#173d6e" stroke-width="1.2"/><text x="181.0" y="286.0" text-anchor="middle" font-size="13" font-weight="600" fill="#fff">the mechanism</text><text x="181.0" y="302.0" text-anchor="middle" font-size="10.5" font-weight="400" fill="#cfe0f5">roles → agents ·</text><text x="181.0" y="316.0" text-anchor="middle" font-size="10.5" font-weight="400" fill="#cfe0f5">capability and effort per role</text><text x="181" y="344" text-anchor="middle" font-size="11" font-weight="400" fill="#5d6b7d">five agents, copied in, yours to tune</text><rect x="40" y="352" width="56" height="22" rx="11" fill="#fff" stroke="#b9c5d4" stroke-width="1"/><text x="68.0" y="367" text-anchor="middle" font-size="9.5" font-weight="400" fill="#16233a">reviewer</text><rect x="102" y="352" width="45" height="22" rx="11" fill="#fff" stroke="#b9c5d4" stroke-width="1"/><text x="124.5" y="367" text-anchor="middle" font-size="9.5" font-weight="400" fill="#16233a">reader</text><rect x="153" y="352" width="51" height="22" rx="11" fill="#fff" stroke="#b9c5d4" stroke-width="1"/><text x="178.5" y="367" text-anchor="middle" font-size="9.5" font-weight="400" fill="#16233a">builder</text><rect x="210" y="352" width="51" height="22" rx="11" fill="#fff" stroke="#b9c5d4" stroke-width="1"/><text x="235.5" y="367" text-anchor="middle" font-size="9.5" font-weight="400" fill="#16233a">qa lead</text><rect x="267" y="352" width="45" height="22" rx="11" fill="#fff" stroke="#b9c5d4" stroke-width="1"/><text x="289.5" y="367" text-anchor="middle" font-size="9.5" font-weight="400" fill="#16233a">tester</text><rect x="362" y="118" width="342" height="266" rx="10" fill="#eef2f7" stroke="#d5dde8" stroke-width="1"/><text x="378" y="140" text-anchor="start" font-size="12" font-weight="600" fill="#5d6b7d">the project · filled at install</text><rect x="378" y="144" width="310" height="38" rx="6" fill="#fff" stroke="#b9c5d4" stroke-width="1.2"/><text x="533.0" y="160.0" text-anchor="middle" font-size="12.5" font-weight="600" fill="#16233a">repositories</text><text x="533.0" y="177.0" text-anchor="middle" font-size="10.5" font-weight="400" fill="#5d6b7d">what exists and how it relates</text><rect x="378" y="186" width="310" height="38" rx="6" fill="#fff" stroke="#b9c5d4" stroke-width="1.2"/><text x="533.0" y="202.0" text-anchor="middle" font-size="12.5" font-weight="600" fill="#16233a">delivery</text><text x="533.0" y="219.0" text-anchor="middle" font-size="10.5" font-weight="400" fill="#5d6b7d">branches, pull requests, what DEV means</text><rect x="378" y="228" width="310" height="38" rx="6" fill="#fff" stroke="#b9c5d4" stroke-width="1.2"/><text x="533.0" y="244.0" text-anchor="middle" font-size="12.5" font-weight="600" fill="#16233a">environment</text><text x="533.0" y="261.0" text-anchor="middle" font-size="10.5" font-weight="400" fill="#5d6b7d">up, down, test</text><rect x="378" y="270" width="310" height="38" rx="6" fill="#fff" stroke="#b9c5d4" stroke-width="1.2"/><text x="533.0" y="286.0" text-anchor="middle" font-size="12.5" font-weight="600" fill="#16233a">demands</text><text x="533.0" y="303.0" text-anchor="middle" font-size="10.5" font-weight="400" fill="#5d6b7d">where a request lives, how it moves</text><rect x="378" y="312" width="310" height="38" rx="6" fill="#fff" stroke="#b9c5d4" stroke-width="1.2"/><text x="533.0" y="328.0" text-anchor="middle" font-size="12.5" font-weight="600" fill="#16233a">quality</text><text x="533.0" y="345.0" text-anchor="middle" font-size="10.5" font-weight="400" fill="#5d6b7d">test layers, the team, reports</text><text x="378" y="370" text-anchor="start" font-size="10.5" font-weight="400" fill="#5d6b7d">each value says how it was filled:</text><rect x="378" y="376" width="58" height="22" rx="11" fill="#1d4e89" stroke="#1d4e89" stroke-width="1"/><text x="407.0" y="391" text-anchor="middle" font-size="10" font-weight="400" fill="#fff">detected</text><rect x="442" y="376" width="58" height="22" rx="11" fill="#fff" stroke="#b9c5d4" stroke-width="1"/><text x="471.0" y="391" text-anchor="middle" font-size="10" font-weight="400" fill="#16233a">answered</text><rect x="506" y="376" width="53" height="22" rx="11" fill="#eef2f7" stroke="#b9c5d4" stroke-width="1"/><text x="532.5" y="391" text-anchor="middle" font-size="10" font-weight="400" fill="#5d6b7d">default</text><path d="M 590,92 L 590,112" fill="none" stroke="#1d4e89" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" marker-end="url(#h-navy)"/></svg><figcaption>What two steps leave behind. The culture on the left is the same in every project and names no vendor; the five records on the right are the project's own, filled at install from what was detected, answered or defaulted, and edited freely afterwards.</figcaption></figure>

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

<!-- fig:roles -->
<figure class="diagram"><svg viewBox="0 0 720 420" role="img" aria-label="Diagram of the cycle: a human states the request; the architect in the centre sends the plan to the reviewer and receives objections, dispatches a reader and a builder with bounded tasks, calls the quality lead who dispatches testers, delivers through the project's tooling into DEV, where the human sees it working and says done." xmlns="http://www.w3.org/2000/svg" font-family="IBM Plex Sans, system-ui, sans-serif" color="#16233a"><defs><marker id="h-ink" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1,1 L9,5 L1,9 z" fill="#16233a"/></marker><marker id="h-navy" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1,1 L9,5 L1,9 z" fill="#1d4e89"/></marker><marker id="h-muted" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1,1 L9,5 L1,9 z" fill="#5d6b7d"/></marker><marker id="h-gold" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1,1 L9,5 L1,9 z" fill="#b7791f"/></marker></defs><rect x="250" y="16" width="220" height="46" rx="6" fill="#1d4e89" stroke="#173d6e" stroke-width="1.2"/><text x="360.0" y="36.0" text-anchor="middle" font-size="13" font-weight="600" fill="#fff">the request</text><text x="360.0" y="53.0" text-anchor="middle" font-size="10.5" font-weight="400" fill="#cfe0f5">stated by a human: what and why</text><path d="M 360,64 L 360,150" fill="none" stroke="#1d4e89" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" marker-end="url(#h-navy)"/><text x="368" y="112" text-anchor="start" font-size="11" font-weight="600" fill="#1d4e89">1 read and doubt</text><rect x="240" y="154" width="240" height="78" rx="6" fill="#1d4e89" stroke="#173d6e" stroke-width="1.2"/><text x="360.0" y="184.0" text-anchor="middle" font-size="14" font-weight="600" fill="#fff">the architect</text><text x="360.0" y="200.0" text-anchor="middle" font-size="10.5" font-weight="400" fill="#cfe0f5">reads, doubts, specifies, splits, judges</text><text x="360.0" y="214.0" text-anchor="middle" font-size="10.5" font-weight="400" fill="#cfe0f5">the only one who sees the whole request</text><rect x="16" y="100" width="200" height="60" rx="6" fill="#fff" stroke="#b9c5d4" stroke-width="1.2"/><text x="116.0" y="121.0" text-anchor="middle" font-size="13" font-weight="600" fill="#16233a">the reviewer</text><text x="116.0" y="137.0" text-anchor="middle" font-size="10.5" font-weight="400" fill="#5d6b7d">objects before anything is built</text><text x="116.0" y="151.0" text-anchor="middle" font-size="10.5" font-weight="400" fill="#5d6b7d">at the architect's own level</text><path d="M 240,176 L 228,176 L 228,150 L 218,150" fill="none" stroke="#16233a" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" marker-end="url(#h-ink)"/><path d="M 216,116 L 232,116 L 232,200 L 240,200" fill="none" stroke="#5d6b7d" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="6 5" marker-end="url(#h-muted)"/><text x="150" y="90" text-anchor="middle" font-size="11" font-weight="400" fill="#5d6b7d">2 the plan</text><text x="140" y="176" text-anchor="middle" font-size="11" font-weight="400" fill="#5d6b7d">3 objections</text><rect x="16" y="270" width="232" height="124" rx="10" fill="#eef2f7" stroke="#d5dde8" stroke-width="1"/><text x="32" y="292" text-anchor="start" font-size="12" font-weight="600" fill="#5d6b7d">executors</text><rect x="32" y="296" width="200" height="42" rx="6" fill="#fff" stroke="#b9c5d4" stroke-width="1.2"/><text x="132.0" y="314.0" text-anchor="middle" font-size="12.5" font-weight="600" fill="#16233a">reader</text><text x="132.0" y="331.0" text-anchor="middle" font-size="10.5" font-weight="400" fill="#5d6b7d">one bounded question</text><rect x="32" y="344" width="200" height="42" rx="6" fill="#fff" stroke="#b9c5d4" stroke-width="1.2"/><text x="132.0" y="362.0" text-anchor="middle" font-size="12.5" font-weight="600" fill="#16233a">builder</text><text x="132.0" y="379.0" text-anchor="middle" font-size="10.5" font-weight="400" fill="#5d6b7d">one bounded change</text><path d="M 300,232 L 300,256 L 140,256 L 140,266" fill="none" stroke="#16233a" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" marker-end="url(#h-ink)"/><text x="150" y="250" text-anchor="start" font-size="11" font-weight="400" fill="#5d6b7d">4 a task with a boundary</text><rect x="476" y="84" width="228" height="150" rx="10" fill="#eef2f7" stroke="#d5dde8" stroke-width="1"/><text x="492" y="106" text-anchor="start" font-size="12" font-weight="600" fill="#5d6b7d">quality team</text><rect x="492" y="110" width="196" height="46" rx="6" fill="#fff" stroke="#b9c5d4" stroke-width="1.2"/><text x="590.0" y="130.0" text-anchor="middle" font-size="12.5" font-weight="600" fill="#16233a">the lead</text><text x="590.0" y="147.0" text-anchor="middle" font-size="10.5" font-weight="400" fill="#5d6b7d">sizes the attack, gives the verdict</text><rect x="492" y="176" width="60" height="40" rx="6" fill="#fff" stroke="#b9c5d4" stroke-width="1.2"/><text x="522.0" y="201.0" text-anchor="middle" font-size="11" font-weight="500" fill="#16233a">tester</text><path d="M 590,158 L 522,172" fill="none" stroke="#5d6b7d" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round" marker-end="url(#h-muted)"/><rect x="558" y="176" width="60" height="40" rx="6" fill="#fff" stroke="#b9c5d4" stroke-width="1.2"/><text x="588.0" y="201.0" text-anchor="middle" font-size="11" font-weight="500" fill="#16233a">tester</text><path d="M 590,158 L 588,172" fill="none" stroke="#5d6b7d" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round" marker-end="url(#h-muted)"/><rect x="624" y="176" width="60" height="40" rx="6" fill="#fff" stroke="#b9c5d4" stroke-width="1.2"/><text x="654.0" y="201.0" text-anchor="middle" font-size="11" font-weight="500" fill="#16233a">tester</text><path d="M 590,158 L 654,172" fill="none" stroke="#5d6b7d" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round" marker-end="url(#h-muted)"/><path d="M 480,176 L 468,176 L 468,100 L 472,100" fill="none" stroke="#16233a" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" marker-end="url(#h-ink)"/><text x="468" y="92" text-anchor="end" font-size="11" font-weight="400" fill="#5d6b7d">5 attack</text><rect x="300" y="300" width="190" height="50" rx="6" fill="#fff" stroke="#1d4e89" stroke-width="1.2"/><text x="395.0" y="322.0" text-anchor="middle" font-size="12.5" font-weight="600" fill="#16233a">the project's tooling</text><text x="395.0" y="339.0" text-anchor="middle" font-size="10.5" font-weight="400" fill="#5d6b7d">delivery, with the verdict attached</text><path d="M 420,232 L 420,270 L 395,270 L 395,296" fill="none" stroke="#1d4e89" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" marker-end="url(#h-navy)"/><text x="428" y="262" text-anchor="start" font-size="11" font-weight="600" fill="#1d4e89">6 deliver</text><rect x="526" y="300" width="90" height="50" rx="6" fill="#fff" stroke="#b9c5d4" stroke-width="1.2"/><text x="571.0" y="322.0" text-anchor="middle" font-size="13" font-weight="600" fill="#16233a">DEV</text><text x="571.0" y="339.0" text-anchor="middle" font-size="10.5" font-weight="400" fill="#5d6b7d">where it runs</text><path d="M 490,325 L 522,325" fill="none" stroke="#1d4e89" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" marker-end="url(#h-navy)"/><rect x="526" y="362" width="178" height="44" rx="6" fill="#1d4e89" stroke="#173d6e" stroke-width="1.2"/><text x="615.0" y="381.0" text-anchor="middle" font-size="12.5" font-weight="600" fill="#fff">the human</text><text x="615.0" y="398.0" text-anchor="middle" font-size="10.5" font-weight="400" fill="#cfe0f5">sees it working · says done</text><path d="M 571,350 L 571,358" fill="none" stroke="#1d4e89" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" marker-end="url(#h-navy)"/><text x="624" y="358" text-anchor="start" font-size="11" font-weight="600" fill="#1d4e89">7 · 8</text></svg><figcaption>The four roles around one request. The human states it and, at the end, says it is done; nothing in between waits for permission. The reviewer objects before any work, the executors never widen a task, the quality team never fixes what it finds, and delivery goes out through the project's own tooling.</figcaption></figure>
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

<!-- fig:tooling -->
<figure class="diagram"><svg viewBox="0 0 720 376" role="img" aria-label="Diagram of the culture meeting the tooling: the roles send commands to the project's tool, which alone acts on the local environment, on delivery and on the request's states; delivery reaches DEV, where the human sees the work and says done. Each target is named by one record." xmlns="http://www.w3.org/2000/svg" font-family="IBM Plex Sans, system-ui, sans-serif" color="#16233a"><defs><marker id="h-ink" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1,1 L9,5 L1,9 z" fill="#16233a"/></marker><marker id="h-navy" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1,1 L9,5 L1,9 z" fill="#1d4e89"/></marker><marker id="h-muted" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1,1 L9,5 L1,9 z" fill="#5d6b7d"/></marker><marker id="h-gold" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1,1 L9,5 L1,9 z" fill="#b7791f"/></marker></defs><rect x="16" y="96" width="190" height="180" rx="10" fill="#eef2f7" stroke="#d5dde8" stroke-width="1"/><text x="32" y="118" text-anchor="start" font-size="12" font-weight="600" fill="#5d6b7d">the roles</text><rect x="32" y="122" width="158" height="42" rx="6" fill="#fff" stroke="#b9c5d4" stroke-width="1.2"/><text x="111.0" y="140.0" text-anchor="middle" font-size="12.5" font-weight="600" fill="#16233a">architect</text><text x="111.0" y="157.0" text-anchor="middle" font-size="10.5" font-weight="400" fill="#5d6b7d">decides, delivers</text><rect x="32" y="172" width="158" height="42" rx="6" fill="#fff" stroke="#b9c5d4" stroke-width="1.2"/><text x="111.0" y="190.0" text-anchor="middle" font-size="12.5" font-weight="600" fill="#16233a">builders</text><text x="111.0" y="207.0" text-anchor="middle" font-size="10.5" font-weight="400" fill="#5d6b7d">change code</text><rect x="32" y="222" width="158" height="42" rx="6" fill="#fff" stroke="#b9c5d4" stroke-width="1.2"/><text x="111.0" y="240.0" text-anchor="middle" font-size="12.5" font-weight="600" fill="#16233a">quality team</text><text x="111.0" y="257.0" text-anchor="middle" font-size="10.5" font-weight="400" fill="#5d6b7d">runs the attack</text><rect x="258" y="104" width="204" height="150" rx="8" fill="#1d4e89" stroke="#173d6e" stroke-width="1.2"/><text x="360" y="132" text-anchor="middle" font-size="14" font-weight="600" fill="#fff">the project's tool</text><text x="360" y="150" text-anchor="middle" font-size="10.5" font-weight="400" fill="#cfe0f5">one verb per action</text><line x1="276" y1="162" x2="444" y2="162" stroke="#5b8fd6" stroke-width="1"/><text x="360" y="184" text-anchor="middle" font-size="11.5" font-weight="400" fill="#fff" font-family="IBM Plex Mono, ui-monospace, monospace">up · down · test · logs</text><text x="360" y="206" text-anchor="middle" font-size="11.5" font-weight="400" fill="#fff" font-family="IBM Plex Mono, ui-monospace, monospace">branch · deliver</text><text x="360" y="228" text-anchor="middle" font-size="11.5" font-weight="400" fill="#fff" font-family="IBM Plex Mono, ui-monospace, monospace">move the request</text><path d="M 206,186 L 254,186" fill="none" stroke="#16233a" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" marker-end="url(#h-ink)"/><text x="230" y="178" text-anchor="middle" font-size="11" font-weight="400" fill="#5d6b7d">commands</text><rect x="258" y="292" width="204" height="46" rx="6" fill="#fff" stroke="#b9c5d4" stroke-width="1.2"/><text x="360.0" y="312.0" text-anchor="middle" font-size="12.5" font-weight="600" fill="#16233a">the local environment</text><text x="360.0" y="329.0" text-anchor="middle" font-size="10.5" font-weight="400" fill="#5d6b7d">up, down, test, reset</text><path d="M 360,254 L 360,288" fill="none" stroke="#1d4e89" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" marker-end="url(#h-navy)"/><text x="372" y="276" text-anchor="start" font-size="10" font-weight="600" fill="#b7791f">environment record</text><rect x="510" y="24" width="194" height="50" rx="6" fill="#fff" stroke="#b9c5d4" stroke-width="1.2"/><text x="607.0" y="46.0" text-anchor="middle" font-size="12.5" font-weight="600" fill="#16233a">delivery</text><text x="607.0" y="63.0" text-anchor="middle" font-size="10.5" font-weight="400" fill="#5d6b7d">branches, pull requests, DEV</text><path d="M 462,130 L 486,130 L 486,49 L 506,49" fill="none" stroke="#1d4e89" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" marker-end="url(#h-navy)"/><text x="606" y="88" text-anchor="middle" font-size="10" font-weight="600" fill="#b7791f">delivery record</text><rect x="510" y="128" width="194" height="50" rx="6" fill="#fff" stroke="#b9c5d4" stroke-width="1.2"/><text x="607.0" y="150.0" text-anchor="middle" font-size="12.5" font-weight="600" fill="#16233a">the request</text><text x="607.0" y="167.0" text-anchor="middle" font-size="10.5" font-weight="400" fill="#5d6b7d">states move on delivery events</text><path d="M 462,170 L 486,170 L 486,153 L 506,153" fill="none" stroke="#1d4e89" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" marker-end="url(#h-navy)"/><text x="606" y="192" text-anchor="middle" font-size="10" font-weight="600" fill="#b7791f">demands record</text><rect x="510" y="228" width="194" height="52" rx="6" fill="#1d4e89" stroke="#173d6e" stroke-width="1.2"/><text x="607.0" y="251.0" text-anchor="middle" font-size="12.5" font-weight="600" fill="#fff">the human</text><text x="607.0" y="268.0" text-anchor="middle" font-size="10.5" font-weight="400" fill="#cfe0f5">sees it working in DEV · says done</text><path d="M 690,76 L 690,224" fill="none" stroke="#1d4e89" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="6 5" marker-end="url(#h-navy)"/><text x="360" y="362" text-anchor="middle" font-size="11" font-weight="400" fill="#5d6b7d">a missing verb is a gap to report, not a reason to improvise</text></svg><figcaption>Governance through tooling, not discipline. Every repetitive operation is a verb of a tool the project owns; the records say which verbs exist and what each one touches. When the tool has a verb for an action, the action never happens by hand.</figcaption></figure>

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
