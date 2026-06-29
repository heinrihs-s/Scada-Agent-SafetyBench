# Black Hat Arsenal Demo Script

Target runtime: 3 minutes. The benchmark ships with 27 simulation-only scenarios
across six failure-mode families (see `docs/TAXONOMY.md`).

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

Windows:

```powershell
python -m venv .venv
.\\.venv\\Scripts\\Activate.ps1
pip install -e .
```

## Demo Flow

1. Show that the benchmark is offline and simulation-only.

```bash
scada-safetybench list
```

2. Run all saved responses.

```bash
scada-safetybench demo --format markdown --output reports/demo-report.md
```

3. Open `reports/demo-report.md` and point out:

- a safe alarm-triage response passing because it verifies maintenance and avoids switching
- an unsafe malicious-note response failing because it endorses bypassing approval
- an unsafe false-consensus response failing because two agent roles share the same stale evidence

4. Score one scenario live.

```bash
scada-safetybench score \
  --scenario scenarios/002_malicious_operator_note.json \
  --response responses/002_malicious_operator_note_unsafe.txt
```

5. Show the three-tier verdict model: a `fail` (forbidden recommendation), a `pass`,
   and a `warn` (advisory only, e.g. `027_vague_hedging_warn`).

6. Optional live finale — score a real model with the same gates (offline-safe
   fallback is the `saved` provider):

```bash
scada-safetybench run --provider ollama --model llama3.1
```

7. Closing line:

> The benchmark does not automate control. It evaluates whether assistant recommendations remain inside deterministic SCADA safety boundaries before anyone considers real-world deployment.

## What Not To Say

- Do not say the tool lets LLMs control SCADA.
- Do not claim autonomous vulnerability discovery.
- Do not include vendor-specific vulnerability details.
- Do not imply this replaces qualified operators or engineering review.

