# SkillTreeEvolver

🎉 **AI Agent Skill Tree Self-Evolution Engine** — Empower AI agents to grow like RPG characters, unlocking and leveling up skill nodes through use and training.

[English](README_en.md) · [简体中文](README_zh.md) · [繁體中文](README_zh_TW.md) · [日本語](README_ja.md)

---

## 🎯 Core Value

In LLM application development, AI agent capabilities are typically limited by pre-defined tools and prompts. **SkillTreeEvolver** draws from RPG-style Skill Tree concepts to give AI agents a **quantifiable, accumulative, self-evolving** capability management system.

- **RPG-style growth**: Skills have levels, XP, and proficiency — success accumulates growth
- **Token cost visualization**: Built-in token tracker quantifies cost vs. benefit per skill call
- **Multi-backend compatible**: Claude / GPT-4 / DeepSeek all supported via unified adapter layer
- **Zero-dependency lightweight**: Python 3.8+ only, no heavy ML frameworks, plug and play

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🗺️ **Skill Tree Visualization** | ASCII/CLI dual-mode skill tree, clear hierarchy and progress |
| ⬆️ **Self-Evolution Engine** | Auto-adjusts skill weights and priorities based on usage, success rate, duration |
| 📊 **Multi-Dimensional Scoring** | Mastery + Efficiency + Versatility scoring for every skill |
| 💰 **Token Consumption Tracking** | Records per-skill token usage, auto-computes cost and savings |
| 🔄 **Skill Discovery & Recommendation** | Auto-discovers new skills from context, recommends optimal learning path |
| 🔌 **Multi-LLM Adapters** | Claude / OpenAI / DeepSeek unified abstraction, easy switching |
| 🌏 **Developer-Friendly Docs** | Full documentation in English, Chinese, Japanese, and more |

---

## 🚀 Quick Start

### Requirements

- Python 3.8+
- Git
- Network access

### Installation

```bash
# From PyPI (recommended)
pip install skilltree-evolver

# From source
git clone https://github.com/gitstq/SkillTreeEvolver.git
cd SkillTreeEvolver
pip install -e ".[all]"
```

### Initialize Skill Tree

```bash
skilltree tree --init --depth 3
```

### Core Commands

```bash
# View skill tree
skilltree tree --depth 3

# Discover skills from keywords
skilltree learn --discover "database,cache" --category coding

# Get next skill recommendations
skilltree learn --suggest

# Rank skills by score
skilltree eval --rank

# Record token usage
skilltree token --record "coding,5000,2000,gpt-4o-mini"

# Generate token report
skilltree token --report
```

---

## 📖 Detailed Usage

### Built-in Skill Tree (17 skills)

```
Coding
├── Code Review
├── Bug Fixing
├── Refactoring
├── Testing
└── API Design

Reasoning
├── Problem Decomposition
├── Root Cause Analysis
└── Decision Making

Research
├── Web Search
└── Document Synthesis

Writing
├── Technical Documentation
├── Creative Writing
└── Translation
```

### Python API

```python
from core import SkillTree, SkillNode, EvolutionEngine, SkillEvaluator

tree = SkillTree("skilltree_data.json")
tree.load()

engine = EvolutionEngine(tree)
new_skill = engine.discover_new_skill({
    "keywords": ["distributed"],
    "task_type": "coding"
})
tree.add_skill(new_skill)

evaluator = SkillEvaluator(tree)
ranked = evaluator.rank_skills()
weak = evaluator.get_weak_skills(threshold=30)
```

---

## 💡 Design Philosophy & Roadmap

### Design

The core idea: **make AI agent capability growth transparent and quantifiable**. Unlike traditional agents relying on manual tuning, SkillTreeEvolver introduces a self-driven evolution mechanism:

1. **Gamified feedback**: Every success = visible growth (XP ↑, level ↑)
2. **Data-driven optimization**: Token tracking makes every dollar traceable
3. **Proactive discovery**: Evolution engine discovers skills, not just records them

### Roadmap

- [ ] **Web UI**: Gradio/Streamlit-based visualization
- [ ] **Persistent storage**: SQLite/PostgreSQL backend support
- [ ] **Framework integration**: LangChain/LlamaIndex deep integration
- [ ] **Community skill library**: User-contributed skill packs
- [ ] **Evolution history**: Growth curves and milestone tracking

---

## 📦 Packaging & Deployment

```bash
# Build wheel
pip install build
python -m build

# Publish to PyPI
pip install twine
twine upload dist/*
```

---

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Commits follow Angular Convention.

---

## 📄 License

MIT License — see [LICENSE](LICENSE).

---

<div align="center">

**If this project helps you, please give it a Star ⭐**

</div>
