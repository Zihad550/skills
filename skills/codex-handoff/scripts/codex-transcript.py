#!/usr/bin/env python3
"""Print a Codex CLI session as a readable transcript.

Usage: codex-transcript.py <session-id-or-prefix> [--tail N]

Finds ~/.codex/sessions/**/rollout-*<id>*.jsonl and prints the working
directory, then user prompts, assistant messages and tool calls in order.
Injected AGENTS.md and skill listings are skipped. --tail keeps the last N
entries (default: all).
"""
import glob
import json
import os
import sys

INJECTED = ("# AGENTS.md instructions", "<skills_instructions>", "<environment_context>",
            "<user_instructions>", "<permissions instructions>")


def text_of(content):
    return "\n".join(c.get("text", "") for c in content or [] if isinstance(c, dict))


def clip(s, n):
    s = s.strip()
    return s if len(s) <= n else s[:n] + " …"


def main():
    args = sys.argv[1:]
    if not args:
        sys.exit(__doc__)
    tail = None
    if "--tail" in args:
        i = args.index("--tail")
        tail = int(args[i + 1])
        del args[i:i + 2]
    sid = args[0].strip().strip("\"'")
    files = glob.glob(os.path.expanduser(f"~/.codex/sessions/**/rollout-*{sid}*.jsonl"), recursive=True)
    if not files:
        sys.exit(f"no Codex session matches {sid}")
    if len(files) > 1:
        sys.exit("several sessions match; pass more of the id:\n" + "\n".join(files))

    entries, cwd = [], None
    for line in open(files[0]):
        try:
            o = json.loads(line)
        except json.JSONDecodeError:
            continue
        p = o.get("payload") or {}
        if o.get("type") == "session_meta":
            cwd = p.get("cwd")
        if o.get("type") != "response_item":
            continue
        kind = p.get("type")
        if kind == "message" and p.get("role") in ("user", "assistant"):
            t = text_of(p.get("content"))
            if p["role"] == "user" and (not t.strip() or t.lstrip().startswith(INJECTED)):
                continue
            entries.append(f"[{p['role']}] {clip(t, 4000)}")
        elif kind == "custom_tool_call":
            entries.append(f"[tool {p.get('name')}] {clip(p.get('input', ''), 600)}")
        elif kind == "function_call":
            entries.append(f"[tool {p.get('name')}] {clip(p.get('arguments', ''), 300)}")
        elif kind == "agent_message":
            entries.append(f"[subagent {p.get('author')}] {clip(text_of(p.get('content')), 1500)}")

    print(f"session: {files[0]}\ncwd: {cwd}\n")
    for e in entries[-tail:] if tail else entries:
        print(e, end="\n\n")


main()
