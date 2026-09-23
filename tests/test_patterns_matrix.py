"""
Comprehensive 21-Pattern Headless Test Matrix.
Verifies all agentic architectural patterns execute deterministically under 5s per pattern.
"""
import os
import sys
import json
import subprocess
import pytest

ALL_PATTERNS = [
    "01_prompt_chaining",
    "02_routing",
    "03_parallelization",
    "04_reflection",
    "05_tool_use",
    "06_planning",
    "07_multi_agent",
    "08_memory_management",
    "09_learning_and_adaptation",
    "10_mcp_model_context_protocol",
    "11_goal_setting_and_monitoring",
    "12_exception_handling_and_recovery",
    "13_human_in_the_loop",
    "14_knowledge_retrieval_rag",
    "15_inter_agent_communication",
    "16_resource_aware_optimization",
    "17_reasoning_techniques",
    "18_guardrails_and_safety",
    "19_evaluation_and_monitoring",
    "20_prioritization",
    "21_exploration_and_discovery",
]


@pytest.mark.parametrize("pattern_dir", ALL_PATTERNS)
def test_individual_pattern_execution(pattern_dir):
    """Executes each pattern script headlessly with MOCK_LLM enabled."""
    script_path = os.path.join("patterns", pattern_dir, "run.py")
    assert os.path.exists(script_path), f"Script {script_path} does not exist"

    env = os.environ.copy()
    env["MOCK_LLM"] = "true"

    result = subprocess.run(
        [sys.executable, script_path],
        env=env,
        capture_output=True,
        text=True,
        timeout=15,
    )

    assert result.returncode == 0, f"Pattern {pattern_dir} failed with stderr: {result.stderr}"
    assert len(result.stdout.strip()) > 0, f"Pattern {pattern_dir} produced empty stdout"


def test_pattern_01_prompt_chaining_output():
    """Validates Pattern 01 produces valid structured JSON specifications."""
    script = "patterns/01_prompt_chaining/run.py"
    env = os.environ.copy()
    env["MOCK_LLM"] = "true"
    res = subprocess.run([sys.executable, script], env=env, capture_output=True, text=True, timeout=10)
    assert res.returncode == 0
    assert "Final JSON Output" in res.stdout
    assert "cpu" in res.stdout
    assert "memory" in res.stdout
    assert "storage" in res.stdout


def test_pattern_02_routing_output():
    """Validates Pattern 02 routes queries accurately."""
    script = "patterns/02_routing/run.py"
    env = os.environ.copy()
    env["MOCK_LLM"] = "true"
    res = subprocess.run([sys.executable, script], env=env, capture_output=True, text=True, timeout=10)
    assert res.returncode == 0
    assert "Routed to: tech_support" in res.stdout
    assert "Routed to: billing" in res.stdout


def test_pattern_04_reflection_output():
    """Validates Pattern 04 self-reflection loop completes with approval."""
    script = "patterns/04_reflection/run.py"
    env = os.environ.copy()
    env["MOCK_LLM"] = "true"
    res = subprocess.run([sys.executable, script], env=env, capture_output=True, text=True, timeout=10)
    assert res.returncode == 0
    assert "Final approved pitch achieved!" in res.stdout


def test_pattern_05_tool_use_output():
    """Validates Pattern 05 ReAct agent invokes tool and returns grounded answer."""
    script = "patterns/05_tool_use/run.py"
    env = os.environ.copy()
    env["MOCK_LLM"] = "true"
    res = subprocess.run([sys.executable, script], env=env, capture_output=True, text=True, timeout=10)
    assert res.returncode == 0
    assert "weather" in res.stdout.lower()
    assert "tokyo" in res.stdout.lower()


def test_pattern_10_mcp_output():
    """Validates Pattern 10 Model Context Protocol tool discovery and execution."""
    script = "patterns/10_mcp_model_context_protocol/run.py"
    env = os.environ.copy()
    env["MOCK_LLM"] = "true"
    res = subprocess.run([sys.executable, script], env=env, capture_output=True, text=True, timeout=10)
    assert res.returncode == 0
    assert "financial-intelligence-mcp" in res.stdout
    assert "GOOGL" in res.stdout


def test_pattern_13_human_in_the_loop_guard():
    """Validates Pattern 13 enforces human approval gating constraint."""
    script = "patterns/13_human_in_the_loop/run.py"
    env = os.environ.copy()
    env["MOCK_LLM"] = "true"
    res = subprocess.run([sys.executable, script], env=env, capture_output=True, text=True, timeout=10)
    assert res.returncode == 0
    assert "Execution aborted by Human-in-the-Loop constraint." in res.stdout


def test_pattern_18_guardrails_safety():
    """Validates Pattern 18 blocks hazardous queries and permits safe ones."""
    script = "patterns/18_guardrails_and_safety/run.py"
    env = os.environ.copy()
    env["MOCK_LLM"] = "true"
    res = subprocess.run([sys.executable, script], env=env, capture_output=True, text=True, timeout=10)
    assert res.returncode == 0
    assert "Action: Input allowed" in res.stdout
    assert "Action: Input rejected due to safety policy" in res.stdout


def test_run_pattern_cli_list():
    """Validates CLI --list outputs taxonomy table containing 21 patterns."""
    res = subprocess.run([sys.executable, "run_pattern.py", "--list"], capture_output=True, text=True)
    assert res.returncode == 0
    for p in ALL_PATTERNS:
        assert p in res.stdout


def test_run_pattern_cli_matrix():
    """Validates CLI --all --mock executes full validation matrix with exit code 0."""
    res = subprocess.run([sys.executable, "run_pattern.py", "--all", "--mock"], capture_output=True, text=True, timeout=30)
    assert res.returncode == 0
    assert "SUMMARY: 21/21 PASSED (100.0%)" in res.stdout
