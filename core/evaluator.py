"""Skill Evaluator - Scoring and performance metrics."""
from __future__ import annotations
from typing import Optional
from .skill_tree import SkillTree, SkillNode


class SkillEvaluator:
    """Evaluates skills on multiple dimensions."""

    def __init__(self, tree: SkillTree):
        self.tree = tree

    def score_skill(self, skill_id: str) -> dict:
        """Compute a multi-dimensional score for a skill."""
        skill = self.tree.get_skill(skill_id)
        if not skill:
            return {}
        return {
            "skill_id": skill_id,
            "name": skill.name,
            "mastery_score": self._mastery_score(skill),
            "efficiency_score": self._efficiency_score(skill),
            "versatility_score": self._versatility_score(skill),
            "overall_score": 0,
        }

    def _mastery_score(self, skill: SkillNode) -> float:
        """How well is this skill mastered?"""
        level_factor = min(1.0, skill.level / 10)
        progress_factor = skill.xp_progress
        return round((level_factor * 0.6 + progress_factor * 0.4) * 100, 2)

    def _efficiency_score(self, skill: SkillNode) -> float:
        """How efficiently is this skill executed?"""
        if skill.avg_duration_ms == 0:
            return 0.0
        return round(max(0, 100 - (skill.avg_duration_ms / 100)), 2)

    def _versatility_score(self, skill: SkillNode) -> float:
        """How versatile is this skill?"""
        child_factor = min(1.0, len(skill.children_ids) / 5)
        tag_factor = min(1.0, len(skill.tags) / 3)
        return round((child_factor * 0.5 + tag_factor * 0.5) * 100, 2)

    def rank_skills(self) -> list[dict]:
        """Rank all skills by overall score."""
        scored = []
        for skill in self.tree.nodes.values():
            s = self.score_skill(skill.skill_id)
            s["overall_score"] = round(
                (s["mastery_score"] * 0.5 + s["efficiency_score"] * 0.3 + s["versatility_score"] * 0.2), 2
            )
            scored.append(s)
        scored.sort(key=lambda x: x["overall_score"], reverse=True)
        return scored

    def get_weak_skills(self, threshold: float = 30.0) -> list[dict]:
        """Find skills with low overall scores."""
        weak = []
        for skill in self.tree.nodes.values():
            s = self.score_skill(skill.skill_id)
            s["overall_score"] = round(
                (s["mastery_score"] * 0.5 + s["efficiency_score"] * 0.3 + s["versatility_score"] * 0.2), 2
            )
            if s["overall_score"] < threshold:
                weak.append(s)
        return sorted(weak, key=lambda x: x["overall_score"])
