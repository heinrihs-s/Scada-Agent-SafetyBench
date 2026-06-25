from pathlib import Path

from scada_agent_safetybench.loaders import load_scenarios


def test_bundled_scenarios_load():
    repo = Path(__file__).resolve().parents[1]
    scenarios = load_scenarios(repo / "scenarios")
    assert len(scenarios) == 10
    assert scenarios[0].id == "001_alarm_burst_maintenance"

