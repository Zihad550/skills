---
name: linear-add-task
description: "Add a task to a Linear project from a short brief. Use when the user asks to add, create or file a Linear task or issue in a named project. Usage: /linear-add-task <project> <task details>."
---

# Linear add task

Turn the user's brief into one Linear task in the named project, written for a person to read.

## Arguments

- The first word is the project name, e.g. `dotfiles`.
- Everything after it is the task details, in the user's own words. With either one missing, ask for it.

## Steps

1. **Resolve the project.** `list_projects` with `query: <project>` and `fields: ["id", "name", "teams", "url"]`. Done when you hold one project and its team. When nothing matches, or several could, list the candidates and ask.

2. **Check for a duplicate.** `list_issues` with `project: <project>` and a `query` of the brief's key noun or two. Done when every open result has been compared with the brief. When one already covers it, give its identifier and URL and ask whether to update it instead.

3. **Write the task.**
   - **Title**: an imperative line naming the outcome, e.g. `Create a lazy-diff mod for Claude Code`.
   - **Description**: what the task is and why, in short sentences; a `## What it does` list of every ask in the brief; a `## Done when` checklist with one checkable item per ask.
   - **Agent notes**: implementation detail (files, commands, APIs, gotchas) goes in a collapsible section at the end, opened by `+++ Agent notes` and closed by `+++` on its own line. Explore the codebase or docs the brief names when that detail needs it.

   Done when every ask in the brief maps to a `Done when` item.

4. **Create it.** `save_issue` with `team`, `project`, `title` and `description`. Leave status, priority, labels and assignee unset unless the brief names them. Done when you print the identifier, title, status and URL in one line.
