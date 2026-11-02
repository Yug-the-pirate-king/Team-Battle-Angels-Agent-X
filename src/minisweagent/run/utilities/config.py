#!/usr/bin/env python3

"""Utility to manage the global config file for Battle Angels Alita.

You can also directly edit the `.env` file in the config directory.

It is located at [bold green]{global_config_file}[/bold green].
"""

import os
import subprocess

from dotenv import load_dotenv, set_key, unset_key
from rich.console import Console
from rich.rule import Rule
from typer import Argument, Typer

from minisweagent import global_config_file


def _reload_config():
    load_dotenv(dotenv_path=global_config_file, override=True)


app = Typer(
    help=__doc__.format(global_config_file=global_config_file),  # type: ignore
    no_args_is_help=True,
    rich_markup_mode="rich",
    add_completion=False,
)
console = Console(highlight=False)


_SETUP_HELP = """[bold cyan]Team Battle Angels - Alita Configuration[/bold cyan]

To get started, set up your model selection and API keys.
You can also set environment variables directly or create a .env file.

Popular supported models & environment variables:
  - [bold green]openai/gpt-4o[/bold green] ([bold green]OPENAI_API_KEY[/bold green])
  - [bold green]anthropic/claude-3-5-sonnet-20241022[/bold green] ([bold green]ANTHROPIC_API_KEY[/bold green])
  - [bold green]gemini/gemini-1.5-pro[/bold green] ([bold green]GEMINI_API_KEY[/bold green])
  - [bold green]openrouter/auto[/bold green] ([bold green]OPENROUTER_API_KEY[/bold green])
  - [bold green]ollama/llama3[/bold green] (Local models - no API key required)

[bold]Note: Please always include the provider prefix (e.g. "openai/", "anthropic/", "gemini/").[/bold]

[bold yellow]You can leave any setting blank to skip it.[/bold yellow]
"""


def prompt(*args, **kwargs):
    from prompt_toolkit.shortcuts.prompt import prompt as _prompt

    return _prompt(*args, **kwargs)


def configure_if_first_time():
    if not os.getenv("MSWEA_CONFIGURED"):
        console.print(Rule(characters="="))
        setup()
        console.print(Rule(characters="="))


@app.command()
def setup():
    """Setup the global config file."""
    console.print(_SETUP_HELP.format(global_config_file=global_config_file))
    default_model = prompt(
        "Enter your default model (e.g., openai/gpt-4o): ",
        default=os.getenv("MSWEA_MODEL_NAME", "openai/gpt-4o"),
    ).strip()
    if default_model:
        set_key(global_config_file, "MSWEA_MODEL_NAME", default_model)
    console.print(
        "[bold yellow]If you already have your API keys set as environment variables, you can ignore the next question.[/bold yellow]"
    )
    key_name = prompt("Enter your API key name (e.g., OPENAI_API_KEY): ").strip()
    key_value = None
    if key_name:
        key_value = prompt("Enter your API key value (e.g., sk-...): ", default=os.getenv(key_name, "")).strip()
        if key_value:
            set_key(global_config_file, key_name, key_value)
    if not key_value:
        console.print(
            "[bold red]API key setup not completed.[/bold red] Totally fine if you have your keys as environment variables."
        )
    set_key(global_config_file, "MSWEA_CONFIGURED", "true")
    _reload_config()
    console.print(
        "\n[bold yellow]Config finished.[/bold yellow] Run [bold green]battle-angels --help[/bold green] to get started."
    )


@app.command()
def set(
    key: str | None = Argument(None, help="The key to set"),
    value: str | None = Argument(None, help="The value to set"),
):
    """Set a key in the global config file."""
    if key is None:
        key = prompt("Enter the key to set: ")
    if value is None:
        value = prompt(f"Enter the value for {key}: ")
    set_key(global_config_file, key, value)
    _reload_config()


@app.command()
def unset(key: str | None = Argument(None, help="The key to unset")):
    """Unset a key in the global config file."""
    if key is None:
        key = prompt("Enter the key to unset: ")
    unset_key(global_config_file, key)
    _reload_config()


@app.command()
def edit():
    """Edit the global config file."""
    editor = os.getenv("EDITOR", "nano")
    subprocess.run([editor, global_config_file])
    _reload_config()


if __name__ == "__main__":
    app()
