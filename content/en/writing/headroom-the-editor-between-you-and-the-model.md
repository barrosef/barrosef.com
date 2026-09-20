---
title: "Headroom: the editor between you and the model"
date: 2026-09-20T16:30:00-04:00
draft: false
translationKey: "headroom-editor"
categories: ["Technology"]
tags: ["claude-code", "headroom", "ai-assisted-development", "tooling", "cost"]
description: "Every request to a coding agent re-sends the whole conversation. Headroom is a local proxy that edits it on the way out. What it promises, how to set it up on Linux, macOS and Windows, and the rules of a test that starts tomorrow on real projects."
---

Picture a courier who carries a dossier between you and a specialist. Every
time you add a page, he walks over and reads the specialist the entire file
from page one — the new page and the four hundred before it — because the
specialist keeps nothing between visits. The specialist charges by the word.

That is a conversation with a language model. It has no memory: each request
carries everything said so far, and the bill counts all of it, every time. In
one real project I looked at last week, thirty days of Claude Code sessions
sent **3.6 billion tokens** of input to the API. Ninety-eight percent were
served from the provider's cache, at a tenth of the price. The average request
still carried **half a million tokens** of context — the dossier, read aloud
again.

Headroom proposes to put an editor at the door.

## What the editor is

[Headroom](https://github.com/headroomlabs-ai/headroom) is an open-source
(Apache 2.0) proxy that runs on your own machine. You point the agent at
`http://127.0.0.1:8787` instead of the API; the proxy reads each request,
edits it, and forwards the result. Nothing leaves your computer except what
already would have. It speaks the Anthropic, OpenAI and Gemini wire formats,
so the same process serves Claude Code, Codex, Cursor, Aider and a dozen
others.

For Claude Code specifically, three pieces arrive together:

- **the proxy**, the editor itself;
- **a plugin**, two hooks that check at session start (and before every
  shell command) that the proxy is alive, and start it if it is not;
- **an MCP server**, three tools the model can call: `headroom_compress`,
  `headroom_stats`, and the one that matters, `headroom_retrieve`.

## What it does to the dossier

<figure class="diagram">
<svg viewBox="0 0 720 330" role="img" aria-label="Claude Code sends the whole conversation to a local Headroom proxy; inside it four stages run in order: content router, compressors, cache aligner, tool-schema deferral; the edited request goes on to the Anthropic API. Below the proxy a CCR vault keeps every original; a retrieve arrow returns to Claude Code through the MCP server." xmlns="http://www.w3.org/2000/svg" font-family="IBM Plex Sans, system-ui, sans-serif" color="#16233a"><defs><marker id="hd-ink" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1,1 L9,5 L1,9 z" fill="#16233a"/></marker><marker id="hd-navy" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1,1 L9,5 L1,9 z" fill="#1d4e89"/></marker><marker id="hd-muted" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1,1 L9,5 L1,9 z" fill="#5d6b7d"/></marker></defs><rect x="16" y="92" width="118" height="76" rx="10" fill="#eef2f7" stroke="#d5dde8"/><text x="75" y="124" text-anchor="middle" font-size="14" font-weight="600" fill="#16233a">Claude Code</text><text x="75" y="143" text-anchor="middle" font-size="11" fill="#5d6b7d">the courier</text><line x1="134" y1="130" x2="176" y2="130" stroke="#16233a" stroke-width="1.5" marker-end="url(#hd-ink)"/><text x="155" y="147" text-anchor="middle" font-size="10.5" fill="#5d6b7d">whole</text><text x="155" y="159" text-anchor="middle" font-size="10.5" fill="#5d6b7d">dossier</text><rect x="178" y="48" width="376" height="164" rx="12" fill="#1d4e89" stroke="#173d6e" stroke-width="1.5"/><text x="366" y="72" text-anchor="middle" font-size="14.5" font-weight="600" fill="#fff">Headroom proxy · 127.0.0.1:8787</text><text x="366" y="88" text-anchor="middle" font-size="11" fill="#cfe0f5">the editor</text><g font-size="11.5" fill="#16233a"><rect x="192" y="104" width="82" height="66" rx="8" fill="#eef2f7"/><text x="233" y="130" text-anchor="middle" font-weight="600">router</text><text x="233" y="146" text-anchor="middle" font-size="10" fill="#5d6b7d">what is this</text><text x="233" y="159" text-anchor="middle" font-size="10" fill="#5d6b7d">block?</text><rect x="284" y="104" width="82" height="66" rx="8" fill="#eef2f7"/><text x="325" y="130" text-anchor="middle" font-weight="600">compress</text><text x="325" y="146" text-anchor="middle" font-size="10" fill="#5d6b7d">JSON · logs</text><text x="325" y="159" text-anchor="middle" font-size="10" fill="#5d6b7d">code · prose</text><rect x="376" y="104" width="82" height="66" rx="8" fill="#eef2f7"/><text x="417" y="130" text-anchor="middle" font-weight="600">cache</text><text x="417" y="146" text-anchor="middle" font-size="10" fill="#5d6b7d">freeze what</text><text x="417" y="159" text-anchor="middle" font-size="10" fill="#5d6b7d">is memorized</text><rect x="468" y="104" width="72" height="66" rx="8" fill="#eef2f7"/><text x="504" y="130" text-anchor="middle" font-weight="600">tools</text><text x="504" y="146" text-anchor="middle" font-size="10" fill="#5d6b7d">schemas</text><text x="504" y="159" text-anchor="middle" font-size="10" fill="#5d6b7d">on demand</text></g><line x1="274" y1="137" x2="284" y2="137" stroke="#cfe0f5" stroke-width="1.5"/><line x1="366" y1="137" x2="376" y2="137" stroke="#cfe0f5" stroke-width="1.5"/><line x1="458" y1="137" x2="468" y2="137" stroke="#cfe0f5" stroke-width="1.5"/><text x="366" y="196" text-anchor="middle" font-size="10.5" fill="#cfe0f5">every lossy cut leaves a marker  ‹‹ccr:hash››</text><line x1="554" y1="130" x2="596" y2="130" stroke="#16233a" stroke-width="1.5" marker-end="url(#hd-ink)"/><text x="575" y="118" text-anchor="middle" font-size="10.5" fill="#5d6b7d">edited</text><rect x="598" y="92" width="106" height="76" rx="10" fill="#eef2f7" stroke="#d5dde8"/><text x="651" y="124" text-anchor="middle" font-size="14" font-weight="600" fill="#16233a">Anthropic</text><text x="651" y="143" text-anchor="middle" font-size="11" fill="#5d6b7d">API · the model</text><rect x="284" y="244" width="164" height="60" rx="10" fill="#fff" stroke="#1d4e89" stroke-width="1.5" stroke-dasharray="5 3"/><text x="366" y="268" text-anchor="middle" font-size="13" font-weight="600" fill="#1d4e89">CCR vault</text><text x="366" y="286" text-anchor="middle" font-size="10.5" fill="#5d6b7d">every original, local SQLite</text><line x1="366" y1="212" x2="366" y2="242" stroke="#1d4e89" stroke-width="1.5" marker-end="url(#hd-navy)"/><text x="378" y="232" text-anchor="start" font-size="10.5" fill="#1d4e89">store</text><path d="M284,274 L75,274 L75,170" fill="none" stroke="#5d6b7d" stroke-width="1.5" stroke-dasharray="4 3" marker-end="url(#hd-muted)"/><text x="180" y="266" text-anchor="middle" font-size="10.5" fill="#5d6b7d">headroom_retrieve (MCP)</text><text x="180" y="290" text-anchor="middle" font-size="10.5" fill="#5d6b7d">when the model needs the original</text></svg>
<figcaption>The request path with Headroom in place. Four stages edit the conversation; every lossy cut is stored in the CCR vault and can be recalled by the model through the MCP server.</figcaption>
</figure>

Four moves, in order.

**It reads before it cuts.** A content router classifies every block of the
conversation — a tool's output, a log, a JSON payload, a source file, your own
prose — and picks a compressor to match. JSON gets a structural crusher that
keeps the shape and drops the repetition. Logs and tables get format-native,
lossless compaction. Code goes through an AST-aware pass that keeps
signatures and drops bodies the model already saw. Prose goes to a small
trained model that keeps the sentences that carry weight. Blocks that appear
twice across turns are sent once.

**Every cut leaves a receipt.** This is the part that makes the rest
acceptable. When a compressor drops something, it stores the original in a
local SQLite vault and leaves a marker in its place: `<<ccr:hash>>`. If the
model later needs what was cut, it calls `headroom_retrieve` with the hash
and gets the original back. Headroom calls this CCR — compress, cache,
retrieve. The count of retrievals is the alarm bell: if it grows, the editor
is cutting things the specialist actually needed.

**It never rewrites a page the specialist has memorized.** Providers cache the
prefix of a conversation and charge a tenth for the part they already hold.
An editor who reorders old pages breaks that cache and costs more than he
saves. Headroom tracks which prefix the provider has seen and freezes it.

**It keeps the tool catalogue at the door.** A Claude Code session with a few
MCP servers can carry hundreds of tool definitions — schemas the model reads
on every request and uses on almost none. With tool search on, only the
names travel; a schema is fetched when the model reaches for that tool. This
is not Headroom's invention — it is a Claude Code feature — but the proxy
insists on it, for a reason worth knowing: the moment you set a custom
`ANTHROPIC_BASE_URL`, Claude Code stops deferring schemas unless
`ENABLE_TOOL_SEARCH=true` is set as well. Route through any proxy without
that variable and your context fills with catalogue.

## Two modes, one tension

The editor can be timid or bold.

In **cache mode**, the default, he touches only the newest turn. Every
earlier page stays byte-for-byte as the provider cached it. Safe, cheap,
and — by design — small: most of a long conversation is old pages, and old
pages are off limits.

In **token mode**, he may go back and rewrite earlier turns. The dossier gets
shorter; the provider's cache for that request is broken and rebuilt. You
trade a one-time cache miss for a permanently smaller file. Headroom's own
estimate is that this stretches a session by a quarter to a third before the
context fills.

I learned the difference the honest way. For four days the proxy ran on a
real project in cache mode, by accident — a process started by hand had
ignored the mode I had configured. Just over 700 million tokens went through
it. The message compressor removed 1.7 million of them: a quarter of one
percent. The dashboard cheerfully reported thousands of dollars in "cache
savings", which were the provider's cache, which predates the proxy and owes
it nothing. The only layer that pulled real weight was the tool catalogue:
29.6 million schema tokens kept out of the context window.

A quarter of one percent is not a verdict on Headroom. It is a verdict on
running it in the wrong mode and trusting a dashboard. So the test restarts
tomorrow, in token mode, with rules written down first.

## Setting it up as I did today

The CLI installs the same way everywhere; a Python 3.13 tool in its own
environment:

{{< snippet file="headroom-editor/install.sh" lang="bash" >}}

Step 2 is the portable route: `headroom install apply` creates a proxy that
survives reboots and, in the same breath, applies the guardrails of the test.
On Linux it becomes a systemd user service; on macOS a launchd agent; on
Windows a Task Scheduler entry (the tool converts the service preset for you).
Step 3 writes `ANTHROPIC_BASE_URL` and `ENABLE_TOOL_SEARCH` into the project's
`.claude/settings.local.json`, together with the hooks that keep the proxy
alive. `headroom doctor` then tells you, in one table, whether the proxy is up,
whether Claude is actually routed, and whether your shell is bypassing it.

Under the hood, on Linux, those are three small files, and I prefer to own
them. The settings live in one place:

{{< snippet file="headroom-editor/proxy.env" lang="ini" >}}

The service reads them and restarts the proxy if it ever dies:

{{< snippet file="headroom-editor/headroom.service" lang="ini" >}}

And a wrapper starts Claude through the proxy. I keep plain `claude`
untouched on purpose — it is the control group:

{{< snippet file="headroom-editor/clh" lang="bash" >}}

The Windows twin is a PowerShell script on your `PATH`; the proxy is kept
alive by the scheduled task from step 2:

{{< snippet file="headroom-editor/clh.ps1" lang="powershell" >}}

If you would rather not use a wrapper, this is what `headroom init claude`
writes into the project — the same two variables, plus the hook:

{{< snippet file="headroom-editor/settings.local.json" lang="json" >}}

A note on `--dangerously-skip-permissions`: that flag is my choice for my
own machine, where the agent works inside git repositories I can restore.
Leave it out if that is not your situation.

## The rules of the test

Two principles, agreed before the first request goes through.

**Save the most, lose the least — and know what you lost.** Compression with
loss is still loss; the claim that nothing is ever affected would be
dishonest. What the test demands is that every loss be *acceptable* (it does
not change the outcome of the work), *predictable* (the rules of what is never
cut are known in advance), and *auditable* (what was cut can be counted and
recalled).

**Let the evidence decide.** Before and after are measured from the same
source, and the rule for keeping, deepening or abandoning the setup is written
before the data comes in. The chart decides, not the impression.

In practice, the guardrails look like this:

| Guardrail | Why |
|---|---|
| **Bold editing**<br>`HEADROOM_MODE=token` | The lever that was never tested. |
| **Files are sacred**<br>`HEADROOM_PROTECT_TOOL_RESULTS=Read,Edit,Write` | Whatever the agent read or wrote is never lossy-compressed; it never edits from a summary. |
| **Shorter catalogue**<br>`HEADROOM_TOOL_DESC_MAX_CHARS=200` | Tool descriptions truncated to their first sentence — cheap and predictable. |
| **Conservative prose**<br>`HEADROOM_TARGET_RATIO` unset | The prose compressor keeps its own cautious threshold. |
| **Every cut recoverable**<br>CCR on (default) | No `--no-ccr`; retrievals are the alarm. |
| **A receipt per request**<br>`HEADROOM_LOG_FILE=…/requests.jsonl` | Tokens before and after, cache reads and writes, latency, which transforms ran. |

And the measurement, in three sources that do not depend on each other: the
Claude Code transcripts, which record what the API actually billed per
request; the proxy's own request log, which records what it claims to have
done; and the subscription usage poller, which records what the plan's weekly
quota actually consumed. Two projects, three phases each — no proxy, cache
mode, token mode — with at least five working days in the last one.

The rule is fixed now, so that I cannot bend it later: **keep and deepen** if
billed tokens per request fall by fifteen percent or more, re-reads and
retrievals do not rise by more than a fifth, and the proxy's added latency
stays under four seconds at the ninetieth percentile. Otherwise, fall back to
cache mode or lossless compaction — and say so.

## What comes next

The editor took his seat tonight. In a few days I will publish what the
receipts say: tokens per request by phase, cache reads against cache writes,
how far a session stretches before it fills, how often the model asked for an
original back, and what the proxy cost in seconds. If the editor earns the
chair, I will say so. If he does not, I will say that too.

*Versions: Headroom 0.36.5, Claude Code 2.1.278, as of September 2026. The
numbers above come from one real project I work on; the project is not the
subject and is not named.*
