---
name: gt-plan-issue
displayName: Plan Forgejo issue to fix it
description: Get Forgejo issue information by using the provided issue id and the gt CLI and create a plan to fix it.
version: 2.0.0
tags: [forgejo, gt, issues, management, plan]
---

# Instructions
1. Read the issue and its comments with the `gt` CLI:
```bash
gt issue view <issue-id> --comments
```
   Ask the user when the issue id is uncertain. Done when the output shows the issue's title, body and every comment.
2. Create a step-by-step plan to fix the issue. Done when every ask in the issue and its comments maps to a step.
