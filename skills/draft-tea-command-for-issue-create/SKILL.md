---
name: draft-tea-command-for-issue-create
displayName: Draft tea issue-create command
description: Draft a Forgejo issue title and description for the user to discuss with a teammate, then give the exact tea CLI command to create it. Does not run the command.
version: 1.0.0
tags: [forgejo, tea, issues, drafting]
---
# Instructions

1. Draft only a title and a description, based on the current conversation, the codebase, and/or user-provided instructions. If either is unclear, explore the codebase and ask the user follow-up questions rather than guessing.
2. Write in natural language. Never use em dashes. Use present tense for verbs (e.g. "filter", not "filters" or "filtered", unless grammar requires otherwise).
3. When the draft is meant to prompt a discussion (e.g. "is this expected behavior?", "should we do X or Y?") rather than assert a bug, phrase the description as an open question, not a conclusion. State what was observed, how to reproduce it if applicable, and end with the actual question for the teammate.
4. Show the drafted title and description to the user first and ask if they'd like changes, unless they've already approved the content earlier in the conversation.
5. Show the bare body text on its own first, as plain markdown, separate from the command. Don't route it through a temp file and `--body "$(cat <path>)"`; inline it directly in the command instead.
6. Give the exact `tea` command with the body inlined directly as a double-quoted string, backticks escaped with a backslash (`` \` ``) so they aren't read as command substitution. Don't pass `--repo`; `tea` infers it from the current directory's git remote when run inside the repo.
```bash
tea issues create \
  --title "<title>" \
  --body "<body, inlined, with every \` escaped>"
```
   - Confirm the actual flag names with `tea issues create --help`, but run it in the same shell the user will actually run the command in (ask if unsure), not just wherever the assistant's tool calls happen to execute. The two can be different `tea` installs/versions with different flags (e.g. `--body`/`-b` vs `--description`/`-d`), and the assistant's own shell isn't authoritative for what the user has.
   - If the user reports a "flag provided but not defined" error, the CLI's own usage output in that error already gives the real flag names; use those directly instead of re-guessing or re-checking the assistant's own `--help`.
   - If `tea login ls` (or the current version's equivalent) shows no configured logins, mention that the user may need to pass `-l <login-name>` or run `tea login add` first.
   - Double-quoted strings also treat `$`, `"`, and `\` specially; escape any that appear in the body too. If the body has enough of these that escaping makes it hard to read, say so and offer the temp-file approach as a fallback rather than silently reintroducing it.

# Requirements

1. This skill only drafts and hands over the command. Do not execute `tea issues create` yourself unless the user explicitly says to run it.
2. Do not fabricate the repo slug or login name; verify them (`git remote -v`, `tea login ls`) rather than assuming, even though the command itself omits `--repo`.
3. Never hand over a command with unescaped backticks, `$`, or `"` inside a double-quoted `--body` value; verify the escaping before presenting it, since a paired unescaped backtick silently triggers command substitution instead of erroring.
