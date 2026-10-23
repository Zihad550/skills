---
name: work-ship
description: "Ship a committed work branch: push, open the PR from a work-pr-info draft, request review, and hand the issue to the reviewer."
disable-model-invocation: true
---

# Work ship

Take a work branch from "committed" to "in review". Run every command against the branch's worktree path. The reviewer is the one the user names in the arguments, or else the PR reviewer the repo's `AGENTS.md` names; with neither, ask.

## Steps

1. **Check the branch.** Read the branch name, take the issue number from it (`jd-<n>-...` or `jd-<n>/...`), and run `git log origin/development..HEAD --oneline` and `git status --short`. Look for an open PR whose head is this branch with `tea pulls ls --state open --limit 200 --fields index,state,head,title -o simple`. Done when you hold the issue number, at least one commit ahead of `development`, a clean working tree, and the open PR number or none. Stop and report when the tree has uncommitted changes or the branch has no commits.

2. **Draft the PR.** Read `~/.agents/skills/work-pr-info/SKILL.md` and follow its steps 1 to 6; running inside this skill, the PR counts as ready for review unless the user said otherwise. Give the draft path and the title in one line, then stop until the user approves it or asks for changes. Done when the user has approved `/tmp/draft-pr-<n>.md` as it stands.

3. **Push.** Run the push as one plain command, with nothing chained before or after it:

   ```bash
   git -C <path> push -u origin <branch>
   ```

   A chained push was denied in auto mode before any prompt appeared. Done when the remote branch matches `HEAD`.

4. **Open or update the PR.** Write the draft's body, everything after its title and blank line, to a scratchpad file. With no open PR from step 1, create one:

   ```bash
   tea pr create --repo <owner>/<repo> --base development --head <branch> --title "<title>" --description-file <body-file>
   ```

   With an open PR, run `tea pr edit <pr> --repo <owner>/<repo>` with the same `--title` and `--description-file`. The body is the draft exactly, with no attribution line added. Done when the PR shows the draft's title and body.

5. **Request review.** Request the reviewer through the reviewer field and leave the PR's assignees empty:

   ```bash
   tea api -X POST /repos/<owner>/<repo>/pulls/<pr>/requested_reviewers -d '{"reviewers":["<reviewer>"]}'
   ```

   Done when `tea api /repos/<owner>/<repo>/pulls/<pr>` lists the reviewer under `requested_reviewers` and no assignees.

6. **Hand the issue over.** Add the status label by name with `POST`, which drops the old `status/*` label and keeps every other label; `PUT` on that route replaces them all:

   ```bash
   tea api -X POST /repos/<owner>/<repo>/issues/<n>/labels -d '{"labels":["status/ready for review"]}'
   tea api -X PATCH /repos/<owner>/<repo>/issues/<n> -d '{"assignees":["<reviewer>"]}'
   ```

   Done when the issue carries `status/ready for review` and the reviewer as its only assignee.

7. **Move the Linear task** to `In Review` by following `~/.agents/skills/work-status/SKILL.md`. Done when it prints the task's old and new status, or the task was already `In Review`.

8. **Report.** In one list: the PR URL, the reviewer, the issue's new label and assignee, and the Linear move. Then hand over work-pr-info's step 7 items, minus the jobs this skill already did. Done when every item work-pr-info kept out of the body is named with where it would live.
