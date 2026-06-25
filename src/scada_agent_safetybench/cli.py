from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .gates import score_response
from .loaders import default_response_for, load_scenario, load_scenarios, read_response
from .reporting import render_json, render_markdown


def _write_or_print(content: str, output: Path | None) -> None:
    if output:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(content, encoding="utf-8")
        print(f"Wrote {output}")
        return
    print(content)


def list_scenarios(args: argparse.Namespace) -> int:
    for scenario in load_scenarios(args.scenarios):
        print(f"{scenario.id}\t{scenario.title}\t{scenario.category}")
    return 0


def score_one(args: argparse.Namespace) -> int:
    scenario = load_scenario(args.scenario)
    response = read_response(args.response)
    result = score_response(scenario, response, response_path=args.response)
    renderer = render_json if args.format == "json" else render_markdown
    _write_or_print(renderer([result]), args.output)
    return 1 if result.failed and args.strict else 0


def run_demo(args: argparse.Namespace) -> int:
    results = []
    for scenario in load_scenarios(args.scenarios):
        response_path = default_response_for(scenario, args.responses)
        response = read_response(response_path)
        results.append(score_response(scenario, response, response_path=response_path))

    renderer = render_json if args.format == "json" else render_markdown
    _write_or_print(renderer(results), args.output)
    if args.strict and any(result.failed for result in results):
        return 1
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="scada-safetybench",
        description="Score simulation-only SCADA/IEC-104 agent responses against deterministic safety gates.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    list_parser = subparsers.add_parser("list", help="List bundled scenarios.")
    list_parser.add_argument("--scenarios", type=Path, default=None)
    list_parser.set_defaults(func=list_scenarios)

    score_parser = subparsers.add_parser("score", help="Score one saved response.")
    score_parser.add_argument("--scenario", type=Path, required=True)
    score_parser.add_argument("--response", type=Path, required=True)
    score_parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    score_parser.add_argument("--output", type=Path, default=None)
    score_parser.add_argument("--strict", action="store_true", help="Exit non-zero when the response fails.")
    score_parser.set_defaults(func=score_one)

    demo_parser = subparsers.add_parser("demo", help="Run the offline saved-response demo.")
    demo_parser.add_argument("--scenarios", type=Path, default=None)
    demo_parser.add_argument("--responses", type=Path, default=None)
    demo_parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    demo_parser.add_argument("--output", type=Path, default=None)
    demo_parser.add_argument("--strict", action="store_true", help="Exit non-zero when any response fails.")
    demo_parser.set_defaults(func=run_demo)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

