"""Evolution Engine - Skill Discovery and Learning System"""
from __future__ import annotations
import json
import random
from typing import Optional
from .skill_tree import SkillTree, SkillNode


class EvolutionEngine:
    """Handles skill discovery, learning, and evolution decisions."""

    def __init__(self, tree: SkillTree):
        self.tree = tree
        self.learning_history: list[dict] = []

    def discover_new_skill(self, context: dict) -> Optional[SkillNode]:
        """Discover a new skill based on context/hints."""
        suggested = self._analyze_context(context)
        if suggested:
            self.learning_history.append({
                "action": "discover",
                "skill_id": suggested.skill_id,
                "context": context,
            })
        return suggested

    def _analyze_context(self, context: dict) -> Optional[SkillNode]:
        """Analyze context to suggest new skills."""
        keywords = context.get("keywords", [])
        task_type = context.get("task_type", "")
        existing_names = [s.name.lower() for s in self.tree.nodes.values()]
        for kw in keywords:
            if kw.lower() not in existing_names:
                return self._create_skill_from_keyword(kw, task_type)
        return None

    def _create_skill_from_keyword(self, keyword: str, task_type: str) -> SkillNode:
        """Create a new skill definition from a keyword."""
        import uuid
        skill_id = f"skill_{uuid.uuid4().hex[:8]}"
        parent_id = None
        for skill in self.tree.nodes.values():
            if skill.category.lower() == task_type.lower():
                parent_id = skill.skill_id
                break
        return SkillNode(
            skill_id=skill_id,
            name=keyword.title(),
            description=f"Auto-discovered skill: {keyword}",
            category=task_type or "general",
            parent_id=parent_id,
            xp_required=100,
        )

    def suggest_next_skill(self, current_skill_id: Optional[str] = None) -> Optional[list[SkillNode]]:
        """Suggest next skills to learn based on current state."""
        suggestions = []
        if current_skill_id:
            children = self.tree.get_children(current_skill_id)
            unmastered = [c for c in children if c.xp_current < c.xp_required]
            suggestions.extend(unmastered[:3])
        if current_skill_id:
            current = self.tree.get_skill(current_skill_id)
            if current and current.parent_id:
                siblings = self.tree.get_children(current.parent_id)
                suggestions.extend([s for s in siblings if s.skill_id != current_skill_id][:2])
        if not suggestions:
            roots = [self.tree.nodes[rid] for rid in self.tree.root_ids if rid in self.tree.nodes]
            if roots:
                random.shuffle(roots)
                suggestions.append(roots[0])
        return suggestions[:5] if suggestions else None

    def evolve_skill(self, skill_id: str, new_description: str) -> bool:
        """Refine/improve a skill's definition."""
        skill = self.tree.get_skill(skill_id)
        if not skill:
            return False
        skill.description = new_description
        self.learning_history.append({
            "action": "evolve",
            "skill_id": skill_id,
            "new_description": new_description,
        })
        return True

    def get_learning_path(self, target_skill_id: str) -> list[str]:
        """Get the prerequisite path to unlock a skill."""
        path = []
        current = self.tree.get_skill(target_skill_id)
        while current and current.parent_id:
            parent = self.tree.get_skill(current.parent_id)
            if parent:
                if parent.xp_current < parent.xp_required:
                    path.append(parent.skill_id)
                current = parent
            else:
                break
        return list(reversed(path))

    def auto_balance(self) -> dict:
        """Auto-balance skill XP requirements based on usage patterns."""
        stats = self.tree.get_stats()
        adjusted = []
        for skill in self.tree.nodes.values():
            if skill.usage_count > 10:
                if skill.xp_required > 50:
                    skill.xp_required = max(50, int(skill.xp_required * 0.8))
                    adjusted.append(skill.skill_id)
        return {"stats": stats, "adjusted_skills": adjusted}
