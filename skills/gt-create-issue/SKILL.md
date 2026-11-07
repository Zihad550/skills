---
name: gt-create-issue
displayName: Create Forgejo issue
description: Create a Forgejo issue by using user provided instructions and also by exploring the current codebase.
version: 2.0.0
tags: [forgejo, gt, issues, management]
---
# Instructions
1. Draft only a title and a body for the issue, and write the body to a scratchpad file. When either is unclear, explore the codebase and ask the user follow-up questions. Use present tense for verbs: update, create, fix. Done when the body file exists and no question is left open.
2. Show the draft and ask whether the user wants changes. Done when the user says to proceed.
3. Create the issue with the `gt` CLI and stop:
```bash
gt issue create -R <owner/repo> --title "<title>" --body-file <body-file>
```
Take `<owner/repo>` from `git remote -v`. Done when `gt` prints the new issue's URL.
