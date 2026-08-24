# The operator skill ships here; the prompt the loop drives does not

Two prompts came out of building the ralph loop, and only one of them is a skill.

`ralph-loop-implement` is the **operator** prompt: how to preflight a queue, start the loop,
read `.ralph/state.json`, tell a healthy run from a wedged one, and interpret a
parked issue. A person asks an agent for that — "work through the queue", "what is
ralph doing" — so it belongs in this repo, where the `skills` CLI installs it to
every agent at once from one line in `dotfiles/setup/common/setup-skills`.

`implement-issue` is the **implementer** prompt: what the agent inside a single
loop iteration should do with one ticket. Nobody invokes it by hand; `ralph` passes
it to `opencode run --command`, which takes a command, not a skill. It stays in the
ralph-loop repo as `opencode/command/implement-issue.md` and is installed by that
project's `install.sh`. Publishing it here as well would put a prompt in front of
five agents that none of them are ever meant to choose.

## Consequences

The split is by **who invokes it**, not by subject matter. Both prompts are about
the same loop; that is not a reason to ship both, and a future prompt that only a
runner ever passes to a subprocess does not belong here either.

The operator skill now lives in a different repo from the tool it documents, so a
change to ralph's flags or state files can ship without its skill following. The
skill is written to survive that — it names commands and files rather than
restating implementation detail — but drift is the standing cost, and a ralph
change that alters the supervision surface has to be mirrored here by hand.

Removing `implement-issue` from this repo does not remove it from the machine: it
remains an opencode command, and it is what actually does the work. Anyone reading
this repo for "how does ralph implement an issue" will not find the answer here,
which is why this record says where it went.
