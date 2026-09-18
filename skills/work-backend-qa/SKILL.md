---
name: work-backend-qa
description: QA a backend issue implementation as a black box — confirms acceptance criteria and affected frontend features work, and describes any failures.
disable-model-invocation: true
---

# Backend QA

QA confirms that the feature works. Treat the implementation as a black box: exercise it and compare observed behavior against the acceptance criteria. QA is not a code review — do not report style, refactoring, or design improvements as findings.

When something fails, describe how it fails: inputs, steps, expected result, actual result. If you can trace the failure into the code, point to where it breaks with a file/line reference — that helps, but the failure description comes first.

If you notice something that could be improved but does not affect the functionality under test, put it in the report's Suggestions block. Do not create issues for suggestions; the user follows up on them.

## Workflow

1. Fetch the provided issue, including comments:

   ```sh
   tea i ISSUE_NUMBER --comments
   ```

   Extract the issue's acceptance criteria, implementation context, and any constraints from the issue and comments.

2. Check whether the requested changes landed on the current branch. Inspect the branch diff and relevant history only to confirm each acceptance criterion has corresponding changes. Identify missing, partial, or unrelated changes.

3. Verify each acceptance criterion by exercising the backend behavior directly — call the endpoints, run the commands, or run the relevant tests — including error cases the criteria imply (invalid input, unauthorized access, missing data). Record the request/setup, the expected result, and the observed result.

4. Determine which frontend features are affected by the change, if any. Inspect `../frontend` and trace the changed backend contract through its consumers. For every affected interactive feature, use the `playwright-cli` skill to exercise the relevant user flow in a browser — start the frontend dev server yourself first, `playwright-cli` does not manage it. Record the route, setup/data used, actions, and observed result.

5. Produce a final report containing:

   - whether the issue changes landed on this branch;
   - pass/fail for each acceptance criterion, with evidence;
   - failures, ordered by severity, each with reproduction steps, expected vs. actual result, and a code location if you found one — or an explicit statement that none were found;
   - the list of affected frontend features, or an explicit statement that none were affected;
   - manual verification steps for each affected frontend feature, so a human can re-verify independently of the browser run, including expected results;
   - tests and checks run, including failures or environmental limitations;
   - a **Suggestions** block listing improvements that don't affect functionality, or omit it if there are none.

Complete the workflow only after every acceptance criterion has been checked and every affected frontend feature has either been browser-tested or clearly documented as untestable with the reason.
