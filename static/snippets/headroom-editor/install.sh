# 1. Install the CLI in its own environment (Linux, macOS, Windows).
uv tool install --python 3.13 "headroom-ai[all]"
#    or: pip install "headroom-ai[all]"

# 2. One command, every OS: a proxy that survives reboots,
#    with the test's guardrails. Linux -> systemd user service,
#    macOS -> launchd agent, Windows -> Task Scheduler.
headroom install apply \
  --preset persistent-service \
  --mode token \
  --protect-tool-results Read,Edit,Write \
  --env HEADROOM_TOOL_DESC_MAX_CHARS=200 \
  --env HEADROOM_LOG_FILE="$HOME/.headroom/logs/requests.jsonl" \
  --telemetry

# 3. Route Claude Code through it: writes env + hooks into
#    .claude/settings.local.json (--global: ~/.claude/settings.json).
#    Then check the wiring.
headroom init claude
headroom doctor
