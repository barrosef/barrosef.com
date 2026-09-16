---
title: "When is an AI agent's work done?"
date: 2026-09-16T17:00:00-04:00
draft: false
translationKey: "when-is-an-agents-work-done"
categories: ["Technology"]
tags: ["dop", "ai-agents", "software-delivery", "architecture-decisions"]
description: "An agent opens a pull request in twenty minutes; a person takes an hour to review it. DOP's answer: no green, no PR — and green has to be earned on a commit, not a dirty tree."
---

An agent opens a pull request in twenty minutes. A person takes an hour to
review it properly. Put five agents on five demands and the bottleneck is no
longer writing the code — it is the reviewer's desk. Parallelism that stops
there only moves the queue.

[DOP](/about/) is a platform I am building where a developer and
an agent run a demand end to end. Two of its architecture decisions answer the
question in the title, and the answer is the same in both: **no green, no
PR** — and green has to be earned honestly.

## The path from spec to main

<div class="path" role="img" aria-label="Seven steps: executable acceptance in the spec; the agent iterates to green; a runner builds the commit from source; a critic reviews diff against spec; the PR carries the evidence; the merge queue re-verifies against today's main; the human decides.">
  <div class="path-step"><span class="path-n">1</span><span class="path-name">Acceptance is born in the spec</span><span class="path-who">executable, or it is a wish</span></div>
  <div class="path-step"><span class="path-n">2</span><span class="path-name">The agent iterates to green</span><span class="path-who">a stuck failure becomes a question, never a broken PR</span></div>
  <div class="path-step"><span class="path-n">3</span><span class="path-name">A runner builds the commit from source</span><span class="path-who">not the agent's working tree</span></div>
  <div class="path-step"><span class="path-n">4</span><span class="path-name">A critic reviews diff against spec</span><span class="path-who">clean context, no memory of writing it</span></div>
  <div class="path-step"><span class="path-n">5</span><span class="path-name">The PR carries the evidence</span><span class="path-who">results, runs, verdict, trace</span></div>
  <div class="path-step"><span class="path-n">6</span><span class="path-name">The merge queue re-verifies</span><span class="path-who">against today's main, one at a time</span></div>
  <div class="path-step path-step-human"><span class="path-n">7</span><span class="path-name">The human decides</span><span class="path-who">the exception, not the rule</span></div>
</div>

## Four rules before anyone is called

**Acceptance is executable.** Every demand carries criteria a machine can
verify — test suites, checks derived from the spec. A criterion that does not
execute is not a criterion; it is a wish, and wishes are what reviewers end up
checking by hand.

**The agent iterates to green.** No PR opens with acceptance failing. When a
failure persists, it turns into a block with a question for the human, in the
attention box. A broken PR is never the way to ask for help.

**A critic reviews before the human.** An independent instance, with a clean
context and no history of having written the code, receives diff, spec and
evidence and issues a verdict. It is the first defence against rubber-stamping
— the reviewer who has read four green PRs today and is about to approve the
fifth on trust.

**The PR carries its evidence.** Acceptance results, test runs, the critic's
verdict, links to the trace. The human reviews the exception, not the rule.

## Why the test cannot run where the agent works

The agent works in a sandbox: its own microVM, its own working tree, everything
it installed along the way. The obvious place to run the tests is right there.
DOP refuses, and the refusal is written into the domain: a verification run
must name the commit it ran on, because *evidence that does not say which code
it ran on is not evidence*.

A test inside the sandbox runs against a dirty tree — which is no commit at
all. So the verification happens in a **runner**: an ephemeral environment that
starts from nothing, pulls the commit, builds the application from source and
starts it. No image of the project is ever built, pushed or deployed — the
slow part was never the build but the `build → push → pull` trip around a
registry. Dependencies such as a database are pulled as published images.
When the run ends, the runner dies.

The gain is honesty by construction: the green speaks about a commit because
it ran in an environment built from that commit — the same one that will be
merged.

## Who answers which question

| The question | Who answers it | Where |
|---|---|---|
| Does it do what the spec says? | The tests | In the runner, on the commit |
| Is the diff what the spec asked for, and nothing else? | The critic | A clean context |
| Is it still green against today's `main`? | The merge queue | A re-run after rebase |
| Should it merge? | The human | The PR, with the evidence |

## After green: the queue

Three demands run in parallel and each opens a green PR — each tested against
the `main` of the moment its branch was born. The first merge invalidates the
other two. At best a text conflict; at worst a silent semantic break, where
one PR removes the check the other assumed. A PR's CI does not see it.
Production does.

So a green PR does not merge; it joins a **queue per repository**. The queue
reapplies each PR on top of the current `main`, re-runs the verification and
merges one at a time. A conflict is the demand's agent's task first; only a
failed resolution reaches the human, with the conflict's context attached.
And the project's orchestrator watches which active demands touch the same
files, so the overlap is flagged before the PR, not after.

## What this buys

| What the human used to do | What the human does now |
|---|---|
| Run the tests, or trust that the agent did | Read a result that names the commit |
| Read the whole diff to see if it matches the ask | Read the critic's verdict and its reasons |
| Guess whether it still merges cleanly | Know it was re-verified on today's `main` |
| Review everything | Review the exceptions |

DOP is under construction; these are decisions, and decisions are cheaper to
argue with than code. The two that this article rests on are public:
[ADR-0007, no green, no PR](https://github.com/barrosef/dop/blob/main/docs/adr/0007-no-green-no-pr.md)
and [ADR-0030, verification builds from source](https://github.com/barrosef/dop/blob/main/docs/adr/0030-verification-runs-from-source.md).
