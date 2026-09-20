# clh.ps1 — Windows twin of the Linux wrapper. Put it on your PATH;
# run `clh --resume`. The proxy itself is kept alive by the
# Task Scheduler entry that `headroom install apply` creates.
$env:ANTHROPIC_BASE_URL = "http://127.0.0.1:8787"
$env:ENABLE_TOOL_SEARCH = "true"
claude --dangerously-skip-permissions @args
