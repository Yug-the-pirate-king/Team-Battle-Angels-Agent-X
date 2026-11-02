# 🚀 Quickstart Guide - Team Battle Angels: Agent X

Welcome to **Agent X**, the autonomous AI software engineering agent developed by **Team Battle Angels**.

This guide will get you up and running with Agent X in under **2 minutes**.

---

## 📋 Prerequisites

- **Python 3.10+** (Python 3.10, 3.11, 3.12, or 3.13)
- An API key for your preferred LLM provider:
  - OpenAI (`OPENAI_API_KEY`)
  - Anthropic (`ANTHROPIC_API_KEY`)
  - Google Gemini (`GEMINI_API_KEY`)
  - OpenRouter (`OPENROUTER_API_KEY`)
  - *Or* a local Ollama instance (No API key needed!)

---

## ⚡ 3-Step Setup

### Step 1: Install Dependencies

```bash
# In the project directory:
pip install -r requirements.txt
pip install -e .
```

### Step 2: Configure Environment & API Keys

Copy the sample environment file:
```bash
# Windows:
copy .env.example .env

# macOS / Linux:
cp .env.example .env
```

Open `.env` and enter your preferred API key:
```env
OPENAI_API_KEY=sk-proj-your-openai-api-key-here
MSWEA_MODEL_NAME=openai/gpt-4o
```

*(You can also set environment variables directly in your terminal if you prefer)*:
```powershell
$env:OPENAI_API_KEY="your-api-key"
```

### Step 3: Run the Agent

You have 3 easy ways to run Agent X:

#### Option A: Autonomous Mode (Recommended for Hackathon Tasks)
Solve a coding task automatically without waiting for confirmation:
```bash
battle-angels --task "Fix the bug in app.py where divide by zero is unhandled" --yolo
```

#### Option B: Interactive Mode (Human-in-the-Loop)
Prompt the agent interactively step-by-step:
```bash
battle-angels
```

#### Option C: Python Script / Demo Runner
```bash
python run_demo.py
```

---

## 🔍 Inspecting Trajectories

Agent X logs every decision, bash command, tool output, and code diff to a `.traj.json` file.
You can view the full execution trajectory using the built-in inspector:

```bash
mini-extra inspect last_run.traj.json
```
Navigate steps using `Left` / `Right` arrows and view model reasoning and execution logs!
