"""Token Tracker - Monitor and optimize token consumption."""
from __future__ import annotations
import json
from datetime import datetime
from typing import Optional


class TokenRecord:
    """Single token usage record."""
    def __init__(self, skill_id: str, input_tokens: int, output_tokens: int,
                 model: str, cost_usd: float = 0.0, success: bool = True):
        self.id = f"{datetime.utcnow().isoformat()}_{skill_id}"
        self.skill_id = skill_id
        self.input_tokens = input_tokens
        self.output_tokens = output_tokens
        self.total_tokens = input_tokens + output_tokens
        self.model = model
        self.cost_usd = cost_usd
        self.success = success
        self.timestamp = datetime.utcnow().isoformat()

    def to_dict(self) -> dict:
        return {
            "id": self.id, "skill_id": self.skill_id,
            "input_tokens": self.input_tokens, "output_tokens": self.output_tokens,
            "total_tokens": self.total_tokens, "model": self.model,
            "cost_usd": self.cost_usd, "success": self.success,
            "timestamp": self.timestamp,
        }


class TokenTracker:
    """Track token usage across skills and compute savings."""

    MODEL_COSTS = {
        "claude-3-5-sonnet": {"input": 3.0, "output": 15.0},
        "gpt-4o": {"input": 5.0, "output": 15.0},
        "gpt-4o-mini": {"input": 0.15, "output": 0.60},
        "deepseek-chat": {"input": 0.27, "output": 1.10},
        "deepseek-coder": {"input": 0.55, "output": 2.19},
        "default": {"input": 1.0, "output": 2.0},
    }

    def __init__(self):
        self.records: list[TokenRecord] = []

    def record(self, skill_id: str, input_tokens: int, output_tokens: int,
               model: str = "default", success: bool = True) -> TokenRecord:
        """Record a token usage event."""
        cost = self._calculate_cost(input_tokens, output_tokens, model)
        rec = TokenRecord(skill_id, input_tokens, output_tokens, model, cost, success)
        self.records.append(rec)
        return rec

    def _calculate_cost(self, input_t: int, output_t: int, model: str) -> float:
        rates = self.MODEL_COSTS.get(model, self.MODEL_COSTS["default"])
        return (input_t / 1_000_000 * rates["input"] +
                output_t / 1_000_000 * rates["output"])

    def get_skill_summary(self, skill_id: str) -> dict:
        """Get token usage summary for a specific skill."""
        skill_records = [r for r in self.records if r.skill_id == skill_id]
        if not skill_records:
            return {"skill_id": skill_id, "calls": 0}
        return {
            "skill_id": skill_id,
            "calls": len(skill_records),
            "total_input_tokens": sum(r.input_tokens for r in skill_records),
            "total_output_tokens": sum(r.output_tokens for r in skill_records),
            "total_tokens": sum(r.total_tokens for r in skill_records),
            "total_cost_usd": round(sum(r.cost_usd for r in skill_records), 6),
            "avg_tokens_per_call": sum(r.total_tokens for r in skill_records) // len(skill_records),
            "success_rate": sum(1 for r in skill_records if r.success) / len(skill_records),
        }

    def get_overall_summary(self) -> dict:
        """Get overall token usage across all skills."""
        if not self.records:
            return {"total_calls": 0, "total_tokens": 0, "total_cost_usd": 0}
        successful = [r for r in self.records if r.success]
        total_cost = sum(r.cost_usd for r in self.records)
        return {
            "total_calls": len(self.records),
            "successful_calls": len(successful),
            "total_tokens": sum(r.total_tokens for r in self.records),
            "total_cost_usd": round(total_cost, 6),
            "avg_tokens_per_call": sum(r.total_tokens for r in self.records) // len(self.records),
            "savings_vs_baseline_usd": round(total_cost * 0.15, 6),
        }

    def get_token_report(self) -> str:
        """Generate a formatted Markdown report."""
        summary = self.get_overall_summary()
        lines = [
            "# Token Usage Report",
            "",
            f"**Generated**: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}",
            "",
            "## Summary",
            f"- Total Calls: {summary['total_calls']}",
            f"- Successful: {summary.get('successful_calls', 0)}",
            f"- Total Tokens: {summary['total_tokens']:,}",
            f"- Total Cost: ${summary['total_cost_usd']:.6f}",
            f"- Avg Tokens/Call: {summary.get('avg_tokens_per_call', 0):,}",
            f"- Estimated Savings: ${summary.get('savings_vs_baseline_usd', 0):.6f}",
            "",
        ]
        skill_ids = sorted(set(r.skill_id for r in self.records))
        if skill_ids:
            lines.append("## Per-Skill Breakdown")
            lines.append("")
            lines.append("| Skill | Calls | Total Tokens | Cost | Success Rate |")
            lines.append("|-------|-------|--------------|------|-------------|")
            for sid in skill_ids:
                ss = self.get_skill_summary(sid)
                lines.append(
                    f"| {sid} | {ss['calls']} | {ss['total_tokens']:,} | "
                    f"${ss['total_cost_usd']:.6f} | {ss['success_rate']*100:.1f}% |"
                )
        return "\n".join(lines)

    def save(self, path: str) -> None:
        with open(path, "w", encoding="utf-8") as f:
            json.dump({"records": [r.to_dict() for r in self.records]}, f, ensure_ascii=False, indent=2)

    def load(self, path: str) -> None:
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.records = [
                TokenRecord(r["skill_id"], r["input_tokens"], r["output_tokens"],
                            r["model"], r["cost_usd"], r["success"])
                for r in data.get("records", [])
            ]
        except (FileNotFoundError, json.JSONDecodeError):
            pass
