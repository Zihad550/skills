---
name: work-draft-reply
description: Draft a message a person will read, for the user to send. Use when asked to draft or write a reply to a PR review or comment, an issue comment, a question for a teammate, or a chat message to the team.
---

# Work draft reply

Write one message the user sends themselves. Drafting is the whole job: the working tree stays exactly as it is, and the message is posted only when the user asks you to post it.

## Steps

1. **Read the thread.** Read what the message answers, in full: the PR's review comments and review bodies (`df-tpr <pr>`), the issue and its comments (`df-ti <issue>`), or the text the user pasted. When the thread has an image you cannot fetch, ask the user to paste it. Done when you can state, in one sentence each, what the other person asked or claimed and what the user wants to say back.

2. **Check every claim.** List each factual claim the draft will make (what the code does, what a test showed, what the other person's fix would cause). Confirm each one against code you read or output you ran in this session, and run what is missing. Drop any claim you cannot confirm. Done when every claim in the draft has a source you can point to.

3. **Write the draft** in the shape below. Done when the draft fits the shape and every rule under Plain text holds.

4. **Polish.** Read `~/.agents/skills/unslop/SKILL.md` and apply it to the draft. Done when a reread finds none of its patterns.

5. **Save it** under Output. Done when the draft file exists and the chat reply holds no copy of it.

## Shape

- **Lead with the point**: the finding, the decision, or the question. Then the exact evidence (the error text, the observed result). Then the question or the next step. Nothing else: side notes, alternatives nobody asked about, and test narration stay out unless the user asks for them.
- **Compact means fewer words**, not a different layout. Default to two to four sentences. With several points, one sentence each, as numbered points.
- **Answer only what was asked**, one sentence per question, and leave out status the user didn't ask to share (what is local, pushed, or not yet a PR). A #938 reply to a reviewer went from three paragraphs to one sentence after the user cut it.
- **Ask to verify, never to announce.** A question for the team asks what the expected behaviour is; it does not describe what the user built. When offering options, put each option on its own line.
- **Disagreeing with a reviewer**: state the consequence of their suggestion ("if we apply your fix, two workspaces can share one ad account") and ask how they want to handle it.
- **Proposing work**: say what we can do and what it improves, in that order.
- **Tagging**: tag a person (`@name`) when the message asks them a question or needs their decision, and otherwise only when the user asks, using the username from gt output rather than a display name. PR #982's question to the reviewer went untagged and the user stopped the post to add it.

## Plain text

The message reads as plain prose a person typed:

- Full sentences, or numbered points when a list is needed.
- Commas, colons, or a new sentence where a dash would go; no em dashes, en dashes, hyphens used as punctuation, or dash bullets.
- Open compounds ("per workspace", not "workspace-scoped").
- No blockquote markers, bold, or headings wrapped around the draft.

For a draft that goes to Forgejo (PR comment, issue comment, review reply), wrap every HTML tag in inline backticks (`<script setup>`), because a raw tag is swallowed when pasted into Forgejo.

## Output

Write the draft to `<root>/tmp`, where `<root>` is the session's project root: where the session started, or where `/cd` or a worktree move took it; create `tmp/` when it is missing. Use it even when the session names a scratchpad directory: the user reads and copies the draft through the `/drafts` panel, which reads only `<root>/tmp`. Leave the draft out of the chat reply. Reply with the file's absolute path and one line saying what the draft says.

- For a Forgejo comment on an issue or a PR, write it to `<root>/tmp/gt-comment-<number>.md` and give the command that posts it, for the user to run. Resolve `<owner/repo>` from the repo's `git remote -v`:

  ```bash
  gt issue comment <number> -R <owner/repo> --body-file <root>/tmp/gt-comment-<number>.md
  ```

- For anything else (a chat message, a question for a teammate), write it to `<root>/tmp/draft-<slug>.md`, where `<slug>` is a short kebab-case name for the topic.
