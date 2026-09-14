---
name: session-status
description: >-
  Inspect active token context and session metrics anytime via
  scripts/session_status.py, and format the standardized agent footer bar.
---

# Session and Context Monitoring

Use this skill to inspect active context token usage, model parameters, and CLI quota remaining during an Antigravity session.

## Usage

Run the monitoring helper script:

```bash
python scripts/session_status.py
```

## Output

The script inspects the latest transcript log in the Antigravity session directory and prints:
1. **Active Model & Context Window**: Current model and maximum context window.
2. **Token Usage & Progress Bar**: Approximate context tokens used and visual bar.
3. **Model Quotas Remaining**: Active 5-hour and weekly quota percentages from the `agy` CLI.
4. **Agent Footer Bar**: The standardized footer required at the end of every response:

```markdown
---
[Context: <used>% (~<tokens>k / <max>k tokens) | <Model>] [Quota Remaining: 5h: <pct>% | Weekly: <pct>%]
```
