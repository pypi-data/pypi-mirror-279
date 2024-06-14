from __future__ import annotations

from tach import filesystem as fs


def clean_project(root: str) -> None:
    """
    Remove tach-related configuration from project root.
    """

    project_config_path = fs.get_project_config_path(root)
    if project_config_path:
        fs.delete_file(project_config_path)


__all__ = ["clean_project"]
