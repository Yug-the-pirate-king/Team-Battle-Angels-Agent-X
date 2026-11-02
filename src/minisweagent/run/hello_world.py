"""Team Battle Angels - Alita: Hello World Example.

Simple python script demonstrating how to invoke Alita programmatically.
"""

import logging
import os
from pathlib import Path

import typer
import yaml

from minisweagent import package_dir
from minisweagent.agents.default import DefaultAgent
from minisweagent.environments.local import LocalEnvironment
from minisweagent.models.litellm_model import LitellmModel

app = typer.Typer()


@app.command()
def main(
    task: str = typer.Option(..., "-t", "--task", help="Task/problem statement", show_default=False, prompt=True),
    model_name: str | None = typer.Option(
        None,
        "-m",
        "--model",
        help="Model name (defaults to MSWEA_MODEL_NAME environment variable)",
    ),
) -> DefaultAgent:
    logging.basicConfig(level=logging.INFO)
    resolved_model = model_name or os.getenv("MSWEA_MODEL_NAME", "openai/gpt-4o")
    model = LitellmModel(model_name=resolved_model)
    agent_config = yaml.safe_load(Path(package_dir / "config" / "default.yaml").read_text(encoding="utf-8"))["agent"]
    agent = DefaultAgent(
        model=model,
        env=LocalEnvironment(),
        **agent_config,
    )
    print(f"\n[Team Battle Angels] Running task: {task}\n")
    agent.run(task)
    return agent


if __name__ == "__main__":
    app()
