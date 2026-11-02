import os
import sys
from prompt_toolkit.formatted_text.html import HTML
from prompt_toolkit.history import FileHistory
from prompt_toolkit.output import DummyOutput
from prompt_toolkit.shortcuts import PromptSession

from minisweagent import global_config_dir

_history = FileHistory(global_config_dir / "interactive_history.txt")


def _create_session(multiline: bool = False) -> PromptSession:
    """Create a prompt session with graceful fallback for headless/redirected console environments."""
    try:
        return PromptSession(history=_history, multiline=multiline)
    except Exception:
        return PromptSession(history=_history, multiline=multiline, output=DummyOutput())


class _LazyPromptSession:
    """Lazy initialization of PromptSession so importing does not fail when no screen buffer exists."""

    def __init__(self, multiline: bool = False):
        self._multiline = multiline
        self._session = None

    def _get_inner(self) -> PromptSession:
        if self._session is None:
            self._session = _create_session(self._multiline)
        return self._session

    def prompt(self, *args, **kwargs):
        try:
            return self._get_inner().prompt(*args, **kwargs)
        except Exception:
            # Fallback for headless environments or when console is redirected
            prompt_str = args[0] if args else ""
            if prompt_str:
                print(prompt_str, end="", flush=True)
            return input()

    def __getattr__(self, name):
        return getattr(self._get_inner(), name)


prompt_session = _LazyPromptSession(multiline=False)
_multiline_prompt_session = _LazyPromptSession(multiline=True)


def _multiline_prompt() -> str:
    try:
        return _multiline_prompt_session.prompt(
            "",
            bottom_toolbar=HTML(
                "Submit message: <b fg='yellow' bg='black'>Esc, then Enter</b> | "
                "Navigate history: <b fg='yellow' bg='black'>Arrow Up/Down</b> | "
                "Search history: <b fg='yellow' bg='black'>Ctrl+R</b>"
            ),
        )
    except Exception:
        print("(Enter your task below. Type 'END' on a new line or EOF to submit):")
        lines = []
        while True:
            try:
                line = input()
                if line.strip() == "END":
                    break
                lines.append(line)
            except (EOFError, KeyboardInterrupt):
                break
        return "\n".join(lines)


__all__ = ["prompt_session", "_multiline_prompt_session", "_multiline_prompt"]
