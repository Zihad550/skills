---
name: ww-worktree
description: Draft a branch or worktree name from one or more issue numbers.
disable-model-invocation: true
---

# WW worktree

Turn the issue numbers passed with the invocation into one proposed branch or worktree name.

1. Parse the arguments as one or more decimal issue numbers. Accept spaces or commas between numbers and preserve their input order. If any argument is not a decimal issue number, ask for corrected input. Done when the ordered issue-number list is unambiguous.

2. Fetch every issue with the user's interactive Zsh environment:

   ```bash
   zsh -ic "ti <issue-number>"
   ```

   Run the command once per issue, replacing `<issue-number>` with the validated decimal number. If a command fails or does not return issue details, report which issue could not be read and stop. Done when details are available for every issue.

3. Derive a short kebab-case description of the work from the issue titles and details. For multiple issues, describe their shared outcome rather than concatenating their titles. Done when the description is specific, concise, and contains only lowercase ASCII letters, digits, and hyphens.

4. Draft exactly one name in this format:

   ```text
   us-<issue-number>[_<additional-issue-number>...]/<description>
   ```

   Join multiple issue numbers with `_` after the single `us-` prefix. For example, issues 230 and 231 become `us-230_231/fix-things`; issue 230 alone becomes `us-230/fix-things`. Return the proposed name with a one-sentence rationale. Done when every fetched issue number appears once, in input order, and the name matches the format.
