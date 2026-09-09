---
name: work-branch-name-gen
description: Draft a work branch name from one or more issue numbers.
disable-model-invocation: true
---

# Work branch name generator

Turn the issue numbers passed with the invocation into one proposed branch or worktree name.

1. Parse the arguments as one or more decimal issue numbers. Accept spaces or commas between numbers and preserve their input order. If any argument is not a decimal issue number, ask for corrected input. Done when the ordered issue-number list is unambiguous.

2. Fetch every issue with the user's interactive Zsh environment:

   ```bash
   zsh -ic "ti <issue-number>"
   ```

   Run the command once per issue, replacing `<issue-number>` with the validated decimal number. If a command fails or does not return issue details, report which issue could not be read and stop. Done when details are available for every issue.

3. Derive a short kebab-case description of the work from the issue titles and details. Describe the outcome, not the full issue title. For multiple issues, describe their shared outcome rather than concatenating their titles. Aim for 3 to 6 words and 20 to 50 characters. Done when the description is specific and contains only lowercase ASCII letters, digits, and hyphens.

4. Draft exactly one name in this format:

   ```text
   jd-<issue-number>[_<additional-issue-number>...]/<description>
   ```

   Join multiple issue numbers with `_` after the single `jd-` prefix. Prefer a complete name under 80 characters. If the issue-number prefix is long, keep every issue number and shorten the description. Return the proposed name with a one-sentence rationale. Done when every fetched issue number appears once, in input order, and the name matches the format.

   Good examples:

   ```text
   jd-230/fix-payment-timeout
   jd-230_231/add-invoice-validation
   ```

   Too long:

   ```text
   jd-230/fix-the-problem-where-payment-processing-times-out-for-some-users
   ```
