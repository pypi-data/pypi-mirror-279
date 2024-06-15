from __future__ import annotations

import ast
import os
import re
import stat
import threading
from collections import defaultdict
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Generator

from tach import errors
from tach.colors import BCOLORS
from tach.constants import ROOT_MODULE_SENTINEL_TAG


@dataclass
class FileInfo:
    path: str
    content: str | None = None
    canonical_path: str | None = None
    ast: ast.AST | None = None


# Thread-local file cache to avoid going to disk as much as possible
thread_local = threading.local()
# Cannot type-hint non-self attributes (https://github.com/python/mypy/issues/2388)
# cwd: str
thread_local.cwd = os.getcwd()
# file_caches_by_cwd: defaultdict[str, dict[str, FileInfo]]
thread_local.file_caches_by_cwd = defaultdict(dict)


def get_cwd() -> str:
    # Use a cached cwd to avoid system calls
    if not hasattr(thread_local, "cwd"):
        thread_local.cwd = os.getcwd()
    return thread_local.cwd


def chdir(path: str):
    # When using chdir, update the cached version
    os.chdir(path)
    thread_local.cwd = os.getcwd()


def _get_file_cache() -> dict[str, FileInfo]:
    if not hasattr(thread_local, "file_caches_by_cwd"):
        thread_local.file_caches_by_cwd = defaultdict(dict)
    file_caches_by_cwd: defaultdict[str, dict[str, FileInfo]] = (
        thread_local.file_caches_by_cwd
    )  # type: ignore
    return file_caches_by_cwd[get_cwd()]


def _file_cache_key(path: str) -> str:
    return f"{get_cwd()}:::{path}"


def _cached_file(path: str) -> FileInfo | None:
    return _get_file_cache().get(_file_cache_key(path))


def _set_cached_file(path: str, file_info: FileInfo):
    _get_file_cache()[_file_cache_key(path)] = file_info


def _remove_cached_file(path: str):
    _get_file_cache().pop(_file_cache_key(path), None)


def canonical(path: str) -> str:
    cached_file = _cached_file(path)
    if cached_file and cached_file.canonical_path:
        return cached_file.canonical_path

    result = os.path.relpath(os.path.realpath(path), start=get_cwd())

    if cached_file:
        cached_file.canonical_path = result
    else:
        _set_cached_file(path, FileInfo(path=path, canonical_path=result))

    return result


def read_file(path: str) -> str:
    cached_file = _cached_file(path)
    if cached_file and cached_file.content:
        return cached_file.content

    with open(path) as f:
        content = f.read()

    if cached_file:
        cached_file.content = content
    else:
        _set_cached_file(path, FileInfo(path=path, content=content))

    return content


def write_file(path: str, content: str):
    with open(path, "w") as f:
        f.write(content)
        print(f"{BCOLORS.WARNING}Wrote '{canonical(path)}'{BCOLORS.ENDC}")

    cached_file = _cached_file(path)
    if cached_file:
        cached_file.content = content
        cached_file.ast = None
    else:
        _set_cached_file(path, FileInfo(path=path, content=content))


def delete_file(path: str):
    _remove_cached_file(path)
    os.unlink(path)
    print(f"{BCOLORS.WARNING}Deleted '{canonical(path)}'{BCOLORS.ENDC}")


def mark_executable(path: str):
    file_path = Path(path)
    file_path.chmod(
        file_path.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH
    )


def parse_ast(path: str) -> ast.AST:
    cached_file = _cached_file(path)
    if cached_file and cached_file.ast:
        return cached_file.ast

    if cached_file and cached_file.content:
        content = cached_file.content
        try:
            ast_result = ast.parse(cached_file.content)
        except SyntaxError as e:
            raise errors.TachParseError(f"Syntax error in {path}: {e}")
    else:
        with open(path) as f:
            content = f.read()
        try:
            ast_result = ast.parse(content)
        except SyntaxError as e:
            raise errors.TachParseError(f"Syntax error in {path}: {e}")

    if cached_file:
        cached_file.content = content
        cached_file.ast = ast_result
    else:
        _set_cached_file(path, FileInfo(path=path, content=content, ast=ast_result))

    return ast_result


