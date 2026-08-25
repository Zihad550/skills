# Ralph supervision uses a base skill and adapters

The reusable `ralph-loop` operator skill owns bounded OpenCode execution,
verification, monitoring, stall detection, and process placement for arbitrary
tasks. Workflow-specific operator skills such as `ralph-loop-implement` load
that base and add only selection, state, and completion rules for their workflow.
This keeps supervision in one source of truth while allowing users to run Ralph
against work other than GitHub issues.

The `/implement-issue` prompt remains in the ralph-loop project at
`opencode/command/implement-issue.md`. It is an implementer command invoked by
the runner, not an operator skill chosen by a user.
