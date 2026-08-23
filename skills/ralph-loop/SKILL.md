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
| `heartbeat` | rewritten every 15s **only while a run is in flight**. Its timestamp tracks ralph, not opencode — read the `lines=` counter inside it, not the file's age |
| `current.log` | symlink to the live transcript; absent when idle |
| `logs/` | full transcript per attempt, named `issue-N-attemptK-*.log` |

To get pushed events instead of polling, watch the timeline:

```bash
tail -f .ralph/ralph.log | grep --line-buffered -E "picked|closed|parked|WARN|done —"
```

Reading a status:

- `status: running` + `lines=` still climbing → healthy, leave it alone.
- `status: running` + `lines=` flat across two looks minutes apart → **hung**.
  See "Telling a hang from slow work" below.
- `parked: #N` → the issue survived every attempt without closing. Read
  `logs/issue-N-attempt*.log` and the issue's comments to find out why. Parking
  is the loop protecting itself from an infinite retry, not a bug.
- `done` grows but the tree is dirty → the agent closed an issue while leaving
  uncommitted work. Flag it; that usually means a partial implementation.

## Telling a hang from slow work

`RALPH_RUN_TIMEOUT` is a ceiling, not a wait. `bin/ralph` runs opencode as a
blocking foreground call, so **whenever opencode exits, ralph returns within
seconds** — a crash, a dropped connection, a provider `Service Unavailable`, a
clean finish. Only one case burns the full timeout: opencode still alive but
producing nothing, which is what a model that stops responding mid-stream looks
like. The connection stays open, opencode blocks on it, and `timeout` fires at
`RALPH_RUN_TIMEOUT` with `rc=124`.

**The heartbeat's freshness cannot tell you which is happening.** It is written
by a subshell on ralph's own 15s timer, independent of opencode, so it stays
fresh right through an hour-long hang — it only goes stale if ralph itself dies.
What it carries is the signal:

```
alive 2026-08-23T15:11:56+06:00  lines=1847  last=→ Read src/components/FaresPage.tsx
```

`lines=` is the transcript's line count. Compare it across two looks a few
minutes apart:

```bash
ralph --status | grep heartbeat     # note lines=
# …several minutes later…
ralph --status | grep heartbeat     # climbing = working, flat = hung
```

Equivalently, watch whether `.ralph/current.log`'s mtime advances.

When supervising a run, check this **occasionally and spaced out** — every few
minutes at most, never in a tight loop. A flat counter is worth surfacing to the
user with the transcript tail: a hang donates the rest of the hour to nothing,
and killing it early frees the attempt. A climbing counter means leave it alone,
however slow it looks.

This also decides whether raising `RALPH_RUN_TIMEOUT` would have helped. Compare
the transcript's last write against the kill time:

```bash
ls -la --time-style=+%H:%M:%S .ralph/logs/ | tail
```

Silent for most of the run → it hung, and more clock buys nothing. Writing until
seconds before the kill → genuinely slow, and a larger timeout is the fix. Do not
recommend raising the timeout without checking which one it was.

## Running more than one

**One ralph per checkout**, enforced by a lock in `.ralph/lock.d`. If starting one
reports `already running (pid N)`, do not delete the lock to force it — check
`ralph --status` first; a second loop in one working tree interleaves two agents'
commits on one branch. A lock held by a dead process is cleared automatically.

Different repos need no coordination at all.

To work one repo in parallel, give each loop its own checkout and turn on claiming:

```bash
git worktree add ../repo-b -b ralph-b
RALPH_CLAIM=1 ralph &            # in each checkout
```

`RALPH_CLAIM=1` assigns each issue to `@me` before work starts and drops assigned
issues from the frontier, so two loops never take the same ticket. A failed attempt
releases the issue; a **parked** issue keeps its assignee on purpose, so no other
worker grinds through the same broken ticket. Never suggest claiming for a single
loop — it only adds assignee churn.

Watch for the shared-resource collision that survives all of this: two
browser-verifying agents reaching for the same dev-server port.

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
