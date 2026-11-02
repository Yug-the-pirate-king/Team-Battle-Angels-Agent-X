# 🎬 Hackathon Demo Guide - Team Battle Angels

This guide provides hackathon judges, mentors, and evaluators with a 2-minute live walkthrough of **Alita** in action.

---

## 🎯 Demo Scenario: Automated Bug Fix & Regression Test

In this demonstration, Alita:
1. Discovers a repository with a broken function.
2. Formulates a hypothesis and reproduces the bug with a test script.
3. Applies a targeted patch to the source code.
4. Verifies the test passes.
5. Emits the completion signal and exports the trajectory audit file.

---

## 🚀 Running the Automated Demo

We have prepared a self-contained demonstration script:

```bash
python run_demo.py
```

### What happens under the hood:
1. `run_demo.py` spins up a temporary workspace with a buggy calculator module (`calculator.py`).
2. The agent inspects the code, runs the failing test case (`division by zero` crashes the app).
3. The agent edits `calculator.py` with proper exception handling.
4. The agent reruns the test suite and confirms 100% test pass.
5. The full execution trajectory is saved to `demo_trajectory.traj.json`.

---

## 🎮 Running a Live Custom Task

You can also point Alita at any directory on your computer:

```bash
battle-angels --task "Create a python script weather.py that queries wttr.in and displays ASCII weather for Tokyo" --yolo
```

Watch Alita write the code, run it in the terminal, verify the ASCII output, and submit!
