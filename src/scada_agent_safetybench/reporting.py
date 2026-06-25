from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

from .models import ScoreResult


def _display_path(path: Path) -> str:
    try:
        display = path.resolve().relative_to(Path.cwd().resolve())
    except ValueError:
        display = path
    return display.as_posix()


def result_to_dict(result: ScoreResult) -> dict:
    data = asdict(result)
    if result.response_path is not None:
        data["response_path"] = _display_path(result.response_path)
    return data


def render_json(results: list[ScoreResult]) -> str:
    return json.dumps([result_to_dict(result) for result in results], indent=2)


def render_markdown(results: list[ScoreResult]) -> str:
    lines = [
        "# SCADA Agent SafetyBench Report",
        "",
        "| Scenario | Verdict | Findings |",
        "|---|---:|---:|",
    ]
    for result in results:
        lines.append(
            f"| `{result.scenario_id}` {result.scenario_title} | **{result.verdict.upper()}** | {len(result.findings)} |"
        )

    lines.extend(["", "## Findings", ""])
    for result in results:
        lines.append(f"### `{result.scenario_id}` {result.scenario_title}")
        lines.append("")
        lines.append(f"Verdict: **{result.verdict.upper()}**")
        if result.response_path:
            lines.append(f"Response: `{_display_path(result.response_path)}`")
        lines.append("")
        if not result.findings:
            lines.append("No policy-gate findings.")
            lines.append("")
            continue
        for finding in result.findings:
            matched = ", ".join(f"`{item}`" for item in finding.matched) or "n/a"
            lines.append(
                f"- `{finding.severity}` `{finding.kind}` `{finding.gate_id}`: {finding.description} "
                f"(matched: {matched})"
            )
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"
