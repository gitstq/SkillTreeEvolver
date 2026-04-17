# SkillTreeEvolver

🎉 **AI Agent スキルツリー自己進化エンジン** — AI Agent を RPG ゲームのキャラクターのように、使用と訓練を通じてスキルノードのロックを解除・レベルアップさせ、能力を自律的に進化させます。

[English](README_en.md) · [简体中文](README_zh.md) · [繁體中文](README_zh_TW.md) · [日本語](README_ja.md)

---

## 🎯 プロジェクトの中核的価値

LLM アプリケーション開発において、AI Agent の能力は通常、事前に定義されたツールやプロンプトによって制限されます。**SkillTreeEvolver** は RPG のスキルツリー概念を取り入れ、AI Agent に**定量化可能・蓄積可能・自己進化可能**な能力管理システムを実装します。

- **RPG のような成長**：スキルにはレベル、XP、習熟度があり、成功するたびに成長を蓄積
- **トークン消費の可視化**：組み込みトークントラッカーで、各スキル呼び出しのコスト対効果を定量化
- **マルチバックエンド対応**：Claude / GPT-4 / DeepSeek をユニファイドアダプターレイヤーでサポート
- **ゼロ依存軽量設計**：Python 3.8+ のみ、重い ML フレームワーク不要

---

## ✨ コア機能

| 機能 | 説明 |
|------|------|
| 🗺️ **スキルツリー可視化** | ASCII/CLI デュアルモードでスキル階層と進捗をクリアに表示 |
| ⬆️ **自己進化エンジン** | 使用頻度・成功率・実行時間に基づいてスキル重みと優先度を自動調整 |
| 📊 **多次元スコアリング** | 各スキルを習熟度・効率・汎用性の3次元で評価 |
| 💰 **トークン消費追跡** | スキルごとのトークン使用量を記録し、コストと節約額を自動計算 |
| 🔄 **スキル発見と推奨** | コンテキストから新規スキルを自動発見、最適な学習パスを推奨 |
| 🔌 **マルチLLM アダプター** | Claude / OpenAI / DeepSeek を統一抽象화로簡単に切り替え |
| 🌏 **包括的なドキュメント** | 英語・中国語・日本語など複数言語のドキュメントを提供 |

---

## 🚀 クイックスタート

### 必要環境

- Python 3.8+
- Git

### インストール

```bash
# PyPI からインストール
pip install skilltree-evolver

# ソースからインストール
git clone https://github.com/gitstq/SkillTreeEvolver.git
cd SkillTreeEvolver
pip install -e ".[all]"
```

> 💡 中国本土ユーザーは以下を推奨：
> ```bash
> pip install skilltree-evolver -i https://pypi.tuna.tsinghua.edu.cn/simple
> ```

### スキルツリーの初期化

```bash
skilltree tree --init --depth 3
```

### 主要コマンド

```bash
# スキルツリーを表示
skilltree tree --depth 3

# キーワードからスキルを発見
skilltree learn --discover "database,cache" --category coding

# 次に学ぶべきスキルを提案
skilltree learn --suggest

# スキルスコアランキング
skilltree eval --rank

# トークン使用量を記録
skilltree token --record "coding,5000,2000,gpt-4o-mini"

# トークンレポートを生成
skilltree token --report
```

---

## 📖 詳細な使用方法

### 組み込みスキルツリー（17スキル）

```
Coding（コーディング）
├── Code Review（コードレビュー）
├── Bug Fixing（バグ修正）
├── Refactoring（リファクタリング）
├── Testing（テスト）
└── API Design（API 設計）

Reasoning（推論）
├── Problem Decomposition（問題分解）
├── Root Cause Analysis（根本原因分析）
└── Decision Making（意思決定）

Research（リサーチ）
├── Web Search（ウェブ検索）
└── Document Synthesis（文書統合）

Writing（ライティング）
├── Technical Documentation（技術文書）
├── Creative Writing（クリエイティブライティング）
└── Translation（翻訳）
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

## 💡 設計思想とロードマップ

### 設計思想

AI Agent の能力成長のプロセスを**透明化・定量化**することが本プロジェクトの核心的な考え方です。

1. **ゲーミフィケーションフィードバック**：成功するたびに目に見える成長（XP ↑、レベル ↑）
2. **データ駆動型最適化**：トークン追跡により每一分钱每ドル都有踪跡
3. **能動的発見**：進化エンジンはスキルを能動的に発見

### ロードマップ

- [ ] **Web UI**：Gradio/Streamlit ベースの可視化
- [ ] **永続化ストレージ**：SQLite/PostgreSQL バックエンドサポート
- [ ] **フレームワーク統合**：LangChain/LlamaIndex との深統合
- [ ] **コミュニティスキルライブラリ**：ユーザー投稿スキルパック
- [ ] **進化履歴**：成長曲線とマイルストーン追跡

---

## 🤝 コントリビュート

[CONTRIBUTING.md](CONTRIBUTING.md) をご覧ください。コミットは Angular Convention に従います。

---

## 📄 ライセンス

MIT License — [LICENSE](LICENSE) をご覧ください。

---

<div align="center">

**このプロジェクトが役立った方は Star ⭐ を押してください**

</div>
