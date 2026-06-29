"""Generate docs/demo.cast (asciicast v2) from real CLI output.

Deterministic: it runs the offline CLI, captures actual output, and synthesizes
typing + timing into an asciicast v2 stream. No network, no live model. Re-run after
changing scenarios to refresh the recording:

    python tools/make_cast.py
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
OUT = REPO / "docs" / "demo.cast"

WIDTH = 100
HEIGHT = 34
FIXED_TIMESTAMP = 1751200000  # fixed for reproducible output
PROMPT = "\x1b[32m$\x1b[0m "  # green "$ "
CHAR_DELAY = 0.035            # per-keystroke
ENTER_DELAY = 0.25           # think time before output
AFTER_OUTPUT = 1.2           # pause after output before next command


def run_cli(*cli_args: str) -> str:
    proc = subprocess.run(
        [sys.executable, "-m", "scada_agent_safetybench", *cli_args],
        cwd=REPO, capture_output=True, text=True, check=True,
    )
    return proc.stdout


def crlf(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\n", "\r\n")


def main() -> int:
    # The 27-scenario verdict table is the visual finish; trim at the findings detail.
    demo_md = run_cli("demo", "--format", "markdown")
    table = demo_md.split("## Findings", 1)[0].rstrip() + "\n"

    steps = [
        ("# SCADA Agent SafetyBench — simulation-only, offline, no API keys",
         None),
        ("scada-safetybench list",
         run_cli("list")),
        ("scada-safetybench score --scenario scenarios/002_malicious_operator_note.json \\\r\n"
         "      --response responses/002_malicious_operator_note_unsafe.txt",
         run_cli("score",
                 "--scenario", "scenarios/002_malicious_operator_note.json",
                 "--response", "responses/002_malicious_operator_note_unsafe.txt")),
        ("scada-safetybench score --scenario scenarios/013_safe_shutdown_vs_availability.json \\\r\n"
         "      --response responses/013_safe_shutdown_vs_availability_safe.txt",
         run_cli("score",
                 "--scenario", "scenarios/013_safe_shutdown_vs_availability.json",
                 "--response", "responses/013_safe_shutdown_vs_availability_safe.txt")),
        ("scada-safetybench score --scenario scenarios/027_vague_hedging_warn.json \\\r\n"
         "      --response responses/027_vague_hedging_warn_warn.txt",
         run_cli("score",
                 "--scenario", "scenarios/027_vague_hedging_warn.json",
                 "--response", "responses/027_vague_hedging_warn_warn.txt")),
        ("scada-safetybench demo   # 27 scenarios across six failure-mode families",
         table),
    ]

    events: list[list] = []
    t = 0.0

    def emit(data: str) -> None:
        nonlocal t
        events.append([round(t, 3), "o", data])

    for command, output in steps:
        emit(PROMPT)
        t += 0.4
        for ch in command:
            emit(ch)
            t += CHAR_DELAY
        emit("\r\n")
        t += ENTER_DELAY
        if output:
            emit(crlf(output if output.endswith("\n") else output + "\n"))
        t += AFTER_OUTPUT

    emit(PROMPT)

    header = {
        "version": 2,
        "width": WIDTH,
        "height": HEIGHT,
        "timestamp": FIXED_TIMESTAMP,
        "title": "SCADA Agent SafetyBench - offline demo",
        "env": {"TERM": "xterm-256color", "SHELL": "/bin/bash"},
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps(header) + "\n")
        for event in events:
            fh.write(json.dumps(event) + "\n")

    print(f"Wrote {OUT} ({len(events)} events, ~{t:.1f}s runtime)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
