---
title: "Skill or plugin? Choosing how to package what Claude should know"
seoTitle: "Skill or plugin? How to choose in Claude Code"
date: 2026-10-30T17:00:00-04:00
draft: false
translationKey: "skill-or-plugin"
categories: ["Technology"]
tags: ["claude-code", "plugins", "ai-agents"]
description: "Skills hold know-how; plugins distribute it. A developer's guide to choosing between a personal skill, a repo commit and a plugin in Claude Code."
---

The third time I typed the same instructions into Claude Code (how our release
notes are written, which sections they need, the tone we use with clients) I
stopped halfway through the sentence, because repeating myself had become the
real work. The fix seemed obvious: package it once. What wasn't obvious was the
packaging, since Claude Code offers two names that sound like rivals, a skill and
a plugin, and almost everyone I've talked to picks one by instinct and then
discovers, a few weeks later, that they solved a different problem from the one
they had.

The confusion is understandable, because a plugin can contain skills, and a skill
can do much of what people build plugins for. But the two answer different
questions. This article is about telling those questions apart, so that the next
time you catch yourself repeating something to Claude, you know where it belongs.

## Two answers to two different questions

A **skill** is a unit of know-how. It is a folder with a `SKILL.md` file whose
frontmatter describes it and whose body tells Claude how to do something, plus
any reference files or scripts that help. Claude reaches for it when your request
matches its description, or you run it yourself as `/skill-name`. Its question is
*"how should Claude do this?"*

A **plugin** is a unit of distribution. It is a directory that Claude Code
installs and loads as one piece, usually from a marketplace, and it can carry
skills alongside subagents, hooks, MCP servers and other components, all under one
name and one version. Its question is *"how does this setup reach other people
and other projects, and stay the same everywhere?"*

Between the two sits an option that many developers overlook, and it settles more
cases than either: the repository itself. Claude Code reads a project's `.claude/`
folder, so skills in `.claude/skills/`, subagents in `.claude/agents/`, hooks in
`.claude/settings.json` and MCP servers in `.mcp.json` reach everyone who clones
the repo, with no plugin at all. That gives three homes rather than two, and the
rest of this article is about choosing between them.

## What problem each one solves

A skill solves the problem of a capable assistant that doesn't know *your* way of
doing something. Your release-notes format, the checklist you run before a
migration, the way your team names feature flags: none of that is in the model,
and pasting it every time is both tedious and inconsistent. A skill writes it down
once, and Claude Code is economical about it, because only the description sits
in Claude's context so that it knows the skill exists, while the full body loads
when the skill is actually used. That is why a long, detailed skill costs almost
nothing until the moment it is needed.

A plugin solves a different problem: a setup that works on your machine and has to
work, identically, somewhere else. Once your Claude Code habits span a few skills,
a reviewer subagent, a hook that runs a formatter after every edit and an MCP
server for your issue tracker, the hard part is no longer writing any of them; it
is getting all of them to a colleague, or to the next repository, in a state that
matches yours, and knowing which version they have when something behaves
differently.

## Where each one lives, and who gets it

Where you save a skill decides who gets it, and that is the most practical way to
think about the choice. A skill in `~/.claude/skills/` is personal: it follows you
into every project on your machine, and nobody else ever sees it. A skill in the
project's `.claude/skills/` belongs to that repository, and the documentation's
advice is simply to commit it so that your team gets it too; the same goes for
subagents in `.claude/agents/`, for hooks in the shared `.claude/settings.json` and
for MCP servers in `.mcp.json`, so a team can already share a complete setup
through `git pull`. When two skills share a name, the personal one wins over the
project's, which is worth remembering when a teammate says your `/deploy` behaves
differently from theirs.

A plugin lives somewhere else entirely. It is fetched from a marketplace (a
repository or folder with a `marketplace.json` that lists plugins) into Claude
Code's own plugin storage, and you choose a scope when you install it: for
yourself in every project, or for one repository, where the committed settings
declare it and each collaborator still installs it on their own machine. Its
skills appear under its name, as `/plugin-name:skill-name`, which is how two
plugins can each ship a `review` skill without stepping on each other.

## What only a plugin can do

It is tempting to answer "hooks" or "agents", but that would be wrong, since every
one of those components also works on its own. What a plugin adds is not a new
capability but a new kind of reach. It lets one setup travel as a single unit
into many repositories at once, where committing `.claude/` would mean copying the
same files into each of them and hoping the copies never drift. It gives that setup
a version, so that people stay on a known release until you publish the next one,
and it gives them a way to receive the next one, because whoever adds your
marketplace gets your updates instead of a diff to apply by hand. It also keeps
your names out of everyone else's way through the plugin prefix, which matters as
soon as your setup meets other people's.

## What a plugin costs you

None of that is free, and when I packaged my own team's working rules as a plugin
I paid each of these costs in turn. The names change first: a skill that was
`/deploy` becomes `/my-plugin:deploy`, and the people who had the habit of typing
the short one need telling. The footprint changes next, because an enabled plugin
is part of every session, not only the ones where you use it: the descriptions of
the skills and agents Claude may invoke are in context on every turn, its hooks
fire on their events and its MCP servers run, all with your permissions, so a
plugin installed "just in case" is never really idle. And then there is the work
that comes with being a publisher rather than a user: a manifest to keep honest, a
version to bump on purpose, a marketplace to maintain, and the question, every
time you change something, of who will receive it and when. For a single
repository, all of that is overhead with nothing to show for it, because `git pull`
already does the distributing.

A skill, by contrast, costs a file. You can edit it in the middle of a session and
Claude Code picks up the change without a restart, and when it turns out to be
wrong, you fix one place. The trade-off is reach: a skill reaches exactly as far as
the folder you saved it in.

## Deciding in under a minute

<div class="path" role="img" aria-label="Three questions in order: is it only for me, then a personal skill in ~/.claude/skills; is it for everyone in this one repository, then commit it under .claude in the repo; must it reach other repositories or people as one versioned unit, then a plugin.">
  <div class="path-step"><span class="path-n">1</span><span class="path-name">Only for me?</span><span class="path-who">a personal skill in <code>~/.claude/skills/</code></span></div>
  <div class="path-step"><span class="path-n">2</span><span class="path-name">For everyone in this one repo?</span><span class="path-who">commit it under <code>.claude/</code>: skills, agents, hooks, <code>.mcp.json</code></span></div>
  <div class="path-step path-step-human"><span class="path-n">3</span><span class="path-name">Must it travel beyond this repo?</span><span class="path-who">a plugin: one unit, one version, updates from a marketplace</span></div>
</div>

So the choice comes down to one question asked three ways, and it is never "which
is more powerful?" but "how far does this need to go?". When the know-how is yours
alone, such as the release-notes format you prefer or a debugging routine nobody
else uses, it is a personal skill, and you should write it today. When it belongs
to a project and everyone working there should share it, as with that repository's
review checklist, its reviewer subagent and the hook that formats every edit,
commit it under `.claude/`, because the repository is already the best
distribution channel that team has. And when the same setup has to reach many
repositories or many people, stay identical across all of them and change only
when you decide it should, that is the moment, and the only moment, to build a
plugin.

The order matters as much as the rule. Almost everything worth packaging starts as
a skill that one person found useful, becomes a few files that one team commits,
and earns a plugin only when it outgrows the repository it was born in; the
documentation even shows how to convert a `.claude/` setup into a plugin when that
day comes. Start with the smallest home that reaches everyone who needs it, and
let the thing you built tell you when it needs a bigger one.
