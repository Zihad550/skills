---
name: herdr-handoff
description: "Hand off to a new Claude Code session in a new Herdr tab, with a context file of what this session knows. Use when asked to hand off, start a new session with context, or open a new Claude session in a new tab. Usage: /herdr-handoff [task]."
---

# Herdr handoff

Load the `herdr` skill first and follow its rules. This skill adds only the handoff steps.

## 1. Check Herdr

```bash
test "${HERDR_ENV:-}" = 1
```

When it fails, say this session is not running inside Herdr and stop.

## 2. Write the handoff file

Write `./tmp/handoff-<name>.md` in the current checkout, never in the system `/tmp`. `<name>` is the agent name from step 4. Create `./tmp/` when it is missing. When `git check-ignore -q tmp/` fails, add `tmp/` to `$(git rev-parse --git-path info/exclude)`.

The file holds these sections:

- **Context**: the issue or PR number and its title, the worktree path, the branch.
- **Done so far**: what this session read or did, as facts with `file:line` references.
- **Findings**: findings, decisions the user already made, and open questions with their current status.
- **Task**: the skill's argument, or the current task when there is no argument.
- **Constraints**: edit files or implement only when the task asks for it. The repo's AGENTS.md rules still apply.

Done when every line in the file traces to this session's work. Leave out a section or a field that this session does not know.

## 3. Create the tab

```bash
herdr tab create --workspace "$HERDR_WORKSPACE_ID" --cwd "$PWD" --no-focus
```

Done when you hold the pane id from `.result.root_pane.pane_id` and the tab id from `.result.tab`.

## 4. Start Claude

```bash
herdr agent start <name> --kind claude --pane <pane-id>
```

Make the name from the issue, for example `issue-1017-explain`. It must match `[a-z][a-z0-9_-]{0,31}`. When the name clashes with a live agent, append `-2`.

Done when the output reports `agent_started`.

## 5. Send the prompt

```bash
herdr agent prompt <name> "Read ./tmp/handoff-<name>.md and do the task in it."
```

The prompt only points at the file. The context stays in the file.

## 6. Confirm the start

```bash
herdr agent wait <name> --until working --timeout 15000
```

A `timeout` here or from `agent prompt --wait` does not mean the prompt was lost. Check `herdr agent get <name>` and `herdr agent read <name> --source recent-unwrapped --lines 20` before any resend. Resend only when the read shows the prompt never arrived.

## 7. Report

Give the tab id, the pane id, the agent name and the handoff file path. Leave the user's focus where it is, and leave every pane, tab and session open.
