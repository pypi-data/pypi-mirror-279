from __future__ import annotations

import os
from typing import TYPE_CHECKING

from tach import errors
from tach.extension import create_dependency_report, set_excluded_paths

if TYPE_CHECKING:
    from tach.core import ProjectConfig


def report(
    root: str,
    path: str,
    project_config: ProjectConfig,
    exclude_paths: list[str] | None = None,
) -> str:
    if not os.path.isdir(root):
        raise errors.TachSetupError(f"The path '{root}' is not a valid directory.")

    if not os.path.exists(path):
        raise errors.TachError(f"The path '{path}' does not exist.")

    if exclude_paths is not None and project_config.exclude is not None:
        exclude_paths.extend(project_config.exclude)
    else:
        exclude_paths = project_config.exclude

    # This informs the Rust extension ahead-of-time which paths are excluded.
    set_excluded_paths(exclude_paths=exclude_paths or [])

    return create_dependency_report(root, path)


__all__ = ["report"]
