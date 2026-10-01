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

5. **Print it** under Output. Done when the draft copies out of the terminal as is.

## Shape

- **Lead with the point**: the finding, the decision, or the question. Then the exact evidence (the error text, the observed result). Then the question or the next step. Nothing else: side notes, alternatives nobody asked about, and test narration stay out unless the user asks for them.
- **Compact means fewer words**, not a different layout. Default to two to four sentences. With several points, one sentence each, as numbered points.
- **Ask to verify, never to announce.** A question for the team asks what the expected behaviour is; it does not describe what the user built. When offering options, put each option on its own line.
- **Disagreeing with a reviewer**: state the consequence of their suggestion ("if we apply your fix, two workspaces can share one ad account") and ask how they want to handle it.
- **Proposing work**: say what we can do and what it improves, in that order.
- **Tagging**: tag a person (`@name`) only when the user asks, using the username from tea output rather than a display name.

## Plain text

The message reads as plain prose a person typed:

- Full sentences, or numbered points when a list is needed.
- Commas, colons, or a new sentence where a dash would go; no em dashes, en dashes, hyphens used as punctuation, or dash bullets.
- Open compounds ("per workspace", not "workspace-scoped").
- No blockquote markers, bold, or headings wrapped around the draft.

For a draft that goes to Forgejo (PR comment, issue comment, review reply), wrap every HTML tag in inline backticks (`<script setup>`), because a raw tag is swallowed when pasted into Forgejo.

## Output

- A draft with no backticks prints raw.
- A draft containing backticks prints inside one fenced code block. The terminal renders markdown, so bare backticks turn into code styling and vanish from the text the user copies.
- For a Forgejo comment, also write the draft to `/tmp/tea-comment-<number>.md` and give the one-line command that posts it, for the user to run. Resolve `<owner/repo>` from the repo's `git remote -v` and `<login>` from `tea login ls`; `$(<file)` reads the file without a `cat` alias getting in the way:

  ```bash
  tea comment <number> -l <login> -r <owner/repo> "$(</tmp/tea-comment-<number>.md)"
  ```
