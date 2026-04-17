import pytest
import os
import tempfile
from core import SkillTree, SkillNode, EvolutionEngine, SkillEvaluator, TokenTracker


def test_skill_node():
    node = SkillNode(
        skill_id="test1", name="Test Skill", description="A test skill", category="test"
    )
    assert node.skill_id == "test1"
    assert node.level == 1
    assert node.xp_current == 0
    assert node.xp_progress == 0.0
    assert node.success_rate == 0.0


def test_skill_tree_add():
    tree = SkillTree()
    node = SkillNode(skill_id="coding", name="Coding", description="Coding", category="dev")
    tree.add_skill(node)
    assert "coding" in tree.nodes
    assert tree.nodes["coding"].name == "Coding"


def test_award_xp_level_up():
    tree = SkillTree()
    node = SkillNode(skill_id="test", name="Test", description="T", category="t", xp_required=50)
    tree.add_skill(node)
    tree.award_xp("test", 60, success=True)
    assert tree.nodes["test"].level == 2
    assert tree.nodes["test"].xp_current == 10


def test_children_and_parents():
    tree = SkillTree()
    parent = SkillNode(skill_id="p", name="Parent", description="P", category="c")
    child = SkillNode(skill_id="c", name="Child", description="C", category="c", parent_id="p")
    tree.add_skill(parent)
    tree.add_skill(child)
    children = tree.get_children("p")
    assert len(children) == 1
    assert children[0].skill_id == "c"


def test_tree_save_load():
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False, encoding="utf-8") as f:
        path = f.name
    try:
        tree = SkillTree(path)
        node = SkillNode(skill_id="s1", name="S1", description="D", category="c")
        tree.add_skill(node)
        tree.save()
        tree2 = SkillTree(path)
        tree2.load()
        assert "s1" in tree2.nodes
        assert tree2.nodes["s1"].name == "S1"
    finally:
        if os.path.exists(path):
            os.remove(path)


def test_evolution_discover():
    tree = SkillTree()
    node = SkillNode(skill_id="coding", name="Coding", description="C", category="coding")
    tree.add_skill(node)
    engine = EvolutionEngine(tree)
    result = engine.discover_new_skill({"keywords": ["database"], "task_type": "coding"})
    assert result is not None
    assert "database" in result.name.lower()


def test_evaluator_rank():
    tree = SkillTree()
    for i in range(3):
        node = SkillNode(
            skill_id=f"s{i}", name=f"Skill{i}", description="D", category="c",
            usage_count=5, success_count=4, level=i + 1
        )
        tree.add_skill(node)
    ev = SkillEvaluator(tree)
    ranked = ev.rank_skills()
    assert len(ranked) == 3
    assert ranked[0]["overall_score"] >= ranked[-1]["overall_score"]


def test_token_tracker():
    tracker = TokenTracker()
    rec = tracker.record("skill1", 1000, 500, "gpt-4o-mini", success=True)
    assert rec.total_tokens == 1500
    summary = tracker.get_skill_summary("skill1")
    assert summary["calls"] == 1
    assert summary["total_tokens"] == 1500
    overall = tracker.get_overall_summary()
    assert overall["total_calls"] == 1
    assert overall["total_tokens"] == 1500


def test_render_ascii():
    tree = SkillTree()
    parent = SkillNode(skill_id="root", name="Root", description="R", category="r")
    child = SkillNode(skill_id="leaf", name="Leaf", description="L", category="r", parent_id="root")
    tree.add_skill(parent)
    tree.add_skill(child)
    output = tree.render_ascii(max_depth=2)
    assert "Root" in output
    assert "Leaf" in output
