---
name: draft-gt-command-for-issue-create
displayName: Draft gt issue-create command
description: Draft a Forgejo issue title and description for the user to discuss with a teammate, then give the exact gt CLI command to create it. Does not run the command.
version: 2.1.0
tags: [forgejo, gt, issues, drafting]
---
# Instructions

1. Draft only a title and a description, based on the current conversation, the codebase, and/or user-provided instructions. If either is unclear, explore the codebase and ask the user follow-up questions. Done when both are drafted and no question is left open.
2. Write in natural language. Never use em dashes. Use present tense for verbs (e.g. "filter", not "filters" or "filtered", unless grammar requires otherwise).
3. When the draft is meant to prompt a discussion (e.g. "is this expected behavior?", "should we do X or Y?") rather than assert a bug, phrase the description as an open question, not a conclusion. State what was observed, how to reproduce it if applicable, and end with the actual question for the teammate.
4. Write the description to `<root>/tmp/gt-issue-<slug>.md`, where `<root>` is the session's project root: where the session started, or where `/cd` or a worktree move took it; create `tmp/` when it is missing. Use it even when the session names a scratchpad directory for temp files: the user reads the draft through the `/drafts` panel, which reads only `<root>/tmp`. Leave the description out of the chat reply. The file is both the preview and what `gt` sends. Done when the file exists.
5. Show the title in chat with the file's absolute path, and ask if they'd like changes, unless they've already approved the content earlier in the conversation. On changes, edit the file in place. Done when the user approves the draft.
6. Hand over the command, which reads the body from the file:
```bash
gt issue create -R <owner/repo> --title "<title>" --body-file <root>/tmp/gt-issue-<slug>.md
```
   - Resolve `<owner/repo>` from the intended repository's `git remote -v`: remove the host portion and any trailing `.git`.
   - When `gt auth status` lists no account for the repository's host, tell the user to run `gt auth login` first. When it lists several accounts on that host, add `--user <name>` for the one the user means.
   - When the user reports an unknown-flag error, take the flag names from the usage text in that error; their `gt` may differ from the one in the assistant's shell.

# Requirements

1. This skill only drafts and hands over the command. The user runs `gt issue create`; run it yourself only when the user explicitly says to.
2. Before handing the command over, confirm it carries `-R <owner/repo>` and that the `--body-file` path is the file you just wrote.
3. A wrong body on an issue that already exists is fixed with an edit. Find its number with `gt issue list -R <owner/repo> --state all --author @me`, then hand over `gt issue edit <n> -R <owner/repo> --body-file <root>/tmp/gt-issue-<slug>.md`, adding `gt issue reopen <n> -R <owner/repo>` if the user closed it. Leave running those to the user too.
