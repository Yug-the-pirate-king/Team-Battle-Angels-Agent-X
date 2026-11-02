import os
import platform
import re
import signal
import subprocess
import sys
from typing import Any

from pydantic import BaseModel

from minisweagent.exceptions import Submitted
from minisweagent.utils.serialize import recursive_merge


class LocalEnvironmentConfig(BaseModel):
    cwd: str = ""
    env: dict[str, str] = {}
    timeout: int = 30


class LocalEnvironment:
    def __init__(self, *, config_class: type = LocalEnvironmentConfig, **kwargs):
        """This class executes bash/shell commands directly on the local machine."""
        self.config = config_class(**kwargs)

    def execute(self, action: dict, cwd: str = "", *, timeout: int | None = None) -> dict[str, Any]:
        """Execute a command in the local environment and return the result as a dict."""
        command = action.get("command", "")
        cwd = cwd or self.config.cwd or os.getcwd()
        full_env = os.environ | self.config.env
        try:
            result = _run(command, cwd, full_env, timeout or self.config.timeout)
            output = {"output": result.stdout, "returncode": result.returncode, "exception_info": ""}
        except Exception as e:
            raw_output = getattr(e, "output", None)
            raw_output = (
                raw_output.decode("utf-8", errors="replace") if isinstance(raw_output, bytes) else (raw_output or "")
            )
            output = {
                "output": raw_output,
                "returncode": -1,
                "exception_info": f"An error occurred while executing the command: {e}",
                "extra": {"exception_type": type(e).__name__, "exception": str(e)},
            }
        self._check_finished(output)
        return output

    def _check_finished(self, output: dict):
        """Raises Submitted if the output indicates task completion."""
        lines = output.get("output", "").lstrip().splitlines(keepends=True)
        if not lines or output.get("returncode", -1) != 0:
            return
        for i, line in enumerate(lines):
            if line.strip().strip("'\"") == "COMPLETE_TASK_AND_SUBMIT_FINAL_OUTPUT":
                submission = "".join(lines[i + 1:])
                raise Submitted(
                    {
                        "role": "exit",
                        "content": submission,
                        "extra": {"exit_status": "Submitted", "submission": submission},
                    }
                )

    def get_template_vars(self, **kwargs) -> dict[str, Any]:
        return recursive_merge(self.config.model_dump(), platform.uname()._asdict(), os.environ, kwargs)

    def serialize(self) -> dict:
        return {
            "info": {
                "config": {
                    "environment": self.config.model_dump(mode="json"),
                    "environment_type": f"{self.__class__.__module__}.{self.__class__.__name__}",
                }
            }
        }


def _normalize_windows_line(line: str, env: dict[str, str]) -> str:
    sline = line.strip()
    if not sline:
        return ""

    # Expand $VAR and ${VAR}
    def _repl(m):
        var_name = m.group(1) or m.group(2)
        return env.get(var_name, os.environ.get(var_name, ""))

    sline = re.sub(r"\$\{([A-Za-z0-9_]+)\}|\$([A-Za-z0-9_]+)", _repl, sline)

    if sline == "pwd":
        return "cd"
    if sline.startswith("sleep ") or sline == "sleep":
        parts = sline.split()
        secs = parts[1] if len(parts) > 1 else "1"
        return f'"{sys.executable}" -c "import time; time.sleep({secs})"'
    if sline.startswith("echo -e "):
        arg = sline[8:].strip().strip("'\"")
        return f'"{sys.executable}" -c "print(bytes(\'{arg}\', \'utf-8\').decode(\'unicode_escape\'))"'
    if " | grep " in sline:
        parts = sline.split(" | grep ")
        left = parts[0].strip()
        pat = parts[1].strip().strip("'\"")
        sline = f'{left} | findstr /C:"{pat}"'
    # Strip quotes from echo '...' or echo '...' > file
    sline = re.sub(r"^echo\s+'([^']*)'", r"echo \1", sline)
    sline = re.sub(r'^echo\s+"([^"]*)"', r"echo \1", sline)
    if sline.startswith("touch "):
        file_to_touch = sline[6:].strip()
        return f"type nul > {file_to_touch}"
    elif sline.startswith("cat "):
        return "type " + sline[4:]
    return sline


def _normalize_windows_command(cmd: str, env: dict[str, str]) -> str:
    """Normalize POSIX idioms (like sleep, bash math, $VAR, echo 'hello', ; and newlines) for Windows cmd.exe."""
    def _eval_math(m):
        try:
            return str(eval(m.group(1)))
        except Exception:
            return m.group(0)

    cmd = re.sub(r"\$\(\(([0-9\s*+/-]+)\)\)", _eval_math, cmd)

    raw_lines = cmd.splitlines()
    sub_cmds = []
    for line in raw_lines:
        for part in line.split(";"):
            part_str = part.strip()
            if part_str:
                sub_cmds.append(part_str)

    if not sub_cmds:
        return cmd
    norm_lines = [_normalize_windows_line(c, env) for c in sub_cmds if c]
    return " & ".join(norm_lines) if norm_lines else cmd


def _run(command: str, cwd: str, env: dict[str, str], timeout: int) -> subprocess.CompletedProcess[str]:
    """Like subprocess.run, but handles process termination on timeout."""
    exec_command = _normalize_windows_command(command, env) if os.name != "posix" else command
    process = subprocess.Popen(
        exec_command,
        shell=True,
        text=True,
        cwd=cwd,
        env=env,
        encoding="utf-8",
        errors="replace",
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        start_new_session=os.name == "posix",
    )
    try:
        stdout, _ = process.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
        os.killpg(process.pid, signal.SIGKILL) if os.name == "posix" else process.kill()
        stdout, _ = process.communicate()
        raise subprocess.TimeoutExpired(command, timeout, output=stdout)
    return subprocess.CompletedProcess(command, process.returncode, stdout=stdout)
