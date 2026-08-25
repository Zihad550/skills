# OpenCode background monitoring research

Checked against OpenCode's official documentation and `dev` source on 2026-08-25.

## Answer

OpenCode does not currently have a direct equivalent to Claude Code's persistent `Monitor(command: ..., persistent: true)` for arbitrary shell processes.

It has two related facilities, but neither replaces that monitor:

1. Experimental background subagents. The `task` tool accepts `background: true`, returns immediately, and injects a completion notification into the parent session. OpenCode requires `OPENCODE_EXPERIMENTAL_BACKGROUND_SUBAGENTS=true` for this path. This tracks an OpenCode child session, not an arbitrary process such as `ralph`. [Task tool source](https://github.com/anomalyco/opencode/blob/dev/packages/opencode/src/tool/task.ts#L20-L82)
2. Server-side session observation. `opencode serve` exposes `GET /session/status`, `GET /event` as a server-sent event stream, and asynchronous prompts. A separate controller can use these endpoints to watch OpenCode sessions. This requires running or attaching to a persistent OpenCode server and writing the controller. It does not make a standalone `opencode run` command into a persistent pushed process monitor. [Server documentation](https://opencode.ai/docs/server/)

The clearest evidence is in the current shell implementation. Its own TODO list says OpenCode still needs live progress metadata for long-running commands, persistent background-job status with restart recovery, owner-bound get/wait/cancel tools, completion delivery, and HTTP background-job observation. The bash tool otherwise waits for the process or times it out. [Bash tool source](https://github.com/anomalyco/opencode/blob/dev/packages/core/src/tool/bash.ts#L48-L79)

OpenCode's CLI supports `opencode run --attach <server>` and raw JSON events. That is useful if ralph is redesigned around a long-lived `opencode serve`, but it is session transport and output, not lifecycle supervision for an independently launched `ralph` process. [CLI documentation](https://opencode.ai/docs/cli/#run)

## Implications for `ralph-loop-implement`

The skill should not claim that OpenCode itself can arm the stall watch. Ralph launches `opencode run`; OpenCode is the workload being watched, not the outer supervisor. The existing `.ralph/current.log` line-count watcher remains the right portable signal for a stuck model stream.

The monitor choice belongs to the agent environment that is supervising ralph:

- Claude Code can use its persistent Monitor facility.
- Codex can keep a managed shell session open and receive incremental output.
- An agent running inside OpenCode has no native persistent arbitrary-process monitor today. It must use an external terminal multiplexer, a foreground shell call that the environment can keep alive, or a separate OS-level watcher whose output reaches the operator.

Starting the watch with `nohup`, `&`, or another detached shell technique does not satisfy the skill's definition of "armed". OpenCode has no native channel that forwards later output from that detached process to the active agent.

Native background subagents should not be recommended for the ralph stall watch. They are experimental, represent child agent sessions rather than shell jobs, and their tool prompt explicitly tells the parent not to poll. Ralph needs the opposite behavior: a long-lived observer that emits stall and completion edges.

## Recommended wording

Add this row to the harness table:

| Harness | Armed | Parked or unsupported |
|---|---|---|
| OpenCode | No native arbitrary-process monitor. Use Herdr or another external terminal/process supervisor whose events remain visible to the operator. | `bash` with `&` or `nohup`; experimental background subagents monitor child agent sessions, not ralph's process |

Add this note after the table:

> OpenCode's experimental `task(background: true)` is not a substitute for this watch. It tracks an OpenCode child session and sends a completion notification. The shell tool does not yet expose persistent background-job get, wait, cancel, or live-progress observation. If OpenCode is the supervising harness and Herdr is unavailable, say that the stall watch cannot be armed natively. Do not describe a detached watcher as armed.

This is intentionally conservative. OpenCode's server event stream could support a custom monitor later, but ralph does not currently launch `opencode run` through a persistent server/controller arrangement.
