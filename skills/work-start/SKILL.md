---
name: work-start
description: "Start work on an issue or a PR: read it, reuse its worktree or create one, and brief the asks. Usage: /work-start <issue> or /work-start pr <pr>."
disable-model-invocation: true
---

# Work start

Put the session in the right worktree with the full picture of what is asked, and stop before implementing. Run every `wt` and `tea` command from the repo the user is in; `wt` acts on the clone, so any worktree of it works.

## Steps

1. **Parse the target.** `pr <n>` (or a PR URL) is a pull request; a bare number is an issue. Done when you hold one number and its kind. Without a number, ask for one.

2. **Read it.**
   - Issue: `tea issue <n> --comments -o simple`. When the output shows the number is a pull request, switch to the PR branch of every later step.
   - PR: `df-tpr <n>` for comments, inline review comments, and review bodies. Then read its state and head branch with `tea pulls ls --state all --limit 200 --fields index,state,head,title -o simple | awk '$1 == <n>'`, and read each issue its body lists under `resolves:` or `Related to`.

   When the issue or PR has an image you cannot fetch, ask the user to paste it. Done when every ask, every unresolved review comment, and every linked issue has been read.

3. **Find existing work.** List the worktrees with `wt list --format=json` and the open PRs with `tea pulls ls --state all --limit 200 --fields index,state,head,title -o simple`.
   - Issue: a candidate is a worktree or PR whose branch starts with `jd-<n>` (either `jd-<n>-` or `jd-<n>/`), or a PR whose body resolves `#<n>`.
   - PR: the candidate is the worktree whose `branch` equals the PR's head branch.

   Done when each candidate is classified as open (its PR is open, or it has no PR yet) or merged.

4. **Choose the worktree.**
   - **Open candidate exists**: reuse it. Fetch, and when its `working_tree` is clean and it is only behind its remote, fast-forward it with `git -C <path> pull --ff-only`; otherwise report the ahead, behind, and dirty state without touching it.
   - **PR head branch with no worktree**: create one for the existing branch with `wt switch <head-branch> --no-cd`.
   - **Nothing open** (no candidate, or only merged ones, which means follow-up work on a merged PR): draft a new branch name by reading `~/.agents/skills/work-branch-name-gen/SKILL.md` and following its steps, then create it with `wt switch -c <name> --no-cd`. When an earlier branch for this issue was merged, say so, and name it in the brief.

   Done when `wt list --format=json` shows the chosen branch with its path, and you state that path. Every later read, edit, and command in this session runs against that path.

5. **Brief.** Print, for the chosen worktree:
   - the asks as a checklist, each with who asked and where (issue body, comment, review comment with file and line);
   - for a PR, which review comments are still unresolved;
   - the open questions only the user or the team can answer (copy, expected behaviour, scope), with the issue's own wording quoted when it already answers one.

   Then stop and wait for the user to say how to proceed. Done when the brief is printed and no file in the worktree has changed.
