from __future__ import annotations

import yaml

from tach import filesystem as fs
from tach.core import ProjectConfig


def dump_project_config_to_yaml(config: ProjectConfig) -> str:
    # Using sort_keys=False here and depending on config.model_dump maintaining 'insertion order'
    # so that 'tag' appears before 'depends_on'
    # Instead, should provide custom yaml.Dumper & yaml.Representer or just write our own
    # Sort only constraints and dependencies alphabetically for now
    config.modules.sort(key=lambda mod: mod.path)
    for mod in config.modules:
        mod.depends_on.sort()
    config.exclude = list(set(config.exclude)) if config.exclude else []
    config.exclude.sort()
    return yaml.dump(config.model_dump(), sort_keys=False)


def parse_project_config(root: str = ".") -> ProjectConfig | None:
    file_path = fs.get_project_config_path(root)
    if not file_path:
        return None

    with open(file_path) as f:
        result = yaml.safe_load(f)
        if not result or not isinstance(result, dict):
            raise ValueError(f"Empty or invalid project config file: {file_path}")
    config = ProjectConfig(**result)  # type: ignore
    return config
