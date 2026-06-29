from pathlib import Path

from scada_agent_safetybench.loaders import load_scenarios


def test_bundled_scenarios_load():
    repo = Path(__file__).resolve().parents[1]
    scenarios = load_scenarios(repo / "scenarios")
    assert len(scenarios) == 27
    assert scenarios[0].id == "001_alarm_burst_maintenance"
    ids = [s.id for s in scenarios]
    assert len(ids) == len(set(ids))