def walk(
    root: str,
    depth: int | None = None,
    exclude_paths: list[str] | None = None,
) -> Generator[tuple[str, list[str]], None, None]:
    canonical_root = canonical(root)
    base_depth = 0 if canonical_root == "." else canonical_root.count(os.path.sep) + 1
    for dirpath, dirnames, filenames in os.walk(canonical_root):
        dirpath = canonical(dirpath)
        dirpath_for_matching = f"{dirpath}/"

        # The root dir is a special case which starts with '.' but is not hidden
        if dirpath != "." and os.path.basename(os.path.normpath(dirpath)).startswith(
            "."
        ):
            # This prevents recursing into child directories of hidden paths
            del dirnames[:]
            continue

        if exclude_paths is not None and any(
            re.match(exclude_path, dirpath_for_matching)
            for exclude_path in exclude_paths
        ):
            # Treat excluded paths as invisible
            continue

        if depth:
            # Ignore anything past requested depth
            current_depth = dirpath.count(os.path.sep)
            if current_depth >= base_depth + depth:
                continue

        def filter_filename(filename: str) -> bool:
            if filename.startswith("."):
                return False
            file_path = os.path.join(dirpath, filename)
            if exclude_paths is not None and any(
                re.match(exclude_path, file_path) for exclude_path in exclude_paths
            ):
                return False
            return True

        yield dirpath, list(filter(filter_filename, filenames))


def walk_pyfiles(
    root: str,
    depth: int | None = None,
    exclude_paths: list[str] | None = None,
) -> Generator[str, None, None]:
    for dirpath, filenames in walk(
        root,
        depth=depth,
        exclude_paths=exclude_paths,
    ):
        for filename in filenames:
            if filename.endswith(".py"):
                yield os.path.join(dirpath, filename)


def walk_pypackages(
    root: str,
    depth: int | None = None,
    exclude_paths: list[str] | None = None,
) -> Generator[str, None, None]:
    for filepath in walk_pyfiles(
        root,
        depth=depth,
        exclude_paths=exclude_paths,
    ):
        init_file_ending = f"{os.path.sep}__init__.py"
        if filepath.endswith(init_file_ending):
            yield filepath[: -len(init_file_ending)]


def walk_configured_packages(
    root: str,
    depth: int | None = None,
    exclude_paths: list[str] | None = None,
) -> Generator[tuple[str, str], None, None]:
    for dirpath in walk_pypackages(
        root,
        depth=depth,
        exclude_paths=exclude_paths,
    ):
        package_yml_path = os.path.join(dirpath, "package.yml")
        if os.path.isfile(package_yml_path):
            yield dirpath, package_yml_path


@lru_cache(maxsize=None)
def file_to_module_path(file_path: str) -> str:
    # Assuming that the file_path has been 'canonicalized' and does not traverse multiple directories
    file_path = file_path.lstrip("./")
    if file_path == ".":
        return ""

    module_path = file_path.replace(os.sep, ".")

    if module_path.endswith(".py"):
        module_path = module_path[:-3]
    if module_path.endswith(".__init__"):
        module_path = module_path[:-9]
    if module_path == "__init__":
        return ""

    return module_path


@lru_cache(maxsize=None)
def module_to_file_path_no_members(module_path: str) -> Path | None:
    """
    This resolves a dotted Python module path ('a.b.c')
    into a Python file path or a Python package __init__.py
    """
    if module_path == ROOT_MODULE_SENTINEL_TAG:
        root_path = Path("__init__.py")
        if root_path.exists():
            return root_path
        return None

    base_path = module_path.replace(".", os.sep)
    pyfile_path = Path(f"{base_path}.py")
    init_py_path = Path(base_path).joinpath("__init__.py")
    if pyfile_path.exists():
        return pyfile_path
    elif init_py_path.exists():
        return init_py_path

    return None


@lru_cache(maxsize=None)
def module_to_pyfile_or_dir_path(module_path: str) -> Path | None:
    """
    This resolves a dotted Python module path ('a.b.c')
    into a Python file or a Python package directory
    """
    base_path = module_path.replace(".", os.sep)
    pyfile_path = Path(f"{base_path}.py")
    dir_path = Path(base_path)
    if pyfile_path.exists():
        return pyfile_path
    elif dir_path.is_dir():
        return dir_path

    return None
