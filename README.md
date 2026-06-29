# SCADA Agent SafetyBench

SCADA Agent SafetyBench is a simulation-only benchmark for evaluating whether LLM and AI-agent responses stay inside safe operational boundaries in SCADA and IEC 60870-5-104 control-room workflows.

The first release focuses on IEC 60870-5-104 inspired SCADA control-room workflows. It ships with deterministic policy gates, **27 offline scenarios across six failure-mode families** (see [`docs/TAXONOMY.md`](docs/TAXONOMY.md)), saved example responses, and a CLI that produces reproducible safety reports without API keys or internet access. The same gates can also score responses from a live model (local Ollama or any OpenAI-compatible endpoint).

Keywords: SCADA, ICS, OT security, IEC 60870-5-104, IEC-104, AI safety, LLM agents, control-room decision support, intrusion detection, cyber-physical safety, deterministic policy gates.

## Why This Exists

Generic chatbot jailbreak tests do not capture the failure modes that matter in OT environments. A control-room assistant can be harmful even when it is fluent, technically plausible, and well-intentioned, if it recommends direct control action, ignores stale topology, follows poisoned operator notes, or skips human authorization.

This benchmark tests those boundaries in a safe, synthetic setting:

- IEC-104 and SCADA incident-response context
- cyber-physical safety invariants
- deterministic policy gates for unsafe recommendations
- saved-response mode for reproducible demos
- human authorization and operator deferral checks
- Markdown and JSON reports for review, talks, and research notes

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

## Run Against a Live Model

The deterministic gates can score real model output, not just saved responses. No
extra dependencies are required; the adapters use only the Python standard library.

Local model via Ollama (keeps prompts on your own hardware):

```bash
scada-safetybench run \
  --provider ollama \
  --model llama3.1 \
  --base-url http://localhost:11434 \
  --save-responses runs/llama31
```

Any OpenAI-compatible endpoint (reads `OPENAI_API_KEY`):

```bash
export OPENAI_API_KEY=sk-...
scada-safetybench run --provider openai --model gpt-4o-mini --format markdown
```

`--save-responses DIR` writes each generated response to disk so a run is fully
reproducible and can be replayed offline with `demo`/`score`.

## Recorded Demo

A terminal recording of the offline demo lives at [`docs/demo.cast`](docs/demo.cast)
([asciicast v2](https://docs.asciinema.org/manual/asciicast/v2/)). Play it locally,
upload it, or render it to GIF/SVG:

```bash
asciinema play docs/demo.cast          # play in a terminal
asciinema upload docs/demo.cast        # share on asciinema.org
agg docs/demo.cast docs/demo.gif       # render to GIF (agg)
svg-term --in docs/demo.cast --out docs/demo.svg
```

## Repository Layout

- `scenarios/` - synthetic SCADA/IEC-104 safety scenarios
- `responses/` - saved example model responses for offline evaluation
- `src/scada_agent_safetybench/` - CLI, policy gates, loaders, reports
- `reports/` - example generated reports
- `docs/` - Arsenal demo script and submission support notes
- `tests/` - focused unit tests

## Related IEC-104 / SCADA Repos

- [IEC-60870-5-104-Threat-Scenario-Generator](https://github.com/heinrihs-s/IEC-60870-5-104-Threat-Scenario-Generator) - synthetic IEC-104 attack scenarios and PCAP-style generators for IDS evaluation.
- [iec104-rulebook](https://github.com/heinrihs-s/iec104-rulebook) - YAML monitoring rules and baseline templates for IEC-104 environments.
- [zeek-iec104-lab](https://github.com/heinrihs-s/zeek-iec104-lab) - helper scripts for synthetic Zeek-style IEC-104 records and lab-only queue/preservation checks.

## Agent-Friendly Workflow

This repo includes `AGENTS.md` so Codex, Claude Code, and other coding agents can contribute without crossing the safety boundary. Good agent tasks include adding synthetic scenarios, improving deterministic policy gates, expanding report formats, and writing tests. Live control-system integration is intentionally out of scope.

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

- [x] 27 scenarios across a documented six-family failure-mode taxonomy.
- [x] Local model adapter (Ollama) and OpenAI-compatible adapter for research runs.
- [x] Schema and golden-verdict tests across the full corpus.
- [ ] Published multi-model results table (leaderboard) from `run --save-responses`.
- [ ] Richer scenario metadata, versioning, and per-family scoring.
- [ ] A small static report viewer.

## Results (leaderboard)

The benchmark is designed to produce a comparable, reproducible multi-model results
table. Generate per-model runs with `run --save-responses` and aggregate them into a
table here. (No model scores are published yet; this section is a placeholder until
runs are recorded.)

## Licenses

Code is licensed under Apache-2.0. Scenario text, saved responses, and report text are licensed under CC BY 4.0; see `DATA-LICENSE.md`.

