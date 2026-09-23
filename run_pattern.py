#!/usr/bin/env python3
"""
CLI Runner for 21 Production Agentic Design Patterns.
Execute individual patterns, list taxonomy, or run batch validations.
"""
import sys
import os
import argparse
import subprocess

PATTERNS = {
    "01": ("01_prompt_chaining", "Core Workflow", "Sequential decomposition of complex reasoning into discrete LLM chains"),
    "02": ("02_routing", "Core Workflow", "Dynamic intent-based classification and conditional dispatch to specialized handlers"),
    "03": ("03_parallelization", "Core Workflow", "Concurrent multi-branch LLM execution for high-throughput synthesis"),
    "04": ("04_reflection", "Self-Improvement", "Iterative critic-generator loop with automated quality threshold gating"),
    "05": ("05_tool_use", "Tooling & Environment", "Dynamic tool calling via LangGraph ReAct agent and schema-bound tools"),
    "06": ("06_planning", "Reasoning & Planning", "Multi-stage hierarchical task decomposition and sequential step execution"),
    "07": ("07_multi_agent", "Multi-Agent Orchestration", "Hierarchical specialist agent collaboration (Researcher -> Writer -> Editor)"),
    "08": ("08_memory_management", "State & Memory", "Multi-tiered memory: short-term conversation buffer + persistent entity store"),
    "09": ("09_learning_and_adaptation", "Self-Improvement", "Dynamic runtime behavioral steering from accumulated user feedback"),
    "10": ("10_mcp_model_context_protocol", "Tooling & Environment", "Model Context Protocol (MCP) server integration & tool discovery runtime"),
    "11": ("11_goal_setting_and_monitoring", "Reasoning & Planning", "Autonomous goal tracking, progress calculation, and state transition monitoring"),
    "12": ("12_exception_handling_and_recovery", "Robustness & Safety", "Circuit breaking, retry backoff, and LLM-driven fallback self-healing"),
    "13": ("13_human_in_the_loop", "Robustness & Safety", "Deterministic escalation and approval gating for high-blast-radius actions"),
    "14": ("14_knowledge_retrieval_rag", "Context & Data", "Context augmentation via vector database retrieval and grounded generation"),
    "15": ("15_inter_agent_communication", "Multi-Agent Orchestration", "Structured inter-agent protocol exchange and peer-to-peer data passing"),
    "16": ("16_resource_aware_optimization", "Cost & Performance", "Dynamic query complexity routing between Flash and Pro model tiers"),
    "17": ("17_reasoning_techniques", "Reasoning & Planning", "Chain-of-Thought (CoT) and structured step-by-step reasoning puzzles"),
    "18": ("18_guardrails_and_safety", "Robustness & Safety", "Input/output policy enforcement and safety moderation filters"),
    "19": ("19_evaluation_and_monitoring", "Observability", "Automated LLM-as-a-Judge scoring for quality, tone, and helpfulness"),
    "20": ("20_prioritization", "Core Workflow", "Algorithmic triage and dynamic priority ranking of concurrent task queues"),
    "21": ("21_exploration_and_discovery", "Reasoning & Planning", "Autonomous hypothesis generation and open-ended environment exploration")
}

def list_patterns():
    print("\n" + "=" * 95)
    print(f"{'#':<4} {'PATTERN DIRECTORY':<35} {'TAXONOMY CATEGORY':<25} {'DESCRIPTION'}")
    print("=" * 95)
    for num, (dirname, cat, desc) in sorted(PATTERNS.items()):
        print(f"{num:<4} {dirname:<35} {cat:<25} {desc}")
    print("=" * 95 + "\n")

