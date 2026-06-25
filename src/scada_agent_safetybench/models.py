from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class PatternGate:
    id: str
    description: str
    patterns: tuple[str, ...]
    severity: str = "high"

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "PatternGate":
        return cls(
            id=data["id"],
            description=data["description"],
            patterns=tuple(data.get("patterns", [])),
            severity=data.get("severity", "high"),
        )


@dataclass(frozen=True)
class RequiredElement:
    id: str
    description: str
    any_of: tuple[str, ...]
    severity: str = "medium"

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "RequiredElement":
        return cls(
            id=data["id"],
            description=data["description"],
            any_of=tuple(data.get("any_of", [])),
            severity=data.get("severity", "medium"),
        )


@dataclass(frozen=True)
class Scenario:
    id: str
    title: str
    category: str
    protocol_context: str
    situation: str
    prompt: str
    expected_safe_behavior: str
    forbidden_recommendations: tuple[PatternGate, ...] = field(default_factory=tuple)
    required_elements: tuple[RequiredElement, ...] = field(default_factory=tuple)
    advisory_patterns: tuple[PatternGate, ...] = field(default_factory=tuple)
    source_path: Path | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any], source_path: Path | None = None) -> "Scenario":
        return cls(
            id=data["id"],
            title=data["title"],
            category=data["category"],
            protocol_context=data["protocol_context"],
            situation=data["situation"],
            prompt=data["prompt"],
            expected_safe_behavior=data["expected_safe_behavior"],
            forbidden_recommendations=tuple(
                PatternGate.from_dict(item)
                for item in data.get("forbidden_recommendations", [])
            ),
            required_elements=tuple(
                RequiredElement.from_dict(item)
                for item in data.get("required_elements", [])
            ),
            advisory_patterns=tuple(
                PatternGate.from_dict(item)
                for item in data.get("advisory_patterns", [])
            ),
            source_path=source_path,
        )


@dataclass(frozen=True)
class Finding:
    gate_id: str
    severity: str
    description: str
    matched: tuple[str, ...] = field(default_factory=tuple)
    kind: str = "violation"


@dataclass(frozen=True)
class ScoreResult:
    scenario_id: str
    scenario_title: str
    verdict: str
    findings: tuple[Finding, ...]
    response_path: Path | None = None

    @property
    def failed(self) -> bool:
        return self.verdict == "fail"

