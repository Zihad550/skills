---
name: ralph-loop
displayName: Run and supervise the ralph issue-queue loop
description: Run and supervise `ralph` — the unattended loop that drains a repo's ready-for-agent GitHub issues one at a time with opencode, committing and closing each. Use when asked to work through the issue queue unattended, to start/stop/check on ralph, to read .ralph/state.json or .ralph/ralph.log, or to explain why the loop parked or stalled on an issue.
version: 1.0.0
tags: [github, issues, automation, opencode, unattended]
---

# Ralph loop

`ralph` is a bash loop over a repo's issue queue. One pass = pick the
lowest-numbered open issue that carries the agent-ready label and has **zero open
blockers**, hand it to `opencode run` with the `/implement-issue` command, then check
whether the issue actually closed. Repeat until the frontier is empty.

It writes changes and closes issues on the user's behalf, so it is **never
started without the user asking for it**.

## Before starting a loop

```bash
ralph --check      # config + the exact frontier it will work through
```

Read the output back to the user. Watch for:

- **An empty frontier** — nothing is labelled agent-ready and unblocked. Do not
  "fix" this by relabelling issues on your own.
- **Issues that look already done.** `--check` lists titles; if git history says
  the work shipped, tell the user — a stale open issue burns a full run.
- **A dirty working tree.** ralph warns, but the agent's commits will sweep up
  whatever it stages. Offer to commit or stash first.
- **No `.ralph.env`** in a repo whose checks are unusual — see
  `ralph.env.example` for the per-repo knobs.

## Starting it

```bash
ralph --once       # one issue, then stop — always prefer this for a first run
ralph              # drain the queue
```

Start it as a **background** process so you stay responsive, and tell the user
which mode you used. A run can take many minutes; never poll it in a tight loop.

## Supervising

One command, readable whether or not the loop is running, from any session:

```bash
ralph --status         # state + timeline + heartbeat + last 40 transcript lines
ralph --status 100     # deeper transcript tail
```

Underneath, in the repo's `.ralph/`:

| File | Use it for |
|---|---|
| `state.json` | machine-readable status, current issue + attempt, `done`, `parked`, frontier |
| `ralph.log` | append-only timeline — grep `picked\|closed\|parked\|WARN` |
| `heartbeat` | written every 15s **only while a run is in flight**; a stale one means the run ended or hung |
| `current.log` | symlink to the live transcript; absent when idle |
| `logs/` | full transcript per attempt, named `issue-N-attemptK-*.log` |

To get pushed events instead of polling, watch the timeline:

```bash
tail -f .ralph/ralph.log | grep --line-buffered -E "picked|closed|parked|WARN|done —"
```

Reading a status:

- `status: running` + a **fresh** heartbeat → healthy, leave it alone.
- `status: running` + a heartbeat older than a couple of minutes → the run is
  wedged; it will be killed at `RALPH_RUN_TIMEOUT` anyway. Show the user the
  transcript tail before suggesting a kill.
- `parked: #N` → the issue survived every attempt without closing. Read
  `logs/issue-N-attempt*.log` and the issue's comments to find out why. Parking
  is the loop protecting itself from an infinite retry, not a bug.
- `done` grows but the tree is dirty → the agent closed an issue while leaving
  uncommitted work. Flag it; that usually means a partial implementation.

## Stopping

`Ctrl-C`, or kill the pid in `state.json`. The loop traps the signal, writes
`status: interrupted`, and prints its summary. It never abandons state.

## What ralph deliberately does not do

- **No retries beyond `RALPH_MAX_ATTEMPTS`** (default 2) — the issue is parked
  and the loop moves on.
- **No pushing, no PRs, no branch creation.** It commits to the current branch.
  If the user wants isolation, put them on a branch before starting.
- **No relabelling or reprioritising.** The queue is the user's to shape; ralph
  only reads it.
- **GitHub only.** The blocked check reads GitHub's native issue dependencies
  (`issue_dependencies_summary.blocked_by`). Another tracker needs a new
  frontier query, not a config flag.
