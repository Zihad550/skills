# The unattended implement contract lives here as a skill, and is mirrored as an opencode command

`implement-issue` describes how an agent takes one GitHub issue from ticket to
closed with nobody watching: read the issue and the project's own rules, build
only what was asked, run the checks the repo actually defines, then commit and
close — or leave the issue open with the reason it stalled. That contract is the
valuable part, and it belongs in this repo, where the `skills` CLI installs it to
every agent at once (Claude Code, Cursor, Codex, Pi, Kilo Code) from a single
line in `dotfiles/setup/common/setup-skills`.

The ralph loop drives the same contract through `opencode run --command`, which
takes a **command**, not a skill — so a second copy of these instructions lives
in the ralph-loop repo as `opencode/command/implement-issue.md`. Two files, one
contract, deliberately.

## Consequences

The copies drift unless someone mirrors them. A change to how unattended work is
verified, committed, or closed has to land in both
`skills/implement-issue/SKILL.md` here and `opencode/command/implement-issue.md`
in ralph-loop. That is the price of the loop being able to invoke it
non-interactively; collapsing them would mean giving up either the multi-agent
install or the unattended invocation.

The skill is written for an agent with no human in the loop, which makes it
blunter than a skill a person invokes by hand: it forbids `git add -A`, forbids
claiming an unrun check, and states outright that an honest blocked issue beats a
false close. Those rules read as over-specified when a human is supervising. They
are not aimed at that case.

Verification is discovered, not declared — `package.json` scripts, `mise.toml`,
`Makefile`, or the language default. The skill therefore works in a repo it has
never seen, and gets the checks wrong in a repo that hides them somewhere unusual.
A project that needs different instructions overrides the command locally with its
own `.opencode/command/implement-issue.md`, which opencode prefers over the global
one; routebook does exactly that.
