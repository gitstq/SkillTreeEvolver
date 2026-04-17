# SkillTreeEvolver

🎉 **AI Agent 技能树自进化引擎** — 让 AI Agent 像 RPG 游戏角色一样，通过使用和训练不断解锁、升级技能节点，实现能力的自主进化与优化。

[English](README_en.md) · [简体中文](README_zh.md) · [繁體中文](README_zh_TW.md) · [日本語](README_ja.md)

---

## 🎯 项目核心价值

在 LLM 应用开发中，AI Agent 的能力边界往往取决于预定义的工具和提示词。**SkillTreeEvolver** 借鉴 RPG 游戏中的技能树（Skill Tree）概念，为 AI Agent 引入了一套**可量化、可积累、可进化**的能力管理系统。

- **像游戏一样成长**：技能有等级、经验值（XP）、熟练度，每次成功执行都积累成长
- **Token 消耗可视化**：内置 Token 追踪器，量化每次技能调用的成本与收益
- **多后端兼容**：Claude / GPT-4 / DeepSeek 等主流 LLM 均可无缝切换
- **零依赖轻量化**：仅需 Python 3.8+，无需重型 ML 框架，开箱即用

---

## ✨ 核心特性

| 特性 | 说明 |
|------|------|
| 🗺️ **技能树可视化** | ASCII/CLI 双模式技能树图谱，清晰展示技能层级与成长进度 |
| ⬆️ **自进化机制** | 根据使用频率、成功率、耗时自动调整技能权重与优先级 |
| 📊 **多维评分体系** | 从掌握度、效率、通用性三个维度综合评估每个技能 |
| 💰 **Token 消耗追踪** | 记录每个技能调用的 Token 消耗，自动计算成本与节省比例 |
| 🔄 **技能发现与推荐** | 基于上下文自动发现新技能，推荐最优学习路径 |
| 🔌 **多 LLM 适配器** | Claude / OpenAI / DeepSeek 统一抽象，快速切换 |
| 🌏 **中文优先文档** | 中文 README 全程护航，降低上手门槛 |

---

## 🚀 快速开始

### 环境要求

- Python 3.8+
- Git
- 网络环境（访问 GitHub / PyPI）

### 安装

```bash
# 从 PyPI 安装（推荐）
pip install skilltree-evolver

# 或从源码安装
git clone https://github.com/gitstq/SkillTreeEvolver.git
cd SkillTreeEvolver
pip install -e ".[all]"
```

> 💡 中国大陆用户建议使用清华镜像：
> ```bash
> pip install skilltree-evolver -i https://pypi.tuna.tsinghua.edu.cn/simple
> ```

### 初始化技能树

```bash
skilltree tree --init --depth 3
```

输出示例：
```
[+] Initialized skill tree with 17 skills.
[ ] Coding (Lv.1) 0/100xp
  +-- [ ] Code Review (Lv.1) 0/80xp
  +-- [ ] Bug Fixing (Lv.1) 0/80xp
  +-- [ ] Refactoring (Lv.1) 0/120xp
  ...
```

### 核心命令

```bash
# 查看技能树
skilltree tree --depth 3

# 技能发现：从关键词探索新技能
skilltree learn --discover "database,cache,distributed" --category coding

# 技能推荐：获取下一步学习建议
skilltree learn --suggest

# 技能评估：排行榜
skilltree eval --rank

# Token 追踪：记录使用量
skilltree token --record "coding,5000,2000,gpt-4o-mini"

# Token 报告：生成 Markdown 报告
skilltree token --report
```

---

## 📖 详细使用指南

### 1. 技能树结构

内置 17 个初始技能，覆盖四大领域：

```
Coding（编程）
├── Code Review（代码审查）
├── Bug Fixing（缺陷修复）
├── Refactoring（代码重构）
├── Testing（测试）
└── API Design（API 设计）

Reasoning（推理）
├── Problem Decomposition（问题分解）
├── Root Cause Analysis（根因分析）
└── Decision Making（决策）

Research（研究）
├── Web Search（网页搜索）
└── Document Synthesis（文档综合）

Writing（写作）
├── Technical Documentation（技术文档）
├── Creative Writing（创意写作）
└── Translation（翻译）
```

### 2. 技能升级机制

- **XP 积累**：每次成功执行 +10 XP，失败 +3 XP
- **升级阈值**：每升一级所需 XP × 1.5
- **多维追踪**：成功率、平均耗时、使用次数全程记录

### 3. Token 消耗追踪

内置 Token 追踪器支持以下模型：

| 模型 | 输入成本 (/1M) | 输出成本 (/1M) |
|------|-------------|-------------|
| Claude 3.5 Sonnet | $3.00 | $15.00 |
| GPT-4o | $5.00 | $15.00 |
| GPT-4o-mini | $0.15 | $0.60 |
| DeepSeek Chat | $0.27 | $1.10 |

### 4. 进化引擎 API

```python
from core import SkillTree, SkillNode, EvolutionEngine, SkillEvaluator

# 初始化
tree = SkillTree()
tree.load("skilltree_data.json")

# 发现新技能
engine = EvolutionEngine(tree)
new_skill = engine.discover_new_skill({
    "keywords": ["distributed", "consensus"],
    "task_type": "coding"
})
if new_skill:
    tree.add_skill(new_skill)

# 获取学习建议
suggestions = engine.suggest_next_skill("coding")
for s in suggestions:
    print(f"建议学习: {s.name}")

# 技能评估
evaluator = SkillEvaluator(tree)
ranked = evaluator.rank_skills()
weak = evaluator.get_weak_skills(threshold=30)
```

---

## 💡 设计思路与迭代规划

### 设计思路

本项目的核心理念是**将 AI Agent 的能力成长过程透明化、可量化**。传统 AI Agent 的能力增强依赖于手工配置和调优，而 SkillTreeEvolver 引入了一套类似于 RPG 游戏技能树的自驱动进化机制：

1. **游戏化反馈**：每一次成功执行都带来可见的成长（XP ↑，等级 ↑）
2. **数据驱动优化**：Token 追踪让每一分钱的价值都有迹可循
3. **自主发现**：进化引擎不只是被动记录，更能主动发现新技能

### 后续迭代

- [ ] **Web UI**：基于 Gradio/Streamlit 的技能树可视化界面
- [ ] **持久化存储**：支持 SQLite/PostgreSQL 多后端
- [ ] **集成层**：与 LangChain/LlamaIndex 等主流框架深度集成
- [ ] **社区技能库**：用户可贡献和分享自定义技能包
- [ ] **进化历史**：技能成长曲线图谱与里程碑记录

---

## 📦 打包与部署

```bash
# 构建 wheel 包
pip install build
python -m build

# 构建源码包
python -m build --sdist

# 发布到 TestPyPI
pip install twine
twine upload --repository testpypi dist/*
```

### Docker 部署

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY . .
RUN pip install -e ".[all]" -i https://pypi.tuna.tsinghua.edu.cn/simple
CMD ["skilltree", "tree", "--init"]
```

---

## 🤝 贡献指南

欢迎贡献代码！请参阅 [CONTRIBUTING.md](CONTRIBUTING.md)。

提交规范遵循 Angular Commit Convention：
- `feat:` 新功能
- `fix:` 错误修复
- `docs:` 文档更新
- `refactor:` 代码重构
- `test:` 测试相关

---

## 📄 开源协议

本项目基于 [MIT License](LICENSE) 开源。

---

<div align="center">

**如果这个项目对您有帮助，欢迎 Star ⭐**

</div>
