# Agent Instructions

This repository is a simulation-only SCADA/IEC-104 AI-safety benchmark. Keep every change inside that boundary.

## Safety Rules

- Do not add code that connects to live SCADA, PLC, RTU, substation, or industrial networks.
- Do not add exploit instructions, live target discovery, or command-sending functionality.
- Keep scenarios synthetic and clearly marked as synthetic.
- Prefer deterministic checks over vague model-only scoring.
- Preserve the framing: this evaluates AI assistant recommendations before anything reaches a real control environment.

## Good Agent Tasks

- Add new synthetic scenarios with expected safe behavior and forbidden recommendations.
- Improve deterministic policy gates and add focused tests.
- Add local/offline report formats.
- Improve schema validation for scenarios and responses.
- Add adapter scaffolding for local model evaluation, keeping API keys and private outputs out of the repo.

## Verification

Run the focused tests before committing:

```bash
python -m pytest
```

If dependencies are not installed, at least run:

```bash
python -m compileall src
```
