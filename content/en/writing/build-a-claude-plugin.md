---
title: "Build a Claude Code plugin, step by step"
seoTitle: "Build a Claude Code plugin, step by step"
date: 2026-10-29T17:00:00-04:00
draft: false
translationKey: "build-a-claude-plugin"
categories: ["Technology"]
tags: ["claude-code", "plugins", "ai-agents"]
description: "A hands-on tutorial: build commit-helper, a Claude Code plugin with a slash command, a review agent and a hook that blocks secrets, then install it."
---

Sooner or later, everyone who works with Claude Code for a few weeks ends up with
a little collection of habits: a prompt they paste before every commit, a rule
they repeat about which files never to touch, a review they ask for so often that
they could recite it. Those habits live in a notes file, or in someone's head, and
they stop at the edge of that person's machine. A plugin is how you take them
out of there, because it packages commands, agents and hooks into a folder that
anyone can install with one line, so the way you work becomes something you hand
over instead of something you explain.

This tutorial builds one from an empty directory. The plugin is called
**commit-helper**, and by the end it will give you a `/commit-helper:commit`
command that writes a proper commit message, an agent that reviews the staged diff
before the message is written, and a hook that refuses to let a commit through
when the diff adds something that looks like a password or an API key. Each of
those is a different kind of plugin component, which is the point: once you have
built one of each, you know how every plugin is put together. Along the way I'll
point at [foreman](https://github.com/barrosef/foreman), a plugin I published
recently, only to show what the same piece looks like when a plugin grows up.

You need Claude Code (this was verified on version 2.1.312), git, and Python 3.
Everything below was tested on Linux; it should work as written on macOS, and on
Windows I'd run it under WSL.

## What a plugin is, on disk

A plugin is a directory, and Claude Code finds its parts by where they sit in it.
Nothing is registered anywhere and there is no build step, so the folder you are
about to create is the whole thing:

```text
commit-helper/
├── .claude-plugin/
│   ├── plugin.json
│   └── marketplace.json
├── skills/
│   └── commit/
│       └── SKILL.md
├── agents/
│   └── diff-reviewer.md
└── hooks/
    ├── hooks.json
    └── secret_guard.py
```

The `.claude-plugin/` folder holds metadata and nothing else, which is the one
rule people trip over first: skills, agents and hooks go at the plugin root,
next to it, never inside it. Create the skeleton now and we'll fill it in one
file at a time.

```bash
mkdir -p commit-helper/{.claude-plugin,skills/commit,agents,hooks}
cd commit-helper
```

## Step 1: the manifest

The manifest tells Claude Code what the plugin is called, and the name matters
more than it looks, because every component is namespaced under it. That is why
the command you'll write in a moment runs as `/commit-helper:commit` and never
collides with someone else's `commit`. Save this as `.claude-plugin/plugin.json`:

```json
{
  "name": "commit-helper",
  "version": "0.1.0",
  "description": "Writes your commit messages, reviews the diff first, and refuses to commit secrets.",
  "author": {
    "name": "Your Name"
  },
  "license": "MIT",
  "keywords": ["git", "commit", "review"]
}
```

Strictly speaking only `name` is required, and Claude Code would load the plugin
without a manifest at all, taking the name from the folder; but `version` is
worth setting from day one, since it is what keeps people who install your plugin
on a known release until you deliberately publish the next one. Use kebab-case,
and avoid names that start with `claude-`, which are reserved and rejected by the
validator. You can check your work at any point from the shell:

```bash
claude plugin validate .
```

On this plugin it answers `Validation passed with warnings`, and the only warning
is that there's no icon, which matters only if you list the plugin in Anthropic's
directory. foreman's manifest is the same file with a repository URL and a longer
description; manifests rarely get much bigger than this.

## Step 2: the command

A slash command in a plugin is a **skill**: a folder under `skills/` holding a
`SKILL.md` file whose frontmatter describes it and whose body is the instruction
Claude follows when it runs. There is an older `commands/` folder that still
works, but the documentation now recommends skills for new plugins, so that's
what we'll use. Save this as `skills/commit/SKILL.md`:

```markdown
---
name: commit
description: Write a commit message for the staged changes, after a diff review, and commit when the user confirms.
disable-model-invocation: true
---

Commit the user's staged changes with a good message. Work in this order.

1. Run `git diff --cached --stat`. If nothing is staged, say so and stop; do not stage
   files on your own.
2. Dispatch the `diff-reviewer` agent and wait for its report. If the verdict is
   `concerns`, show the list to the user and ask whether to go on.
3. Write the message in Conventional Commits form: a subject line under 72 characters
   (`feat:`, `fix:`, `docs:`, `refactor:`, `test:` or `chore:`), a blank line, then a short
   body that explains why the change was made, not what each line does.
4. Show the message and ask the user to confirm or edit it.
5. Only after they confirm, run `git commit` with that message. If a hook blocks the
   commit, show its reason and stop.
```

Two details in that file do most of the work. The `description` is what Claude
reads to decide what the skill is for, so it is worth writing as carefully as the
body. `disable-model-invocation: true` means the skill only runs when you type it;
without that line Claude could decide on its own that now is a good moment to
commit, which is exactly what you don't want from a command that writes history.
The body itself is plain instructions written for a capable colleague, numbered
because order matters here, and it already mentions the agent and the hook we
haven't written yet, because that is how the three pieces will meet.

## Step 3: the agent

An agent is a specialist Claude can hand a task to. It runs in its own context,
with its own instructions and only the tools you give it, and reports back when
it's done. That isolation is what makes it useful as a reviewer: it looks at the
diff without the conversation that produced it, so it hasn't already decided the
change is fine. Save this as `agents/diff-reviewer.md`:

````markdown
---
name: diff-reviewer
description: Reviews the staged git diff before a commit and reports problems. Use before writing a commit message. Reports only; never edits files.
tools: Read, Grep, Glob, Bash
model: sonnet
---

You review a staged diff before it is committed. Run `git diff --cached` to see it,
and open the surrounding files when a change needs context.

Look for things a reviewer would stop a commit for:

- debugging leftovers: print statements, commented-out code, `TODO` added in this diff
- a change that does something different from what its neighbours suggest
- files that look unrelated to the rest of the change and probably belong in another commit
- anything that looks like a credential or a private key

Report in this shape, and nothing else:

```
VERDICT: ok | concerns
- <file>:<line> — <what you saw and why it matters>
```

Write `VERDICT: ok` with no list when you find nothing. Never edit, stage or commit
anything; your job ends at the report.
````

The frontmatter is where you make the agent's job safe. `tools` leaves out
`Edit` and `Write`, so even a reviewer that misreads its instructions can't
change your files, and `model: sonnet` gives a routine review to a model that
handles it well without spending your most expensive one on it. The fixed report
shape is there for the skill, which needs to tell `ok` from `concerns` without
interpreting prose. In foreman the agents are the same kind of file, only longer,
because each of them carries a role on a team (an explorer that only reads, a
reviewer that attacks a spec before work starts), and the frontmatter is where
those limits are enforced too.

## Step 4: the hook

Skills and agents are instructions, and an instruction can be ignored or
forgotten. A hook can't, because it isn't sent to the model at all: it's a
program Claude Code runs itself at a fixed point in its lifecycle. That makes it
the right home for the one rule in this plugin that must never bend. We'll use a
`PreToolUse` hook on the Bash tool, which runs before every shell command Claude
is about to execute, receives the command as JSON on stdin, and blocks it by
exiting with code 2. Save the registration as `hooks/hooks.json`:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "python3 \"${CLAUDE_PLUGIN_ROOT}\"/hooks/secret_guard.py"
          }
        ]
      }
    ]
  }
}
```

The outer `"hooks"` key looks redundant, but a plugin's hooks file needs it, and
without it the file fails to load. `${CLAUDE_PLUGIN_ROOT}` is replaced
with wherever the plugin ends up installed, and the quotes around it keep a path
with spaces in one piece. The script itself is short enough to read in one go;
save it as `hooks/secret_guard.py`:

```python
#!/usr/bin/env python3
"""PreToolUse hook: block a git commit whose diff adds something that looks like a secret.

Claude Code sends the tool call as JSON on stdin. Exit 0 lets it through;
exit 2 blocks it, and whatever we print on stderr is shown to Claude.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys

PATTERNS = [
    re.compile(r"AKIA[0-9A-Z]{16}"),                      # AWS access key
    re.compile(r"gh[pousr]_[A-Za-z0-9]{36}"),             # GitHub token
    re.compile(r"sk-ant-[A-Za-z0-9_-]{20,}"),             # Anthropic API key
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),    # PEM private key
    re.compile(r"(password|secret|token|api_key)\s*[:=]\s*['\"][^'\"]{8,}['\"]", re.I),
]


def is_commit(command: str) -> bool:
    return re.search(r"\bgit\s+commit(\s|$)", command) is not None


def commit_all(command: str) -> bool:
    return re.search(r"\bgit\s+commit\b.*\s(-[a-zA-Z]*a[a-zA-Z]*|--all)\b", command) is not None


def find_secrets(diff: str) -> list[str]:
    added = (line[1:].strip() for line in diff.splitlines()
             if line.startswith("+") and not line.startswith("+++"))
    return [line for line in added if any(p.search(line) for p in PATTERNS)]


def staged_diff(cwd: str | None, include_unstaged: bool) -> str:
    target = ["HEAD"] if include_unstaged else ["--cached"]
    result = subprocess.run(["git", "diff", *target], cwd=cwd, capture_output=True, text=True)
    return result.stdout if result.returncode == 0 else ""


def main(stdin_text: str) -> int:
    try:
        event = json.loads(stdin_text)
        command = event["tool_input"]["command"]
    except (ValueError, KeyError, TypeError):
        return 0  # not something we understand: never get in the way
    if not is_commit(command):
        return 0
    hits = find_secrets(staged_diff(event.get("cwd"), commit_all(command)))
    if not hits:
        return 0
    print("commit-helper blocked this commit: the diff adds what looks like a secret:", file=sys.stderr)
    for line in hits:
        print(f"  {line[:80]}", file=sys.stderr)
    print("Remove it (or move it to an environment variable) and commit again.", file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.stdin.read()))
```

Most of what makes this script safe to run before every shell command is in the
small decisions. It looks only at lines the diff *adds*, so deleting a leaked key
is never blocked; it reads `git diff HEAD` when the commit uses `-a`, because
then the changes that matter aren't staged yet; it runs git in the `cwd` that
Claude Code sends with the event; and whenever it meets something it doesn't
understand, such as malformed input or a folder that isn't a repository, it exits
0 and gets out of the way, since a hook that wedges every command is worse than no
hook. It uses only the standard library, and the `__future__` import lets the type
hints run on the Python 3.9 that macOS ships with. Because `main` takes the input
as a string, the logic is easy to cover with ordinary pytest tests; the version in
this tutorial has fourteen of them, including a key on a deleted line and
`git commit` hidden at the end of a `git add . && …` chain.

## Step 5: install it and watch it work

Claude Code installs plugins from a **marketplace**, which sounds grander than it
is: a `marketplace.json` file listing one or more plugins and where to find them.
To install your own plugin you make a marketplace of one, right inside the plugin
folder. Save this as `.claude-plugin/marketplace.json`:

```json
{
  "name": "commit-helper-dev",
  "owner": {
    "name": "Your Name"
  },
  "plugins": [
    {
      "name": "commit-helper",
      "source": "./",
      "description": "Writes your commit messages, reviews the diff first, and refuses to commit secrets."
    }
  ]
}
```

Inside Claude Code, add the marketplace with `/plugin marketplace add` followed by
the folder's path, then open `/plugin` and install commit-helper from the list. If
you'd rather stay in the shell, the same two steps are commands, and the third
shows you what got installed:

```bash
claude plugin marketplace add /path/to/commit-helper
claude plugin install commit-helper@commit-helper-dev
claude plugin details commit-helper
```

The last command should list exactly the three pieces you wrote:

```text
Component inventory
  Skills (1)  commit
  Agents (1)  diff-reviewer
  Hooks (1)  PreToolUse  (harness-only — no model context cost)
```

Now try to break it. In any git repository, stage a file containing
`AWS_KEY = 'AKIAABCDEFGHIJKLMNOP'` (a fake key in the AWS format)
and ask Claude to commit it. When I ran that, Claude reported back:

```text
The commit didn't happen. A PreToolUse hook (`secret_guard.py` from the
`commit-helper` plugin) stopped `git commit -m 'add config'` before it could run.
The hook says the staged `config.py` adds what looks like an AWS access key ...
```

and `git log` confirmed that nothing had been committed. Then replace the key with
`os.environ["AWS_KEY"]`, stage the file again, and type `/commit-helper:commit`.
The skill runs the reviewer, gets `VERDICT: ok`, and comes back with a proposed
message (`chore: add config module reading AWS key from environment`, in my run)
and a question, because it doesn't commit until you confirm. While you iterate on
the plugin you can skip the install entirely: `claude --plugin-dir ./commit-helper`
loads it for that one session, so every edit is picked up the next time you start.

## Step 6: share it

Everything that made your local install work also makes the plugin shareable,
because a marketplace can live in a git repository as easily as in a folder. Push
the `commit-helper` directory to a repository, and a colleague installs it with
`/plugin marketplace add your-org/commit-helper` followed by the same install. From
then on, the `version` in your manifest is your release valve: bump it when you
want people to get the new behaviour. foreman is shipped exactly this way, with a
`marketplace.json` at the root of its GitHub repository listing a single plugin
whose `source` is `./`, so the file you just wrote is the same one a published
plugin uses, only with a different name in it. (If you're curious why foreman
exists in the first place, I wrote about that in
[The Culture You Can Install](/writing/the-culture-you-can-install/).)

Where you go from here depends on what your team keeps repeating. If it's a
procedure, it becomes a skill; if it's a specialist you keep briefing, it becomes
an agent; and if it's a rule that must hold even when nobody remembers it, it
becomes a hook. The plugin is just the folder that carries them from your machine
to everyone else's.
