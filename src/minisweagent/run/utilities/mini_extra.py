#!/usr/bin/env python3

"""This is the central entry point for Battle Angels Agent X utility commands.
Use subcommands to configure API keys, inspect trajectories, etc.
"""

import sys
from importlib import import_module

from rich.console import Console

subcommands = [
    ("minisweagent.run.utilities.config", ["config"], "Manage the global config / API keys"),
    ("minisweagent.run.utilities.inspector", ["inspect", "i", "inspector"], "Run trajectory inspector (browse steps)"),
]


def get_docstring() -> str:
    lines = [
        "[bold cyan]Team Battle Angels - Agent X Utilities[/bold cyan]",
        "",
        "Available sub-commands:",
        "",
    ]
    for _, aliases, description in subcommands:
        alias_text = " or ".join(f"[bold green]{alias}[/bold green]" for alias in aliases)
        lines.append(f"  {alias_text}: {description}")
    return "\n".join(lines)


def main():
    args = sys.argv[1:]

    if len(args) == 0 or len(args) == 1 and args[0] in ["-h", "--help"]:
        return Console().print(get_docstring())

    for module_path, aliases, _ in subcommands:
        if args[0] in aliases:
            return import_module(module_path).app(args[1:], prog_name=f"mini-extra {aliases[0]}")

    return Console().print(get_docstring())


if __name__ == "__main__":
    main()