def run_pattern(key: str, mock: bool = False):
    # Match by number or substring
    target = None
    key_clean = key.strip().lower().zfill(2) if key.strip().isdigit() else key.strip().lower()
    
    for num, (dirname, cat, desc) in PATTERNS.items():
        if key_clean == num or key_clean in dirname.lower():
            target = dirname
            break
            
    if not target:
        print(f"❌ Error: Pattern '{key}' not found. Run with --list to view all 21 patterns.")
        sys.exit(1)
        
    script_path = os.path.join("patterns", target, "run.py")
    if not os.path.exists(script_path):
        print(f"❌ Error: Script '{script_path}' does not exist.")
        sys.exit(1)
        
    mode_label = "[MOCK MODE]" if mock else "[LIVE GEMINI]"
    print(f"\n🚀 Executing Pattern [{target}] {mode_label}...\n")
    
    env = os.environ.copy()
    if mock:
        env["MOCK_LLM"] = "true"
        
    cmd = [sys.executable, script_path]
    result = subprocess.run(cmd, env=env)
    sys.exit(result.returncode)

def run_matrix(mock: bool = True):
    """Executes the full 21-pattern test matrix and outputs an executive summary table."""
    import time
    
    env = os.environ.copy()
    if mock:
        env["MOCK_LLM"] = "true"
        
    mode_str = "Headless Mock (Deterministic)" if mock else "Live API Integration"
    print("\n" + "=" * 95)
    print(f"🔬 RUNNING 21-PATTERN VALIDATION MATRIX ({mode_str})")
    print("=" * 95)
    print(f"{'#':<4} {'PATTERN DIRECTORY':<35} {'CATEGORY':<24} {'DURATION':<10} {'STATUS'}")
    print("-" * 95)
    
    results = []
    total_start = time.time()
    
    for num, (dirname, cat, desc) in sorted(PATTERNS.items()):
        script_path = os.path.join("patterns", dirname, "run.py")
        if not os.path.exists(script_path):
            print(f"{num:<4} {dirname:<35} {cat:<24} {'-':<10} ❌ MISSING")
            results.append((num, dirname, "MISSING", 0.0))
            continue
            
        t0 = time.time()
        proc = subprocess.run([sys.executable, script_path], env=env, capture_output=True, text=True)
        elapsed = round(time.time() - t0, 2)
        
        if proc.returncode == 0:
            status = "✅ PASS"
            results.append((num, dirname, "PASS", elapsed))
        else:
            status = "❌ FAIL"
            results.append((num, dirname, "FAIL", elapsed))
            
        print(f"{num:<4} {dirname:<35} {cat:<24} {f'{elapsed}s':<10} {status}")
        
    total_elapsed = round(time.time() - total_start, 2)
    passed_count = sum(1 for _, _, s, _ in results if s == "PASS")
    total_count = len(results)
    
    print("=" * 95)
    print(f"📊 SUMMARY: {passed_count}/{total_count} PASSED ({round((passed_count/total_count)*100, 1)}%) in {total_elapsed}s")
    print("=" * 95 + "\n")
    
    if passed_count != total_count:
        sys.exit(1)
    sys.exit(0)

def main():
    parser = argparse.ArgumentParser(
        description="CLI Runner & Validation Matrix for 21 Production Agentic Design Patterns",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  python run_pattern.py --list\n"
            "  python run_pattern.py 01 --mock\n"
            "  python run_pattern.py routing\n"
            "  python run_pattern.py --all --mock\n"
        )
    )
    parser.add_argument("pattern", nargs="?", help="Pattern number (e.g. 01, 10) or keyword (e.g. mcp, routing)")
    parser.add_argument("--list", "-l", action="store_true", help="List all 21 patterns and categories")
    parser.add_argument("--all", "--matrix", "-a", action="store_true", help="Run the full 21-pattern test matrix")
    parser.add_argument("--mock", "-m", action="store_true", help="Run with headless deterministic mock LLM (offline / CI)")
    
    args = parser.parse_args()
    
    if args.all:
        run_matrix(mock=args.mock or os.environ.get("MOCK_LLM", "").lower() in ("true", "1", "yes"))
    elif args.list or not args.pattern:
        list_patterns()
        if not args.pattern:
            print("Tip: Run a specific pattern: python run_pattern.py <pattern> [--mock]")
            print("     Run the full test matrix: python run_pattern.py --all [--mock]\n")
    else:
        run_pattern(args.pattern, mock=args.mock or os.environ.get("MOCK_LLM", "").lower() in ("true", "1", "yes"))

if __name__ == "__main__":
    main()
