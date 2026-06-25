# Black Hat Arsenal Submission Notes

Verified live on 2026-06-25: Black Hat Europe 2026 Arsenal Call for Tools closes on 2026-07-19, with notification to submitters listed as 2026-08-24.

## Tool Name

SCADA Agent SafetyBench

## Short Description

Simulation-only benchmark for testing whether AI assistant responses stay inside safe SCADA/IEC-104 operational boundaries.

## Longer Description Draft

SCADA Agent SafetyBench evaluates AI-agent and LLM assistant responses in synthetic industrial-control scenarios inspired by IEC 60870-5-104 control-room workflows. It ships with deterministic policy gates for unsafe recommendations, human-authorization checks, saved example responses, and offline report generation. The tool is designed for defenders, researchers, and OT security teams who need a reproducible way to test whether AI assistants recommend unsafe operational actions, follow untrusted context, or over-trust stale telemetry.

The benchmark is simulation-only. It does not connect to live SCADA systems, issue commands, or include exploit instructions.

## Category Fit

- AI security
- ICS/OT security
- defensive testing
- safety benchmark

## Demo Requirements

- No API key required.
- No internet required.
- Runs with Python 3.10+.
- Demonstrates scenario loading, saved-response scoring, and Markdown/JSON report output.

## Evidence To Prepare Before Submission

- Public GitHub URL: `https://github.com/heinrihs-s/scada-agent-safetybench`
- Three-minute screen recording
- Maintainer bio
- Screenshot of `reports/demo-report.md`
- Short list of future work: JSON schema, Ollama adapter, OpenAI adapter, static report viewer

## Human Rewrite Reminder

Black Hat Briefings notes prohibit LLM-generated submission text. Arsenal rules should also be handled conservatively: use these notes as internal scaffolding, then rewrite the final portal text manually in Heinrihs's own wording.

