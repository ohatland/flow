#!/usr/bin/env python3
"""Observed record of what a subagent did, read from its transcript.

Usage: trace.py <agent-id> [--out <file>]
Finds ~/.claude/projects/*/*/subagents/agent-<agent-id>.jsonl (a resumed agent appends to
the same file). Prints a short TRACE summary; --out also writes the full detail there.
"""
import collections
import glob
import json
import os
import re
import sys
from datetime import datetime

BASH_WRITE = re.compile(r"(sed -i|\btee\b|\bmv\b|\bcp\b|\brm\b|>>?\s*(?!/dev/null|&)[^\s|&]+)")
PIPED_GATE = re.compile(r"\|\s*(tail|head|grep|tee)\b")
# The gate wrote to a file and its exit code was read before anything was piped.
EXIT_BEFORE_PIPE = re.compile(r">\s*\S+[^|;]*;\s*echo[^|;]*\$\?")
BUILD_TEST = re.compile(r"(\.flow/check|\b(dotnet (build|test|format)|(npm|pnpm|yarn|bun) (run|test)|npx|bunx|pytest|cargo (build|test)|go (build|test)|make|playwright test)\b)")


def find(agent_id):
    agent_id = agent_id.removeprefix("agent-")
    hits = glob.glob(os.path.expanduser(f"~/.claude/projects/*/*/subagents/agent-{agent_id}.jsonl"))
    if not hits:
        sys.exit(f"no transcript for agent {agent_id}")
    return max(hits, key=os.path.getmtime)


def short(value, n=110):
    text = value if isinstance(value, str) else json.dumps(value, ensure_ascii=True)
    text = " ".join(text.split())
    return text if len(text) <= n else text[: n - 3] + "..."


def call_label(name, inp):
    if name == "Bash":
        if inp.get("description"):
            return short(f"{inp['description']}: {inp.get('command', '')}")
        return short(inp.get("command", ""))
    for key in ("file_path", "pattern", "path", "query", "url", "skill", "prompt"):
        if key in inp:
            return short(inp[key])
    return short(inp)


def result_text(content):
    if isinstance(content, list):
        return " ".join(c.get("text", "") for c in content if isinstance(c, dict))
    return content or ""


def main():
    args = sys.argv[1:]
    out = None
    if "--out" in args:
        i = args.index("--out")
        out = args[i + 1]
        del args[i : i + 2]
    if len(args) != 1:
        sys.exit(__doc__)

    path = find(args[0])
    meta_path = path[: -len(".jsonl")] + ".meta.json"
    agent_type = "?"
    if os.path.exists(meta_path):
        with open(meta_path) as f:
            agent_type = json.load(f).get("agentType", "?")

    calls = {}
    order = []
    usage_by_msg = {}
    stamps = []
    dispatches = 0
    with open(path) as f:
        for line in f:
            try:
                entry = json.loads(line)
            except json.JSONDecodeError:
                continue
            if ts := entry.get("timestamp"):
                stamps.append(ts)
            msg = entry.get("message") or {}
            content = msg.get("content")
            if entry.get("type") == "assistant":
                if msg.get("id") and msg.get("usage"):
                    usage_by_msg[msg["id"]] = msg["usage"]
                for block in content or []:
                    if block.get("type") == "tool_use":
                        calls[block["id"]] = {"name": block["name"], "input": block.get("input", {}), "error": None}
                        order.append(block["id"])
            elif entry.get("type") == "user":
                if isinstance(content, str):
                    dispatches += not content.startswith("<system-reminder>")
                    continue
                for block in content or []:
                    if block.get("type") != "tool_result" or block.get("tool_use_id") not in calls:
                        continue
                    text = result_text(block.get("content"))
                    if block.get("is_error") or re.match(r"Exit code [1-9]", text):
                        calls[block["tool_use_id"]]["error"] = short(text.splitlines()[0] if text else "error", 140)

    contexts = [u.get("input_tokens", 0) + u.get("cache_read_input_tokens", 0) + u.get("cache_creation_input_tokens", 0)
                for u in usage_by_msg.values()]
    by_tool = collections.Counter(calls[c]["name"] for c in order)
    errors = [calls[c] for c in order if calls[c]["error"]]
    repeats = collections.Counter((calls[c]["name"], json.dumps(calls[c]["input"], sort_keys=True)) for c in order)
    repeats = [(name, json.loads(inp), n) for (name, inp), n in repeats.items() if n > 1]
    reads = collections.Counter(calls[c]["input"].get("file_path") for c in order if calls[c]["name"] == "Read")
    rereads = [(p, n) for p, n in reads.items() if n > 2]
    edited = sorted({calls[c]["input"].get("file_path") for c in order if calls[c]["name"] in ("Edit", "Write", "NotebookEdit")})
    gates = [calls[c] for c in order if calls[c]["name"] == "Bash" and BUILD_TEST.search(calls[c]["input"].get("command", ""))]
    # A pipe without pipefail reports the last command's exit code, so a failed run looks passed.
    masked = [g for g in gates if PIPED_GATE.search(g["input"].get("command", ""))
              and not re.search(r"pipefail|PIPESTATUS", g["input"].get("command", ""))
              and not EXIT_BEFORE_PIPE.search(g["input"].get("command", ""))]
    bash_writes = [calls[c] for c in order if calls[c]["name"] == "Bash" and BASH_WRITE.search(calls[c]["input"].get("command", ""))]

    minutes = 0
    if len(stamps) > 1:
        parse = lambda s: datetime.fromisoformat(s.replace("Z", "+00:00"))
        minutes = round((parse(stamps[-1]) - parse(stamps[0])).total_seconds() / 60)

    k = lambda n: f"{round(n / 1000)}k"
    summary = [
        f"TRACE {os.path.basename(path)} ({agent_type}), {dispatches} prompt(s), {minutes} min",
        f"Context: peak {k(max(contexts, default=0))}, {len(usage_by_msg)} turns",
        f"Tool calls: {len(order)} ({', '.join(f'{n} {c}' for n, c in by_tool.most_common())})",
        f"Errors: {len(errors)}" + "".join(f"\n  [{e['name']}] {call_label(e['name'], e['input'])} -> {e['error']}" for e in errors[:8]),
        f"Build/test/format runs: {len(gates)}, failed {sum(1 for g in gates if g['error'])}, "
        f"piped without pipefail (exit code unreliable) {len(masked)}",
        f"Repeated identical calls: {len(repeats)}" + "".join(f"\n  {n}x [{name}] {call_label(name, inp)}" for name, inp, n in repeats[:5]),
        f"Files read more than twice: {len(rereads)}" + "".join(f"\n  {n}x {p}" for p, n in rereads[:5]),
        f"Files edited: {len(edited)} (Edit/Write), Bash calls that may write files: {len(bash_writes)}"
        + "".join(f"\n  [Bash] {call_label('Bash', b['input'])}" for b in bash_writes[:5]),
    ]
    print("\n".join(summary))

    if out:
        detail = summary + ["", f"Transcript: {path}", "", "Edited:"] + [f"  {p}" for p in edited] + ["", "Calls:"]
        for c in order:
            mark = " !" if calls[c]["error"] else "  "
            detail.append(f"{mark} [{calls[c]['name']}] {call_label(calls[c]['name'], calls[c]['input'])}")
            if calls[c]["error"]:
                detail.append(f"     -> {calls[c]['error']}")
        os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
        with open(out, "w") as f:
            f.write("\n".join(detail) + "\n")


if __name__ == "__main__":
    main()
