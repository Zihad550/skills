---
name: work-pr-info
displayName: Work PR title and description
description: Draft a pull request title and body for a work repo, ready to paste into Forgejo.
disable-model-invocation: true
version: 1.0.0
tags: [forgejo, pull-requests, drafting]
---

# Work PR title and description

Draft one title and one body for a pull request the user opens themselves. Drafting is the whole job: creating the PR, pushing, and setting review state stay with the user.

1. Collect the change: the current branch name, `git log <default-branch>..HEAD --oneline`, and the diff behind those commits. Read every issue the branch name or the commit messages reference:

   ```bash
   zsh -ic "ti <issue-number>"
   ```

   Run it once per issue number. When no issue number appears anywhere, ask which issues this PR relates to. Done when the problem, the solution, and the full issue list are known.

2. Settle whether the PR is ready for review, asking the user when the conversation has not already said. Done when ready or not-ready is decided.

3. Draft the title: one line naming the change from the reader's side, specific enough to tell it apart from the other open PRs. Prefix `WIP: ` when step 2 landed on not ready. Done when the title names the actual change, and carries the prefix only in the not-ready case.

4. Draft the body: one short paragraph on the problem, one on the solution. Write plain text, full sentences, present tense, with numbered points when a list is needed. Skip em dashes, en dashes, hyphens as punctuation, and hyphenated compounds (write "per workspace", not "workspace-scoped"). Done when a reviewer who has not read the diff can say what was wrong and what the change does about it.

5. Close the body with one reference line per issue from step 1, each opening with `Refs` or `Related to`:

   ```text
   Refs #871
   ```

   Forgejo scans a PR body for the words close, closes, closed, fix, fixes, fixed, resolve, resolves and resolved in front of an issue reference, and merging the PR then closes that issue. The team wants those issues to survive the merge, so `Refs` and `Related to` are the two openings that belong here. Done when every issue appears exactly once and every reference line opens with one of those two.

6. Print the title and the body raw, with no blockquote markers, bold, or backticks wrapped around them, so the user copies them straight into Forgejo. Done when the output pastes as is.

7. Hand over the parts that live in the Forgejo UI, with the branch name and issue numbers filled in: link the PR branch to each issue from step 1, and request a new review after any push that follows an approval. Done when both are stated concretely.
