---
name: work-backend-qa
description: QA a backend issue implementation as a black box — confirms acceptance criteria and affected frontend features work, and describes any failures.
disable-model-invocation: true
---

# Backend QA

QA confirms that the feature works. Treat the implementation as a black box: exercise it and compare observed behavior against the acceptance criteria. QA is not a code review — do not report style, refactoring, or design improvements as findings.

When something fails, describe how it fails: inputs, steps, expected result, actual result. If you can trace the failure into the code, point to where it breaks with a file/line reference — that helps, but the failure description comes first.

The frontend is the measure. A failure that a user can hit in the frontend UI is a QA failure. A failure seen only through curl, Redis, the database or code reading is backend-only: it goes in its own section and never decides the verdict on its own.

If you notice something that could be improved but does not affect the functionality under test, put it in the report's Suggestions block. Do not create issues for suggestions; the user follows up on them.

## Workflow

1. Fetch the provided issue, including comments:

   ```sh
   tea i ISSUE_NUMBER --comments
   ```

   Extract the issue's acceptance criteria, implementation context, and any constraints from the issue and comments. When an earlier comment already reported QA failures, list each one: this run re-checks them first. Done when you hold the acceptance criteria and the list of previously reported failures (or know there are none).

2. Check whether the requested changes landed on the current branch. Inspect the branch diff and relevant history only to confirm each acceptance criterion has corresponding changes. Identify missing, partial, or unrelated changes.

3. Verify each acceptance criterion by exercising the backend behavior directly — call the endpoints, run the commands, or run the relevant tests — including error cases the criteria imply (invalid input, unauthorized access, missing data). Record the request/setup, the expected result, and the observed result.

4. Test every affected frontend feature in a browser.
   - Trace the changed backend contract through its consumers in `../frontend` to find the affected features.
   - Pick the frontend worktree: when the issue, its comments or a linked PR name a frontend branch the change depends on, use that branch's worktree (`wt list` in `../frontend`); otherwise use `../frontend` on `development`.
   - In that worktree, start the dev server with `mise run dev`, open a logged-in browser with `mise run pw-login`, and seed what the flow needs with the `seed:*` tasks (`mise tasks` lists them).
   - Exercise each affected flow, starting with the previously reported failures from step 1. Record the route, data, actions and observed result.
   - Close the playwright session and stop only the servers you started, by pid.

   Done when every affected feature has a recorded browser result, or a stated reason it cannot be reached from the UI.

5. Before reporting any failure, search the open issues of every repo the gap touches (`tea issues ls --state open` in this repo and in `../frontend`, plus `../frontend/.scratch/`), and read the likely matches with `tea i <n> --comments`. A gap that an open issue already covers is tracked work: cite the issue instead of reporting a failure. Done when every failure has been checked against the open issues.

6. Produce a final report that leads with the verdict:

   - **Verdict**: failures reproduced in the frontend, or "QA passes from the frontend; you can proceed" when there are none;
   - previously reported failures from step 1, each marked fixed or still failing;
   - failures reproduced in the frontend, ordered by severity, each with UI steps, expected vs. actual result, and a code location if you found one;
   - backend-only failures, labeled as not reproducible from the frontend, each with how it was observed;
   - whether the issue changes landed on this branch, and pass/fail for each acceptance criterion, with evidence;
   - gaps covered by open issues, with the issue numbers;
   - manual verification steps for each frontend failure (or each affected feature when nothing failed): the frontend branch to run, the seed command, each action and the expected result;
   - tests and checks run, including failures or environmental limitations;
   - a **Suggestions** block listing improvements that don't affect functionality, or omit it if there are none.

   Then offer to draft the issue comment with `/qa-issue-comment`.

Complete the workflow only after every acceptance criterion has been checked and every affected frontend feature has either been browser-tested or clearly documented as untestable with the reason.
