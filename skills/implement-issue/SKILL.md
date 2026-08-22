---
name: implement-issue
displayName: Implement a GitHub issue end to end
description: Implement one GitHub issue unattended — read the ticket and the project's own rules, build exactly what it asks, verify it yourself with the repo's checks and a browser run, then commit and close the issue. Use when told to implement/work/do issue #N, or when driven by the ralph loop.
version: 1.0.0
tags: [github, issues, implementation, unattended]
---

# Implement a GitHub issue

Implement the issue the user names.

Assume you are running **unattended**: nobody will answer a question or verify
your work by hand. Finish the loop yourself.

## 1. Read the ticket

```bash
gh issue view <number> --comments
```

Read its labels and any issue or PR it references. If the repo documents tracker
conventions (`docs/agents/issue-tracker.md` or similar), follow them.

## 2. Read the project's own rules — before writing code

Whichever of these exist: `AGENTS.md`, `CLAUDE.md`, `CONTEXT.md`, `README.md`,
`docs/adr/`, and any guidelines file they point at. They are binding and override
your instincts about how this codebase works. Match the conventions of the
surrounding code.

## 3. Scope

Implement exactly what the issue asks. No adjacent refactors, no speculative
abstractions. If the code on disk already satisfies the issue, say so and skip to
step 5.

## 4. Verify without a human

Discover the repo's checks rather than assuming them: `package.json` scripts,
`mise.toml` / `Makefile` / `justfile` tasks, or the language's default
(`cargo test`, `go test ./...`, `pytest`). Run the lint and test commands the repo
actually defines, and fix what they surface.

For a change with a visible UI surface, drive the running app with Playwright
instead of asking for manual verification — use the `webapp-testing` skill.

Never claim a check passed that you did not run.

## 5. Commit and close

Stage only the files you touched — `git add <paths>`, never `git add -A`, since
the working tree may hold changes that are not yours. Commit with a Conventional
Commits subject of 50 characters or less. Do not push unless asked.

```bash
gh issue close <number> --comment "<what shipped, and how it was verified>"
```

If you could not finish, **leave the issue open** and comment with exactly what
blocks you. An honest blocked issue is worth more than a false close: whoever
picks it up next — a person or the loop — needs to know where you stopped.
