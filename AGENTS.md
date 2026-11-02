# Team Battle Angels - Alita Overview & Guidelines

- **Alita** is an autonomous AI software engineering agent developed by **Team Battle Angels** for hackathon challenges.
- Designed to diagnose, reproduce, edit, and fix software bugs and feature requests.
- Embraces radical simplicity, minimal dependencies, and transparent execution.

## Project Structure

```text
minisweagent/__init__      # Core protocols & startup banner
minisweagent/agents        # Agent loops (DefaultAgent & InteractiveAgent)
minisweagent/environments  # Stateless subshell execution (Local & Docker)
minisweagent/models        # Multi-LLM provider interfaces
minisweagent/run           # CLI commands (battle-angels, alita, mini)
```

## Hackathon Development Principles

1. **Target Python 3.10+** with clean type annotations.
2. **Minimal & Readable**: Write concise, maintainable code without bloated layers.
3. **No Secrets**: Never commit `.env` or credentials. Always use `.env.example`.
4. **Cross-Platform Resilience**: Ensure commands work smoothly on Windows, Linux, and macOS.
5. **Deterministic Testing**: Verify core workflows with unit tests.

