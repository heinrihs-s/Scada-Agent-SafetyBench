# SCADA Agent SafetyBench

SCADA Agent SafetyBench is a simulation-only benchmark for evaluating whether LLM and AI-agent responses stay inside safe operational boundaries in industrial-control contexts.

The first release focuses on IEC 60870-5-104 inspired SCADA control-room workflows. It ships with deterministic policy gates, ten offline scenarios, saved example responses, and a CLI that produces reproducible safety reports without API keys or internet access.

## Why This Exists

Generic chatbot jailbreak tests do not capture the failure modes that matter in OT environments. A control-room assistant can be harmful even when it is fluent, technically plausible, and well-intentioned, if it recommends direct control action, ignores stale topology, follows poisoned operator notes, or skips human authorization.

This benchmark tests those boundaries in a safe, synthetic setting:

- IEC-104 and SCADA incident-response context
- cyber-physical safety invariants
- deterministic policy gates for unsafe recommendations
- saved-response mode for reproducible demos
- human authorization and operator deferral checks

## Safety Scope

This project does not connect to live SCADA systems, PLCs, RTUs, substations, or industrial networks. It does not issue commands and does not provide exploit instructions. All scenarios are synthetic and intended for defensive evaluation, research, training, and tool demonstration.

Avoid describing this tool as "LLMs controlling SCADA." A better description is:

> A reproducible, simulation-only benchmark for checking whether AI assistants make unsafe recommendations in SCADA/IEC-104 control-room workflows.

## Install

Requires Python 3.10 or newer.

```powershell
python -m venv .venv
.\\.venv\\Scripts\\Activate.ps1
pip install -e .[dev]
```

On Linux/macOS:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
```

## Quick Demo

Run the fully offline demo:

```bash
scada-safetybench demo
```

Or with Python module execution:

```bash
python -m scada_agent_safetybench demo
```

Score one saved response:

```bash
scada-safetybench score \
  --scenario scenarios/002_malicious_operator_note.json \
  --response responses/002_malicious_operator_note_unsafe.txt
```

Write a Markdown report:

```bash
scada-safetybench demo --format markdown --output reports/demo-report.md
```

## Repository Layout

- `scenarios/` - synthetic SCADA/IEC-104 safety scenarios
- `responses/` - saved example model responses for offline evaluation
- `src/scada_agent_safetybench/` - CLI, policy gates, loaders, reports
- `reports/` - example generated reports
- `docs/` - Arsenal demo script and submission support notes
- `tests/` - focused unit tests

## Scoring Model

Each scenario defines:

- the control-room situation
- the assistant prompt to evaluate
- expected safe behavior
- forbidden recommendations
- required safety elements
- optional advisory signals

The runner evaluates a response with deterministic checks and returns:

- `pass` - no blocking safety issue found
- `warn` - advisory issues found, but no critical violation
- `fail` - direct violation of a scenario safety gate

The gates are intentionally transparent. They are not a replacement for expert review, but they make unsafe patterns easy to reproduce, discuss, and improve.

## Example Use Cases

- Test an OT cyber assistant before a live pilot.
- Compare model responses across prompt designs.
- Build a training exercise for control-room decision support.
- Demonstrate deterministic policy gates for AI-in-OT safety.
- Produce reproducible artifacts for Black Hat Arsenal, S4, CRITIS, or academic review.

## Roadmap

- Add richer scenario metadata and versioning.
- Add optional local model adapters, starting with Ollama.
- Add optional OpenAI adapter for research runs.
- Add JSON schema validation for scenarios.
- Add a small static report viewer.

## Licenses

Code is licensed under Apache-2.0. Scenario text, saved responses, and report text are licensed under CC BY 4.0; see `DATA-LICENSE.md`.

