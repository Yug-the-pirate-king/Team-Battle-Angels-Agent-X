#!/usr/bin/env python3

"""Run Battle Angels Agent X in your environment.
Autonomous AI software engineering agent developed by Team Battle Angels for Hackathons.
"""

import os
from pathlib import Path
from typing import Any

import typer
from rich.console import Console

from minisweagent import global_config_dir
from minisweagent.agents import get_agent
from minisweagent.agents.utils.prompt_user import _multiline_prompt
from minisweagent.config import builtin_config_dir, get_config_from_spec
from minisweagent.environments import get_environment
from minisweagent.models import get_model
from minisweagent.run.utilities.config import configure_if_first_time
from minisweagent.utils.serialize import UNSET, recursive_merge

DEFAULT_CONFIG_FILE = Path(os.getenv("MSWEA_MINI_CONFIG_PATH", builtin_config_dir / "mini.yaml"))
DEFAULT_OUTPUT_FILE = global_config_dir / "last_run.traj.json"


_HELP_TEXT = """Run mini-SWE-agent in your local environment. Powered by Team Battle Angels - Agent X.

[bold cyan]Team Battle Angels - Agent X[/bold cyan]
An autonomous, lightweight AI software engineering agent built for hackathon challenges.

Examples:
  [bold green]battle-angels --task "Fix the bug in app.py"[/bold green]
  [bold green]battle-angels -m openai/gpt-4o --yolo[/bold green]
  [bold green]battle-angels[/bold green]  (Interactive prompt mode)
"""

_CONFIG_SPEC_HELP_TEXT = """Path to config files, filenames, or key-value pairs (e.g. -c mini.yaml -c model.model_kwargs.temperature=0.2)."""

console = Console(highlight=False)
app = typer.Typer(rich_markup_mode="rich")


# fmt: off
@app.command(help=_HELP_TEXT)
def main(
    model_name: str | None = typer.Option(None, "-m", "--model", help="Model to use (e.g. openai/gpt-4o, claude-3-5-sonnet, gemini/gemini-1.5-pro, ollama/llama3)"),
    model_class: str | None = typer.Option(None, "--model-class", help="Model class to use (e.g., 'litellm')", rich_help_panel="Advanced"),
    agent_class: str | None = typer.Option(None, "--agent-class", help="Agent class to use (e.g., 'interactive' or 'default')", rich_help_panel="Advanced"),
    environment_class: str | None = typer.Option(None, "--environment-class", help="Environment class ('local' or 'docker')", rich_help_panel="Advanced"),
    task: str | None = typer.Option(None, "-t", "--task", help="Task or problem statement for the agent", show_default=False),
    yolo: bool = typer.Option(False, "-y", "--yolo", help="Autonomous mode: run without manual confirmation at every step"),
    cost_limit: float | None = typer.Option(None, "-l", "--cost-limit", help="Cost limit in USD. Set to 0 to disable."),
    config_spec: list[str] = typer.Option([str(DEFAULT_CONFIG_FILE)], "-c", "--config", help=_CONFIG_SPEC_HELP_TEXT),
    output: Path | None = typer.Option(DEFAULT_OUTPUT_FILE, "-o", "--output", help="Output trajectory file (.traj.json)"),
    exit_immediately: bool = typer.Option(False, "--exit-immediately", help="Exit immediately when the agent completes rather than confirming.", rich_help_panel="Advanced"),
) -> Any:
    # fmt: on
    configure_if_first_time()

    # Build the config from the command line arguments
    console.print(f"[bold cyan][Team Battle Angels][/bold cyan] Initializing agent config from: [bold green]{config_spec}[/bold green]")
    configs = [get_config_from_spec(spec) for spec in config_spec]
    configs.append({
        "run": {
            "task": task or UNSET,
        },
        "agent": {
            "agent_class": agent_class or UNSET,
            "mode": "yolo" if yolo else UNSET,
            "cost_limit": cost_limit if cost_limit is not None else UNSET,
            "confirm_exit": False if exit_immediately else UNSET,
            "output_path": output or UNSET,
        },
        "model": {
            "model_class": model_class or UNSET,
            "model_name": model_name or UNSET,
        },
        "environment": {
            "environment_class": environment_class or UNSET,
        },
    })
    config = recursive_merge(*configs)

    if (run_task := config.get("run", {}).get("task", UNSET)) is UNSET:
        console.print("[bold yellow]What coding challenge or task would you like Agent X to solve?[/bold yellow]")
        run_task = _multiline_prompt()
        console.print("[bold green]Task received! Starting agent loop...[/bold green]")

    model = get_model(config=config.get("model", {}))
    env = get_environment(config.get("environment", {}), default_type="local")
    agent = get_agent(model, env, config.get("agent", {}), default_type="interactive")
    agent.run(run_task)
    if (output_path := config.get("agent", {}).get("output_path")):
        console.print(f"[bold green]Saved trajectory to '{output_path}'[/bold green]")
    return agent


if __name__ == "__main__":
    app()
