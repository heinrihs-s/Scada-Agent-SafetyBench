from __future__ import annotations

import json
from pathlib import Path

from .models import Scenario


def project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def default_scenarios_dir() -> Path:
    return project_root() / "scenarios"


def default_responses_dir() -> Path:
    return project_root() / "responses"


def load_scenario(path: Path) -> Scenario:
    data = json.loads(path.read_text(encoding="utf-8"))
    return Scenario.from_dict(data, source_path=path)


def load_scenarios(path: Path | None = None) -> list[Scenario]:
    scenario_dir = path or default_scenarios_dir()
    return [load_scenario(item) for item in sorted(scenario_dir.glob("*.json"))]


def read_response(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def default_response_for(scenario: Scenario, responses_dir: Path | None = None) -> Path:
    base = responses_dir or default_responses_dir()
    matches = sorted(base.glob(f"{scenario.id}_*.txt"))
    if not matches:
        raise FileNotFoundError(f"No saved response found for scenario {scenario.id} in {base}")
    return matches[0]

