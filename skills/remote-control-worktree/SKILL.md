---
name: remote-control-worktree
description: "Open a git worktree in Herdr and start Claude Code there with Remote Control on, so the session can be driven from the phone. Use when asked for a worktree, or a new Claude session in one, with Remote Control. Usage: /remote-control-worktree <branch> [task prompt]."
---

# Remote Control worktree

Create a worktree workspace in Herdr, start `claude --remote-control` in it, and hand back the session link. Remote Control belongs to one `claude` process; a new pane never inherits it from this session.

Take the branch from the first argument, the repo from the current checkout, and any remaining text as the task prompt. Ask for a branch only when none is given.

## 1. Check Herdr

```bash
test "${HERDR_ENV:-}" = 1
```

When it fails, say this session is not inside Herdr and stop. Run `herdr --skill` once for the CLI guide when it is not already in context.

## 2. Create the worktree

Find the primary checkout with the first entry of `git worktree list --porcelain`. Herdr creates worktrees only from it and fails with `linked_worktree_source` from a linked one. Put the checkout beside it as `<primary>.<branch>`, with `/` in the branch turned into `-`.

```bash
herdr worktree create --cwd <primary> --branch <branch> --path <primary>.<branch-with-hyphens> --label <branch> --no-focus
```

Done when the JSON reports `worktree_created`. Keep `.result.root_pane.pane_id`.

## 3. Start Claude with Remote Control

The worktree's setup hooks may still run in the new pane, and `herdr agent start` then fails with `agent_pane_busy`. Retry until the pane is free:

```bash
for i in $(seq 1 60); do
  out=$(herdr agent start <agent-name> --kind claude --pane <pane-id> --timeout 60000 -- --remote-control <branch> 2>&1)
  grep -q agent_pane_busy <<<"$out" || { echo "$out"; break; }
  sleep 5
done
```

Use a unique agent name that matches `[a-z][a-z0-9_-]{0,31}`, made from the branch. Done when the output reports `agent_started` with `--remote-control` in `argv`.

## 4. Verify the connection

```bash
herdr pane wait-output <pane-id> --match 'remote-control is active' --timeout 30000
herdr pane read <pane-id> --lines 30 | grep -A1 'remote-control is active'
```

Done when the pane shows `/remote-control is active` and a `https://claude.ai/code/session_...` link. When it shows a Remote Control error instead, report that error and stop.

## 5. Send the task

When a task prompt was given, send it:

```bash
herdr agent prompt <agent-name> "<task prompt>" --wait --timeout 120000
```

## 6. Report

Give the worktree path, the branch, the Herdr workspace, the agent name, and the session link. The session also appears in the Claude app under **Code**.

## An agent that is already running

To turn on Remote Control in a running Claude agent, send the command, then one more `Enter`. The first `Enter` from `agent prompt` only picks the entry in the slash-command menu.

```bash
herdr agent prompt <agent> "/remote-control"
herdr agent send-keys <agent> Enter
```

Then verify as in step 4.
