---
name: create-skill
description: Author a new agent skill in the user's own skills repo and roll it out everywhere.
disable-model-invocation: true
---

# Create a skill

Ship a new skill end to end: authored in `~/dev/src/github.com/Zihad550/skills`, pushed, registered in the dotfiles installer, and installed globally for every agent. A skill that exists only on disk is not shipped — every step below runs.

Use the name the user gave. Absent one, propose a kebab-case name from the skill's job and confirm it before step 1.

## 1. Scaffold

```bash
cd ~/dev/src/github.com/Zihad550/skills/skills && skills init <name>
```

Done when `skills/<name>/SKILL.md` exists with the CLI's placeholder frontmatter.

## 2. Write it

Invoke the `writing-for-agents` skill and write `SKILL.md` under its rules — description as context pointer, steps with checkable completion criteria, reference disclosed behind pointers rather than piled inline.

Done when every placeholder line the CLI wrote is gone and the frontmatter `name` matches the directory.

## 3. Scrub sensitive information

Inspect every file under `skills/<name>` before staging it. Remove credentials and sensitive information copied from prompts, terminals, configuration, examples, logs, or source material. This includes API keys, access tokens, passwords, private keys, session cookies, connection strings, account identifiers, and private endpoints. Replace values needed for instruction or examples with descriptive placeholders such as `<API_TOKEN>` or environment-variable references.

Review the complete diff and run the repository's secret scanner when one is configured. Treat suspected secrets as sensitive until verified otherwise.

Done when the new skill contains no real credentials or sensitive values and its examples remain usable with placeholders.

## 4. Commit and push the skill

```bash
cd ~/dev/src/github.com/Zihad550/skills && git add skills/<name> && git commit && git push
```

Conventional Commits, matching the log's existing style (`feat: add <thing> skill`). Push before step 6 — `skills add` installs from GitHub, so an unpushed skill installs as nothing.

## 5. Register it in the installer

`~/dotfiles/setup/common/setup-skills` is a separate repo. Add `<name>` to the `--skill` list on the `skills add Zihad550/skills` invocation, keeping that list alphabetical, then commit and push the dotfiles repo.

Done when the skill name appears in that list and `git status` in `~/dotfiles` is clean.

## 6. Install globally

Read the `AGENTS` array from `~/dotfiles/setup/common/setup-skills` — it is the source of truth for install targets — and run from `~`:

```bash
cd ~ && skills add Zihad550/skills --skill <name> -g --agent <agents from AGENTS> -y
skills update -g
```

Done when `skills list` shows the new skill installed for each agent in `AGENTS`.
