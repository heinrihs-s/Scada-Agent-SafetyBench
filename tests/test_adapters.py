"""Tests for response adapters. These never touch the network."""

import pytest

from scada_agent_safetybench.adapters import (
    OllamaAdapter,
    OpenAIAdapter,
    SavedResponseAdapter,
    build_adapter,
    build_prompt,
)
from scada_agent_safetybench.loaders import load_scenarios


def _scenario():
    return load_scenarios()[1]  # 002_malicious_operator_note


def test_build_prompt_includes_scenario_fields():
    scenario = _scenario()
    prompt = build_prompt(scenario)
    assert scenario.situation in prompt
    assert scenario.prompt in prompt
    assert scenario.protocol_context in prompt


def test_saved_adapter_returns_reference_response():
    scenario = _scenario()
    text = SavedResponseAdapter().generate(scenario)
    assert isinstance(text, str) and text.strip()


def test_build_adapter_saved_is_offline():
    assert isinstance(build_adapter("saved"), SavedResponseAdapter)


def test_ollama_payload_shape():
    adapter = build_adapter("ollama", model="test-model", base_url="http://host:11434/")
    assert isinstance(adapter, OllamaAdapter)
    assert adapter.base_url == "http://host:11434"  # trailing slash stripped
    payload = adapter.build_payload(_scenario())
    assert payload["model"] == "test-model"
    assert payload["stream"] is False
    assert [m["role"] for m in payload["messages"]] == ["system", "user"]


def test_openai_adapter_requires_key(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    with pytest.raises(RuntimeError):
        build_adapter("openai", model="gpt-x")


def test_openai_payload_shape(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test")
    adapter = build_adapter("openai", model="gpt-x")
    assert isinstance(adapter, OpenAIAdapter)
    payload = adapter.build_payload(_scenario())
    assert payload["model"] == "gpt-x"
    assert [m["role"] for m in payload["messages"]] == ["system", "user"]


def test_ollama_requires_model():
    with pytest.raises(RuntimeError):
        build_adapter("ollama")


def test_unknown_provider_raises():
    with pytest.raises(RuntimeError):
        build_adapter("nope")
