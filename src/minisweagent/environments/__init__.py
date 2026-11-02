"""Environment implementations for Battle Angels Alita."""

import copy
import importlib

from minisweagent import Environment

_ENVIRONMENT_MAPPING = {
    "local": "minisweagent.environments.local.LocalEnvironment",
    "docker": "minisweagent.environments.docker.DockerEnvironment",
}


def get_environment_class(spec: str) -> type[Environment]:
    full_path = _ENVIRONMENT_MAPPING.get(spec, spec)
    try:
        module_name, class_name = full_path.rsplit(".", 1)
        module = importlib.import_module(module_name)
        return getattr(module, class_name)
    except (ValueError, ImportError, AttributeError):
        msg = f"Unknown environment type: {spec} (resolved to {full_path}, available: {list(_ENVIRONMENT_MAPPING.keys())})"
        raise ValueError(msg)


def get_environment(config: dict, *, default_type: str = "local") -> Environment:
    config = copy.deepcopy(config)
    environment_class = config.pop("environment_class", default_type)
    return get_environment_class(environment_class)(**config)


__all__ = ["get_environment_class", "get_environment"]
