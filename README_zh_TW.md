# SkillTreeEvolver

🎉 **AI Agent 技能樹自進化引擎** — 讓 AI Agent 像 RPG 遊戲角色一樣，透過使用和訓練不斷解鎖、升級技能節點，實現能力的自主進化與優化。

[English](README_en.md) · [简体中文](README_zh.md) · [繁體中文](README_zh_TW.md) · [日本語](README_ja.md)

---

## 🎯 專案核心價值

在 LLM 應用開發中，AI Agent 的能力邊界往往取決於預定義的工具和提示詞。**SkillTreeEvolver** 借鑒 RPG 遊戲中的技能樹（Skill Tree）概念，為 AI Agent 引入了一套**可量化、可累積、可進化**的能力管理系統。

- **像遊戲一樣成長**：技能有等級、經驗值（XP）、熟練度，每次成功執行都累積成長
- **Token 消耗可視化**：內建 Token 追蹤器，量化每次技能呼叫的成本與收益
- **多後端相容**：Claude / GPT-4 / DeepSeek 等主流 LLM 均可無縫切換
- **零依賴輕量化**：僅需 Python 3.8+，無需重型 ML 框架，開箱即用

---

## ✨ 核心特性

| 特性 | 說明 |
|------|------|
| 🗺️ **技能樹可視化** | ASCII/CLI 雙模式技能樹圖譜，清晰展示技能層級與成長進度 |
| ⬆️ **自進化機制** | 根據使用頻率、成功率、耗時自動調整技能權重與優先級 |
| 📊 **多維評分體系** | 從掌握度、效率、通用性三個維度綜合評估每個技能 |
| 💰 **Token 消耗追蹤** | 記錄每個技能呼叫的 Token 消耗，自動計算成本與節省比例 |
| 🔄 **技能發現與推薦** | 基於上下文自動發現新技能，推薦最優學習路徑 |
| 🔌 **多 LLM 適配器** | Claude / OpenAI / DeepSeek 統一抽象，快速切換 |
| 🌏 **中文優先文件** | 中文 README 全程護航，降低上手門檻 |

---

## 🚀 快速開始

### 環境要求

- Python 3.8+
- Git
- 網路環境

### 安裝

```bash
# 從 PyPI 安裝
pip install skilltree-evolver

# 或從原始碼安裝
git clone https://github.com/gitstq/SkillTreeEvolver.git
cd SkillTreeEvolver
pip install -e ".[all]"
```

### 初始化技能樹

```bash
skilltree tree --init --depth 3
```

### 核心指令

```bash
# 查看技能樹
skilltree tree --depth 3

# 技能發現：從關鍵詞探索新技能
skilltree learn --discover "database,cache" --category coding

# 技能推薦：獲取下一步學習建議
skilltree learn --suggest

# 技能評估：排行榜
skilltree eval --rank

# Token 追蹤：記錄使用量
skilltree token --record "coding,5000,2000,gpt-4o-mini"
```

---

## 📖 詳細使用指南

### 內建技能樹結構（17 個技能）

```
Coding（程式設計）
├── Code Review（程式碼審查）
├── Bug Fixing（缺陷修復）
├── Refactoring（重構）
├── Testing（測試）
└── API Design（API 設計）

Reasoning（推理）
├── Problem Decomposition（問題分解）
├── Root Cause Analysis（根因分析）
└── Decision Making（決策）

Research（研究）
├── Web Search（網頁搜尋）
└── Document Synthesis（文獻綜合）

Writing（寫作）
├── Technical Documentation（技術文檔）
├── Creative Writing（創意寫作）
└── Translation（翻譯）
```

### Python API

```python
from core import SkillTree, EvolutionEngine, SkillEvaluator

tree = SkillTree("skilltree_data.json")
engine = EvolutionEngine(tree)
new_skill = engine.discover_new_skill({
    "keywords": ["distributed"],
    "task_type": "coding"
})
tree.add_skill(new_skill)

evaluator = SkillEvaluator(tree)
ranked = evaluator.rank_skills()
```

---

## 💡 設計思路與迭代規劃

### 設計思路

將 AI Agent 的能力成長過程**透明化、可量化**。借鑒 RPG 技能樹概念，引入自驅動進化機制：

1. **遊戲化回饋**：每次成功執行帶來可見的成長
2. **數據驅動優化**：Token 追蹤讓每一分錢的價值都有跡可循
3. **自主發現**：進化引擎主動發現新技能，而非被動記錄

### 後續迭代

- [ ] **Web UI**：Gradio/Streamlit 可視化介面
- [ ] **持久化儲存**：SQLite/PostgreSQL 多後端支援
- [ ] **框架整合**：LangChain/LlamaIndex 深度整合
- [ ] **社群技能庫**：使用者貢獻和分享自訂技能包
- [ ] **進化歷史**：技能成長曲線圖譜

---

## 🤝 貢獻指南

歡迎貢獻程式碼！請參閱 [CONTRIBUTING.md](CONTRIBUTING.md)。

提交規範遵循 Angular Commit Convention。

---

## 📄 開源協議

本專案基於 [MIT License](LICENSE) 開源。

---

<div align="center">

**如果這個專案對您有幫助，歡迎 Star ⭐**

</div>
