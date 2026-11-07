---
name: gt-get-issue
displayName: Get Forgejo issue information
description: Get Forgejo issue information by using the provided issue id and the gt CLI
version: 2.0.0
tags: [forgejo, gt, issues, management]
---

# Instructions
1. Read the issue and its comments with the `gt` CLI:
```bash
gt issue view <issue-id> --comments
```
   Ask the user when the issue id or repository is uncertain; `-R <owner/repo>` selects a repository other than the current clone's. Done when the output shows the issue's title, body and every comment.
2. Summarize the issue and ask the user what they want to do with it. Done when the user has the summary and the question.
