---
name: draft-tea-command-for-issue-create
displayName: Draft tea issue-create command
description: Draft a Forgejo issue title and description for the user to discuss with a teammate, then give the exact tea CLI command to create it. Does not run the command.
version: 1.2.0
tags: [forgejo, tea, issues, drafting]
---
# Instructions

1. Draft only a title and a description, based on the current conversation, the codebase, and/or user-provided instructions. If either is unclear, explore the codebase and ask the user follow-up questions rather than guessing.
2. Write in natural language. Never use em dashes. Use present tense for verbs (e.g. "filter", not "filters" or "filtered", unless grammar requires otherwise).
3. When the draft is meant to prompt a discussion (e.g. "is this expected behavior?", "should we do X or Y?") rather than assert a bug, phrase the description as an open question, not a conclusion. State what was observed, how to reproduce it if applicable, and end with the actual question for the teammate.
4. Show the drafted title and description to the user first and ask if they'd like changes, unless they've already approved the content earlier in the conversation.
5. Show the body in chat as plain markdown, and write that same text to a short temp file at `/tmp/tea-issue-<slug>.md`. The chat copy is the preview the user reads; the file is what `tea` sends. Keep the two identical.
6. Give the command as a **single line** that reads the body back from the file and passes the verified repository slug with `-r <owner/repo>`.
```bash
tea issues create -l <login> -r <owner/repo> --title "<title>" --description "$(</tmp/tea-issue-<slug>.md)"
```
   - One line is the point. A `--description "…"` spanning several lines leaves the quote open, so the shell prints a continuation prompt for every following line and a pasted body arrives mangled or empty.
   - `$(<file)` is shell-builtin file reading. Use it rather than `$(cat file)`, because `cat` is often aliased to a pager (`bat --color=always` and similar), and command substitution then captures that pager's header box, line numbers, and ANSI escape codes, all of which land verbatim in the issue body. `command cat` also bypasses the alias.
   - Reading from a file needs no escaping, so backticks, `$`, `"`, and `\` in the body pass through untouched.
   - Confirm the actual flag names with `tea issues create --help`, but run it in the same shell the user will actually run the command in (ask if unsure), not just wherever the assistant's tool calls happen to execute. The two can be different `tea` installs/versions with different flags (e.g. `--body`/`-b` vs `--description`/`-d`), and the assistant's own shell isn't authoritative for what the user has.
   - If the user reports a "flag provided but not defined" error, the CLI's own usage output in that error already gives the real flag names; use those directly instead of re-guessing or re-checking the assistant's own `--help`.
   - If `tea login ls` (or the current version's equivalent) shows no configured logins, mention that the user may need to run `tea login add` first. When it lists a login whose `DEFAULT` is false, pass that name as `-l <login>`.
   - Resolve `<owner/repo>` from the intended repository's `git remote -v`. For HTTPS and SSH remotes, remove the host portion and any trailing `.git`. Do not guess the slug or rely on the command's current directory to select the repository.

# Requirements

1. This skill only drafts and hands over the command. Do not execute `tea issues create` yourself unless the user explicitly says to run it.
2. Do not fabricate the repo slug or login name. Verify them with `git remote -v` and `tea login ls`, then include both `-r <owner/repo>` and `-l <login>` in every `tea` command you hand over.
3. Before handing the command over, confirm it occupies one line and that the path inside `$(<…>)` is the file you just wrote.
4. A mangled description means the issue already exists on the server. Find its index with `tea issues ls -l <login> -r <owner/repo> --state all --author <user>`, then hand over `tea issues edit <idx> -l <login> -r <owner/repo> -d "$(</tmp/tea-issue-<slug>.md)"`, adding `tea issues reopen <idx> -l <login> -r <owner/repo>` if the user closed it. Leave running those to the user too.
