---
name: work-ship
description: "Ship a committed work branch: push, open the PR from a work-pr-info draft, request review, and hand the issue to the reviewer. Also ships a review round: re-requests review from whoever asked for changes."
disable-model-invocation: true
---

# Work ship

Take a work branch from "committed" to "in review". Run every command against the branch's worktree path. The **reviewer** is the one the user names in the arguments, or else the PR reviewer the repo's `AGENTS.md` names; with neither, ask. The issue always goes to the reviewer.

A **review round** is a run on an open PR that has a review requesting changes. In a review round, review is re-requested from the **change requesters**: every user whose latest review on the PR is `REQUEST_CHANGES`, read in order from `gt api repos/<owner>/<repo>/pulls/<pr>/reviews`.

## Steps

1. **Check the branch.** Read the branch name, take the issue number from it (`jd-<n>-...` or `jd-<n>/...`), and run `git log origin/development..HEAD --oneline` and `git status --short`. Look for an open PR whose head is this branch with `gt pr list -R <owner>/<repo> --head <branch> --json number,title`. With an open PR, read its reviews and list the change requesters. Done when you hold the issue number, at least one commit ahead of `development`, a clean working tree, the open PR number or none, and, for an open PR, whether this is a review round and who the change requesters are. Stop and report when the tree has uncommitted changes or the branch has no commits.

2. **Draft the PR.** In a review round, compare the PR body with the commits pushed since the change request: when the body still describes the branch, keep it, say so in one line, and skip this step and step 4. Otherwise read `~/.agents/skills/work-pr-info/SKILL.md` and follow its steps 1 to 6; running inside this skill, the PR counts as ready for review unless the user said otherwise or the issue has a `Blocked by` section whose blocker has not shipped. Then draft it with a `WIP: ` title and ask whether to run steps 5 to 7 now or once the blocker ships (PR #967 was opened ready for review while backend#276 was unmerged, and the user stopped it with "should be draft"). Give the draft path and the title in one line, then stop until the user approves it or asks for changes. Done when the user has approved the title and `<root>/tmp/draft-pr-<n>.md` (`<root>` as work-pr-info defines it) as they stand.

3. **Push.** Run the push as one plain command, with nothing chained before or after it:

   ```bash
   git -C <path> push -u origin <branch>
   ```

   A chained push was denied in auto mode before any prompt appeared. Done when the remote branch matches `HEAD`.

4. **Open or update the PR.** Pass the approved draft file straight to `--body-file`, and run the command as one plain command with the title and path written out literally. With no open PR from step 1, create one:

   ```bash
   gt pr create -R <owner>/<repo> --base development --head <branch> --title "<title>" --body-file <root>/tmp/draft-pr-<n>.md
   ```

   With an open PR, run `gt pr edit <pr> -R <owner>/<repo>` with the same `--title` and `--body-file`. The body is the draft exactly, with no attribution line added. #973's command built the body file through a shell variable, and its permission prompt said "A variable in this command can't be checked before it runs". Done when the PR shows the approved title and the draft file's exact content.

5. **Request review.** Request the reviewer, or in a review round every change requester, through the reviewer field and leave the PR's assignees empty:

   ```bash
   gt api -X POST repos/<owner>/<repo>/pulls/<pr>/requested_reviewers -F 'reviewers=["<login>", ...]'
   ```

   Done when each requested user's latest entry in `gt api repos/<owner>/<repo>/pulls/<pr>/reviews` is `REQUEST_REVIEW` and `gt pr view <pr> -R <owner>/<repo> --json assignees` is empty. `gt pr view --json reviews` leaves `REQUEST_REVIEW` entries out, so read them from the API. Forgejo keeps a change requester under `requested_reviewers` after their review, so that field cannot tell a re-request happened (PR #939 listed @timos there before the re-request).

6. **Hand the issue over** with the dotfiles helpers, each run as its own plain command so the permission prompt shows one short line:

   ```bash
   df-gt-set-issue-label <n> "status/ready for review" -R <owner>/<repo>
   df-gt-set-assignee <n> <reviewer> -R <owner>/<repo> --ref refs/heads/<branch>
   ```

   The label helper swaps the old `status/*` label and keeps every other label. `--ref` sets the issue sidebar's Branch/Tag picker. To drop one assignee and keep the rest, use `df-gt-remove-assignee <n> <login> -R <owner>/<repo>`. Done when the issue carries `status/ready for review`, the reviewer as its only assignee, and `ref` set to the branch.

7. **Move the Linear task** to `In Review` by following `~/.agents/skills/work-status/SKILL.md`. Done when it prints the task's old and new status, or the task was already `In Review`.

8. **Report.** In one list: the PR URL, who was requested for review (re-requested, in a review round), the issue's new label and assignee, and the Linear move. Then hand over work-pr-info's step 7 items, minus the jobs this skill already did. Done when every item work-pr-info kept out of the body is named with where it would live.
