---
title: "The files that make Claude Code yours"
date: 2026-09-16T15:00:00-04:00
draft: false
translationKey: "claude-code-files"
categories: ["Technology"]
tags: ["claude-code", "ai-assisted-development", "tooling"]
description: "Claude Code is configured by a handful of plain-text files. Know which is which and the tool starts working your way — a short reference with tables."
---

Claude Code reads a handful of plain-text files before it does anything for
you. Most people never open them, and then wonder why the assistant keeps
running the wrong test command or asking permission for the same thing every
morning. Know the files and the tool starts working your way.

## Where they live

Two places: the project, which the whole team shares through git, and your
home directory, which is yours alone.

```text
my-project/
├── CLAUDE.md                  # project instructions — commit it
├── CLAUDE.local.md            # your private notes — gitignored
├── .mcp.json                  # MCP servers the team shares
└── .claude/
    ├── settings.json          # team permissions, hooks, env, model
    ├── settings.local.json    # your overrides — kept out of git
    ├── rules/                 # instructions scoped to a path
    ├── skills/<name>/SKILL.md # reusable prompts, run as /name
    └── agents/*.md            # subagents: own prompt, own tools

~/.claude/
├── CLAUDE.md                  # your preferences, every project
├── settings.json              # your defaults, every project
├── skills/ agents/ rules/     # personal versions of the same
├── keybindings.json           # keyboard shortcuts
└── projects/<p>/memory/       # what Claude remembers per project

~/.claude.json                 # app state and sign-in — not for editing
```

## The files that matter

| File | What it is for | Commit? |
|---|---|---|
| `CLAUDE.md` | Standing instructions: how to build, test, name things, what not to touch. Loaded every session. | Yes |
| `CLAUDE.local.md` | The same, but personal — your shortcuts, your paths. | No |
| `.claude/rules/*.md` | Instructions that only apply to part of the tree, gated by a `paths:` front matter. | Yes |
| `.claude/settings.json` | Permissions the team agreed on, hooks, environment variables, the default model. | Yes |
| `.claude/settings.local.json` | Your exceptions to the above. "Yes, and don't ask again" lands here. | No |
| `.mcp.json` | MCP servers the project needs — databases, issue trackers, browsers. | Yes |
| `.claude/skills/<name>/SKILL.md` | A procedure you run often, packaged as `/name`. Can bundle scripts and templates. | Yes |
| `.claude/agents/*.md` | A subagent: its own system prompt, its own tool list, run in its own context. | Yes |
| `~/.claude/settings.json` | Your defaults across every project — theme, model, personal permissions. | — |
| `~/.claude/projects/…/memory/` | Auto memory: notes Claude writes for itself about a project, one fact per file. | — |
| `~/.claude.json` | Sign-in session, personal MCP servers, per-project trust. Not for editing. | — |

## Which setting wins

The same key can be set in several places. Higher beats lower, with one
exception: nothing you set overrides what your organisation manages.

<div class="ladder" role="img" aria-label="Settings precedence, highest first: managed, command line, project local, shared project, user.">
  <div class="ladder-step"><span class="ladder-n">1</span><span class="ladder-name">Managed</span><code>managed-settings.json</code><span class="ladder-who">your organisation</span></div>
  <div class="ladder-step"><span class="ladder-n">2</span><span class="ladder-name">Command line</span><code>claude --settings</code><span class="ladder-who">you, this session</span></div>
  <div class="ladder-step"><span class="ladder-n">3</span><span class="ladder-name">Project local</span><code>.claude/settings.local.json</code><span class="ladder-who">you, this project</span></div>
  <div class="ladder-step"><span class="ladder-n">4</span><span class="ladder-name">Shared project</span><code>.claude/settings.json</code><span class="ladder-who">everyone in the project</span></div>
  <div class="ladder-step"><span class="ladder-n">5</span><span class="ladder-name">User</span><code>~/.claude/settings.json</code><span class="ladder-who">you, every project</span></div>
</div>

Claude Code watches these files and reloads them when they change, so an
edit to permissions or hooks reaches the running session without a restart.

## Where do I put this?

| I want to… | Put it in |
|---|---|
| Tell Claude how this project builds and tests | `CLAUDE.md` |
| Keep a note only I need | `CLAUDE.local.md` |
| Enforce a convention in one directory only | `.claude/rules/<topic>.md` with `paths:` |
| Allow a command for the whole team | `permissions.allow` in `.claude/settings.json` |
| Allow a command just for me | `.claude/settings.local.json` |
| Run a check before every commit | a `hooks` entry in `.claude/settings.json` |
| Turn a five-step routine into one command | `.claude/skills/<name>/SKILL.md` |
| Give a review its own context and tools | `.claude/agents/reviewer.md` |
| Connect a database or a browser | `.mcp.json` |

Start with `CLAUDE.md` and `.claude/settings.json`. Add the rest the day you
need it, not before.

*Reference: the [Claude directory](https://code.claude.com/docs/en/claude-directory) and [settings](https://code.claude.com/docs/en/settings) pages of the official documentation, as of September 2026.*
