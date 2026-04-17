"""SkillTreeEvolver CLI - Main command interface."""
import sys
import argparse
from pathlib import Path
import json

sys.path.insert(0, str(Path(__file__).parent.parent))

from core import SkillTree, SkillNode, EvolutionEngine, SkillEvaluator, TokenTracker, DEFAULT_SKILLS


def cmd_tree(args):
    tree = SkillTree(args.data)
    if args.init:
        for skill in DEFAULT_SKILLS:
            tree.add_skill(SkillNode(**skill))
        tree.save()
        print(f"[+] Initialized skill tree with {len(DEFAULT_SKILLS)} skills.")
    print(tree.render_ascii(max_depth=args.depth))
    stats = tree.get_stats()
    print(f"\nStats: {stats['total_skills']} skills, total usage: {stats.get('total_usage', 0)}, avg level: {stats.get('avg_level', 0):.1f}")
    return 0


def cmd_learn(args):
    tree = SkillTree(args.data)
    engine = EvolutionEngine(tree)
    if args.discover:
        context = {"keywords": args.discover.split(","), "task_type": args.category or "general"}
        skill = engine.discover_new_skill(context)
        if skill:
            tree.add_skill(skill)
            tree.save()
            print(f"[+] Discovered new skill: {skill.name} ({skill.skill_id})")
        else:
            print("[*] No new skills discovered from context.")
    if args.suggest:
        suggestions = engine.suggest_next_skill(args.current)
        if suggestions:
            print("[*] Suggested skills to learn:")
            for s in suggestions:
                print(f"  - {s.name} ({s.category}) Lv.{s.level} | XP: {s.xp_current}/{s.xp_required} | Success: {s.success_rate*100:.0f}%")
        else:
            print("[*] Add more skills to get suggestions.")
    return 0


def cmd_eval(args):
    tree = SkillTree(args.data)
    evaluator = SkillEvaluator(tree)
    if args.rank:
        ranked = evaluator.rank_skills()
        print("[*] Top skills by overall score:")
        for i, s in enumerate(ranked[:10]):
            print(f"  {i+1}. {s['name']}: overall={s['overall_score']} (mastery={s['mastery_score']}, eff={s['efficiency_score']}, vers={s['versatility_score']})")
    if args.weak:
        weak = evaluator.get_weak_skills()
        if weak:
            print("[*] Skills needing improvement:")
            for s in weak[:5]:
                print(f"  - {s['name']}: {s['overall_score']:.1f}")
        else:
            print("[*] All skills are performing well!")
    return 0


def cmd_token(args):
    tracker = TokenTracker()
    if args.data:
        tracker.load(args.data)
    if args.record:
        parts = args.record.split(",")
        if len(parts) >= 4:
            skill_id, inp, outp, model = parts[0], int(parts[1]), int(parts[2]), parts[3]
        else:
            skill_id, inp, outp, model = parts[0], int(parts[1]), int(parts[2]), "default"
        tracker.record(skill_id, inp, outp, model)
        if args.data:
            tracker.save(args.data)
        print(f"[+] Recorded: {inp+outp} tokens for {skill_id}")
    summary = tracker.get_overall_summary()
    print(f"\n[*] Token Summary:")
    print(f"  Total calls: {summary['total_calls']}")
    print(f"  Total tokens: {summary['total_tokens']:,}")
    print(f"  Total cost: ${summary['total_cost_usd']:.6f}")
    print(f"  Savings: ${summary.get('savings_vs_baseline_usd', 0):.6f}")
    if args.report:
        print("\n" + tracker.get_token_report())
    return 0


def cmd_stats(args):
    tree = SkillTree(args.data)
    by_cat = tree.get_category_tree()
    print(f"[*] Skill Tree Stats ({args.data})")
    print(f"  Total: {len(tree.nodes)} skills across {len(by_cat)} categories")
    for cat, skills in sorted(by_cat.items()):
        avg_lv = sum(s.level for s in skills) / len(skills)
        print(f"  [{cat}] {len(skills)} skills, avg level {avg_lv:.1f}")
    return 0


def main():
    parser = argparse.ArgumentParser(
        prog="skilltree",
        description="SkillTreeEvolver - AI Agent Skill Tree Self-Evolution Engine",
    )
    parser.add_argument("--data", default="skilltree_data.json", help="Data file path")
    sub = parser.add_subparsers(dest="cmd")

    p_tree = sub.add_parser("tree", help="Show skill tree")
    p_tree.add_argument("--init", action="store_true", help="Initialize with default skills")
    p_tree.add_argument("--depth", type=int, default=3, help="Max display depth")
    p_tree.set_defaults(fn=cmd_tree)

    p_learn = sub.add_parser("learn", help="Learn/discover skills")
    p_learn.add_argument("--discover", metavar="KW", help="Discover skills from keywords")
    p_learn.add_argument("--suggest", action="store_true", help="Suggest next skills")
    p_learn.add_argument("--current", help="Current skill ID")
    p_learn.add_argument("--category", help="Task category")
    p_learn.set_defaults(fn=cmd_learn)

    p_eval = sub.add_parser("eval", help="Evaluate skills")
    p_eval.add_argument("--rank", action="store_true", help="Rank all skills")
    p_eval.add_argument("--weak", action="store_true", help="Show weak skills")
    p_eval.set_defaults(fn=cmd_eval)

    p_token = sub.add_parser("token", help="Token usage tracking")
    p_token.add_argument("--record", metavar="SKILL,IN,OUT,MODEL", help="Record token usage")
    p_token.add_argument("--report", action="store_true", help="Generate full report")
    p_token.set_defaults(fn=cmd_token)

    p_stats = sub.add_parser("stats", help="Show tree statistics")
    p_stats.set_defaults(fn=cmd_stats)

    args = parser.parse_args()
    if not args.cmd:
        parser.print_help()
        return 0
    return args.fn(args)


if __name__ == "__main__":
    sys.exit(main())
