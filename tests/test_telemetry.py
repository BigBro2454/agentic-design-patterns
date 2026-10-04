"""Unit tests for PatternTelemetryTracker and token economics modeling."""

import tempfile
import unittest
from pathlib import Path

from shared.telemetry import (
    COMPLETION_COST_PER_MILLION,
    PROMPT_COST_PER_MILLION,
    PatternTelemetryTracker,
)


class TestPatternTelemetryTracker(unittest.TestCase):

    def setUp(self):
        self.tracker = PatternTelemetryTracker(mode="mock")
        self.tracker.start_session()

    def test_record_and_aggregate_metrics(self):
        metric = self.tracker.record_run(
            pattern_id="01",
            pattern_name="01_prompt_chaining",
            category="Core Workflow",
            duration_sec=0.45,
            success=True,
            output_text="Sample output text from prompt chaining pattern.",
            custom_prompt_tokens=200,
            custom_completion_tokens=100,
        )

        self.assertEqual(metric.pattern_id, "01")
        self.assertEqual(metric.status, "PASS")
        self.assertEqual(metric.duration_ms, 450.0)
        self.assertEqual(metric.total_tokens, 300)

        # Expected cost calculation:
        # (200 / 1e6 * 0.075) + (100 / 1e6 * 0.30) = 0.000015 + 0.000030 = 0.000045
        expected_cost = round(
            (200 / 1_000_000) * PROMPT_COST_PER_MILLION
            + (100 / 1_000_000) * COMPLETION_COST_PER_MILLION,
            6,
        )
        self.assertAlmostEqual(metric.cost_usd, expected_cost, places=6)

    def test_compute_summary_sla_calculations(self):
        self.tracker.record_run("01", "p1", "Cat A", 0.30, True)
        self.tracker.record_run("02", "p2", "Cat A", 0.50, True)
        self.tracker.record_run("03", "p3", "Cat B", 0.70, True)

        summary = self.tracker.compute_summary()
        self.assertEqual(summary.total_patterns, 3)
        self.assertEqual(summary.passed_count, 3)
        self.assertEqual(summary.failed_count, 0)
        self.assertEqual(summary.pass_rate_pct, 100.0)
        self.assertEqual(summary.min_latency_ms, 300.0)
        self.assertEqual(summary.max_latency_ms, 700.0)
        self.assertAlmostEqual(summary.avg_latency_ms, 500.0, places=1)
        self.assertTrue(summary.projected_cost_per_1k_runs > 0)

    def test_json_and_markdown_export(self):
        self.tracker.record_run("01", "p1", "Cat A", 0.25, True, output_text="output 1")
        self.tracker.record_run("02", "p2", "Cat B", 0.35, True, output_text="output 2")

        with tempfile.TemporaryDirectory() as tmpdir:
            json_path = Path(tmpdir) / "telemetry.json"
            md_path = Path(tmpdir) / "telemetry.md"

            self.tracker.export_json(str(json_path))
            self.tracker.export_markdown(str(md_path))

            self.assertTrue(json_path.exists())
            self.assertTrue(md_path.exists())

            # Verify JSON readable
            import json
            with open(json_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.assertEqual(data["total_patterns"], 2)
            self.assertEqual(data["pass_rate_pct"], 100.0)

            # Verify Markdown content
            content = md_path.read_text(encoding="utf-8")
            self.assertIn("Executive Systems Dashboard", content)
            self.assertIn("Pass Rate", content)
            self.assertIn("100.0%", content)
