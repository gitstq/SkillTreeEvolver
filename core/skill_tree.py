"""Skill Tree Data Structure - Core of the Evolution System"""
from __future__ import annotations
import json
import uuid
from datetime import datetime
from typing import Optional
from dataclasses import dataclass, field, asdict


@dataclass
class SkillNode:
    """Single skill node in the tree."""
    skill_id: str
    name: str
    description: str
    category: str
    level: int = 1
    xp_required: int = 100
    xp_current: int = 0
    parent_id: Optional[str] = None
    children_ids: list = field(default_factory=list)
    dependencies: list = field(default_factory=list)
    tags: list = field(default_factory=list)
    usage_count: int = 0
    success_count: int = 0
    avg_duration_ms: float = 0.0
    last_used: Optional[str] = None
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    metadata: dict = field(default_factory=dict)

    @property
    def xp_progress(self) -> float:
        return min(1.0, self.xp_current / self.xp_required) if self.xp_required > 0 else 0.0

    @property
    def success_rate(self) -> float:
        return self.success_count / self.usage_count if self.usage_count > 0 else 0.0

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "SkillNode":
        return cls(**data)


class SkillTree:
    """Skill Tree Manager - Handles the entire skill graph."""

    def __init__(self, data_path: Optional[str] = None):
        self.nodes: dict[str, SkillNode] = {}
        self.root_ids: list[str] = []
        self.categories: set[str] = set()
        self.data_path = data_path
        if data_path:
            self.load()

    def add_skill(self, skill: SkillNode) -> str:
        """Add a new skill to the tree."""
        if skill.skill_id in self.nodes:
            raise ValueError(f"Skill {skill.skill_id} already exists")
        self.nodes[skill.skill_id] = skill
        self.categories.add(skill.category)
        if skill.parent_id is None and skill.skill_id not in self.root_ids:
            self.root_ids.append(skill.skill_id)
        elif skill.parent_id and skill.parent_id in self.nodes:
            if skill.skill_id not in self.nodes[skill.parent_id].children_ids:
                self.nodes[skill.parent_id].children_ids.append(skill.skill_id)
        return skill.skill_id

    def get_skill(self, skill_id: str) -> Optional[SkillNode]:
        return self.nodes.get(skill_id)

    def get_children(self, skill_id: str) -> list[SkillNode]:
        skill = self.nodes.get(skill_id)
        if not skill:
            return []
        return [self.nodes[cid] for cid in skill.children_ids if cid in self.nodes]

    def get_ancestors(self, skill_id: str) -> list[SkillNode]:
        """Get all ancestor skills (unlocked path to root)."""
        ancestors = []
        current = self.nodes.get(skill_id)
        while current and current.parent_id:
            parent = self.nodes.get(current.parent_id)
            if parent:
                ancestors.append(parent)
                current = parent
            else:
                break
        return ancestors

    def award_xp(self, skill_id: str, amount: int, success: bool = True) -> None:
        """Award XP to a skill and handle leveling."""
        skill = self.nodes.get(skill_id)
        if not skill:
            return
        skill.xp_current += amount
        skill.usage_count += 1
        if success:
            skill.success_count += 1
        skill.last_used = datetime.utcnow().isoformat()
        # Level up check
        while skill.xp_current >= skill.xp_required:
            skill.xp_current -= skill.xp_required
            skill.level += 1
            skill.xp_required = int(skill.xp_required * 1.5)

    def update_stats(self, skill_id: str, duration_ms: float, success: bool) -> None:
        """Update skill statistics after execution."""
        skill = self.nodes.get(skill_id)
        if not skill:
            return
        # Running average
        n = skill.usage_count
        skill.avg_duration_ms = ((n - 1) * skill.avg_duration_ms + duration_ms) / n if n > 0 else duration_ms
        self.award_xp(skill_id, 10 if success else 3, success)

    def render_ascii(self, root_id: Optional[str] = None, max_depth: int = 3, current_depth: int = 0) -> str:
        """Render skill tree as ASCII art."""
        lines = []
        if root_id is None:
            for rid in self.root_ids:
                lines.extend(self._render_node_ascii(rid, current_depth, max_depth))
            return "\n".join(lines)
        return "\n".join(self._render_node_ascii(root_id, current_depth, max_depth))

    def _render_node_ascii(self, skill_id: str, depth: int, max_depth: int) -> list[str]:
        if depth > max_depth:
            return []
        skill = self.nodes.get(skill_id)
        if not skill:
            return []
        indent = "  " * depth
        prefix = "+-- " if depth > 0 else ""
        status = "[*]" if skill.xp_current >= skill.xp_required else "[ ]"
        lines = [f"{indent}{prefix}{status} {skill.name} (Lv.{skill.level}) {skill.xp_current}/{skill.xp_required}xp"]
        for child_id in skill.children_ids[:5]:
            lines.extend(self._render_node_ascii(child_id, depth + 1, max_depth))
        return lines

    def to_dict(self) -> dict:
        return {
            "nodes": {sid: node.to_dict() for sid, node in self.nodes.items()},
            "root_ids": self.root_ids,
            "categories": list(self.categories),
        }

    def save(self, path: Optional[str] = None) -> None:
        p = path or self.data_path
        if not p:
            raise ValueError("No data path specified")
        with open(p, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, ensure_ascii=False, indent=2)

    def load(self, path: Optional[str] = None) -> None:
        p = path or self.data_path
        if not p:
            return
        try:
            with open(p, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.nodes = {sid: SkillNode.from_dict(nd) for sid, nd in data.get("nodes", {}).items()}
            self.root_ids = data.get("root_ids", [])
            self.categories = set(data.get("categories", []))
        except (FileNotFoundError, json.JSONDecodeError):
            pass

    def get_category_tree(self) -> dict[str, list[SkillNode]]:
        """Group skills by category."""
        result: dict[str, list[SkillNode]] = {}
        for skill in self.nodes.values():
            if skill.category not in result:
                result[skill.category] = []
            result[skill.category].append(skill)
        return result

    def get_stats(self) -> dict:
        """Get overall tree statistics."""
        total = len(self.nodes)
        if total == 0:
            return {"total_skills": 0}
        total_usage = sum(s.usage_count for s in self.nodes.values())
        total_success = sum(s.success_count for s in self.nodes.values())
        avg_level = sum(s.level for s in self.nodes.values()) / total
        return {
            "total_skills": total,
            "total_usage": total_usage,
            "avg_success_rate": total_success / total_usage if total_usage > 0 else 0,
            "avg_level": avg_level,
            "categories": len(self.categories),
        }
