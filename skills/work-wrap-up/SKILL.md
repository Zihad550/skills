---
name: work-wrap-up
description: "Finish a work branch: spec check, code review, the repo's loop, browser test, manual steps, stage, then offer the commit message and PR body."
disable-model-invocation: true
---

# Work wrap-up

Take the current branch from "code written" to "staged and ready for the user to commit". Each step ends at a gate; the user decides what gets fixed, what gets committed, and what gets opened as a PR.

## Steps

1. **Collect the change.** Read the branch diff against the merge base with the default branch, plus uncommitted changes: `git diff $(git merge-base HEAD origin/development)` and `git status --short`. Take the issue number from the branch name (`jd-<n>`) and read the issue with `df-ti <n>`. When an open PR exists for the branch, also read its review comments with `df-tpr <pr>`. Done when you hold the changed file list, every ask from the issue, and every unresolved review comment.

2. **Spec check.** Map every ask from step 1 to the change that satisfies it. Report each one as met, partial, or missing, with the file and line. Done when no ask is left unmapped. Stop and ask before going on when anything is partial or missing.

3. **Code review.** Invoke the `code-review` skill with the merge base from step 1 as the fixed point. Present its findings numbered, then let the user answer each one (fix, explain more, or leave). Apply exactly the fixes the user accepts. Done when every finding has the user's answer and every accepted fix is applied.

4. **The loop.** Run the loop the repo's `AGENTS.md` names (`mise run blc` in the frontend) until it is green. When it is red on a file this branch does not touch, follow that `AGENTS.md`'s instructions for checking `development` and running the remaining checks on their own. Done when the loop is green, or red only on lines `development` shares, with the evidence shown.

5. **Browser test.** When the change is user-facing, log in with `mise run pw-login` from the frontend worktree, seed what the test needs with the `seed:*` tasks, and exercise every screen the diff touches. Then exercise the neighbouring features those screens share code with (for a composer change: save, publish, schedule, duplicate). Record each flow and its result. Close the playwright session and stop only the servers you started. Done when every touched screen and its neighbours have a recorded result, or the change is not user-facing and you say why.

6. **Manual steps.** Print numbered steps a person can follow to verify the change in the UI: the seed command or link they need, each action, and the expected result. Done when every ask from step 2 has a step that proves it.

7. **Stage.** Stage only the files this change touched, by path (`git add <paths>`), and list them with one line each on why. Done when `git diff --cached --stat` shows exactly the change and nothing unrelated.

8. **Offer the write-ups.** Ask in one line whether to draft the commit message and the PR body, then stop. On a yes, draft the commit message with the `caveman-commit` skill (ending `Refs: #<issue>`), then draft the PR body by reading `~/.agents/skills/work-pr-info/SKILL.md` and following its steps. Done when the user has answered, and anything they said yes to is printed.
