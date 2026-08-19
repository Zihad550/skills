---
name: work-backend-qa
description: QA a backend issue implementation by checking the issue, branch changes, frontend impact, browser behavior, and implementation bugs. Use when validating whether a backend issue is complete and safe to ship.
---

# Backend QA

Validate a backend issue implementation and report both defects and affected frontend behavior.

## Workflow

1. Fetch the provided issue, including comments:

   ```sh
   tea i ISSUE_NUMBER --comments
   ```

   Extract the issue’s acceptance criteria, implementation context, and any constraints from the issue and comments.

2. Check whether the requested changes landed on the current branch. Inspect the branch diff and relevant history, then map each acceptance criterion to concrete code or tests. Identify missing, partial, or unrelated changes.

3. Determine which frontend features are affected by the change, if any. Inspect `../frontend` and trace the changed backend contract through its consumers. For every affected interactive feature, use the `/webapp-testing` skill to exercise the relevant user flow in a browser. Record the route, setup/data used, actions, and observed result.

4. Look for implementation bugs. Review error handling, validation, authorization, persistence, backwards compatibility, race conditions, and test coverage. Run focused tests and other relevant checks available in the repository. Report concrete findings with severity, evidence, and file/line references.

5. Produce a final report containing:

   - whether the issue changes landed on this branch;
   - bugs and risks, ordered by severity, or an explicit statement that none were found;
   - the list of affected frontend features, or an explicit statement that none were affected;
   - manual verification steps for each affected frontend feature, including expected results;
   - tests and checks run, including failures or environmental limitations.

Complete the workflow only after every acceptance criterion has been checked and every affected frontend feature has either been browser-tested or clearly documented as untestable with the reason.
