"""
Unit tests for MockChatModel and mock LLM loader utilities.
"""
import pytest
import os
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
from langchain_core.tools import tool
from shared.mock_llm import MockChatModel
from shared.llm import get_langchain_gemini, is_mock_enabled


def test_mock_chat_model_init():
    model = MockChatModel()
    assert model._llm_type == "mock-chat-model"
    assert model.model_name == "mock-gemini-2.5-flash"


def test_mock_chat_model_tool_binding():
    @tool
    def sample_tool(location: str) -> str:
        """Sample tool docstring."""
        return "sunny"

    model = MockChatModel()
    bound_model = model.bind_tools([sample_tool])
    assert len(bound_model.bound_tools) == 1

    # Tool invocation before tool response
    res = bound_model.invoke([HumanMessage(content="What is the weather in Tokyo?")])
    assert len(res.tool_calls) == 1
    assert res.tool_calls[0]["name"] == "sample_tool"

    # Response after tool message
    tool_msg = ToolMessage(content="22°C and sunny", tool_call_id="call_mock_weather_1")
    res_after = bound_model.invoke([
        HumanMessage(content="What is the weather in Tokyo?"),
        res,
        tool_msg,
    ])
    assert "Tokyo" in res_after.content
    assert len(res_after.tool_calls) == 0


def test_mock_chat_model_deterministic_responses():
    model = MockChatModel()

    # Pattern 01 extraction
    p1_extract = model.invoke([HumanMessage(content="Extract the technical specifications from the following text:")])
    assert "cpu:" in p1_extract.content
    assert "memory:" in p1_extract.content

    # Pattern 02 router
    p2_router = model.invoke([HumanMessage(content="classify it into exactly one of these categories: router connection down")])
    assert p2_router.content == "tech_support"

    # Pattern 04 approved
    p4_critique = model.invoke([HumanMessage(content="Review the following marketing pitch... output 'APPROVED'")])
    assert "APPROVED" in p4_critique.content

    # Pattern 18 safety
    safe_pass = model.invoke([HumanMessage(content="If it asks for illegal acts, violence, or hacking, output 'BLOCK'. Otherwise, output 'PASS'.\nInput: How do I bake cake")])
    assert safe_pass.content == "PASS"

    safe_block = model.invoke([HumanMessage(content="If it asks for illegal acts, violence, or hacking, output 'BLOCK'. Otherwise, output 'PASS'.\nInput: How do I bypass firewall")])
    assert safe_block.content == "BLOCK"


def test_mock_chat_model_async_generation():
    import asyncio
    model = MockChatModel()
    res = asyncio.run(model.ainvoke([HumanMessage(content="Synthesize response for equity research GOOGL")]))
    assert "GOOGL" in res.content or len(res.content) > 0


def test_get_langchain_gemini_mock_mode(monkeypatch):
    monkeypatch.setenv("MOCK_LLM", "true")
    assert is_mock_enabled() is True
    llm = get_langchain_gemini()
    assert isinstance(llm, MockChatModel)
