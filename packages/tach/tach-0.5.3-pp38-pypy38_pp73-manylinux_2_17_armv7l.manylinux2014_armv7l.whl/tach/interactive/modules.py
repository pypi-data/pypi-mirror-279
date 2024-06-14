from __future__ import annotations

import os
import re
from collections import deque
from dataclasses import dataclass, field
from enum import Enum
from itertools import chain
from typing import TYPE_CHECKING, Callable, Generator

from prompt_toolkit import ANSI
from prompt_toolkit.application import Application
from prompt_toolkit.data_structures import Point
from prompt_toolkit.key_binding import KeyBindings, KeyPressEvent
from prompt_toolkit.layout import (
    Container,
    HSplit,
    Layout,
    ScrollablePane,
    VerticalAlign,
    Window,
)
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.styles import Style
from prompt_toolkit.widgets import Frame
from rich.console import Console
from rich.text import Text
from rich.tree import Tree

from tach import errors
from tach import filesystem as fs

if TYPE_CHECKING:
    from prompt_toolkit.formatted_text import AnyFormattedText

    from tach.core import ProjectConfig


@dataclass
class FileNode:
    full_path: str
    is_dir: bool
    expanded: bool = False
    is_module: bool = False
    parent: FileNode | None = None
    children: list[FileNode] = field(default_factory=list)

    @property
    def empty(self) -> bool:
        return len(self.children) == 0

    @property
    def visible_children(self) -> list[FileNode]:
        if not self.expanded:
            return []
        return self.children

    @classmethod
    def build_from_path(cls, path: str) -> FileNode:
        is_dir = os.path.isdir(path)
        return cls(full_path=path, is_dir=is_dir)

    @property
    def parent_sorted_children(self) -> list[FileNode] | None:
        if not self.parent:
            return None
        return sorted(self.parent.visible_children, key=lambda node: node.full_path)

    @property
    def prev_sibling(self) -> FileNode | None:
        parent_sorted_children = self.parent_sorted_children
        if not parent_sorted_children:
            return None

        try:
            my_index = parent_sorted_children.index(self)
        except ValueError:
            raise errors.TachError("Error occurred in interactive file tree navigation")

        if my_index == 0:
            return None
        return parent_sorted_children[my_index - 1]

    @property
    def next_sibling(self) -> FileNode | None:
        parent_sorted_children = self.parent_sorted_children
        if not parent_sorted_children:
            return None

        try:
            my_index = parent_sorted_children.index(self)
        except ValueError:
            raise errors.TachError("Error occurred in interactive file tree navigation")

        if my_index == len(parent_sorted_children) - 1:
            return None
        return parent_sorted_children[my_index + 1]

    def siblings(self, include_self: bool = True) -> list[FileNode]:
        if not self.parent:
            return [self] if include_self else []

        return (
            self.parent.children
            if include_self
            else [node for node in self.parent.children if node is not self]
        )


@dataclass
class FileTree:
    root: FileNode
    nodes: dict[str, FileNode] = field(default_factory=dict)

    @classmethod
    def build_from_path(
        cls,
        path: str,
        depth: int | None = 1,
        exclude_paths: list[str] | None = None,
    ) -> FileTree:
        root = FileNode.build_from_path(fs.canonical(path))
        root.expanded = True
        tree = cls(root)
        tree.nodes[fs.canonical(path)] = root
        tree._build_subtree(
            root, depth=depth if depth is not None else 1, exclude_paths=exclude_paths
        )
        return tree

    def _build_subtree(
        self,
        root: FileNode,
        depth: int = 1,
        exclude_paths: list[str] | None = None,
    ):
        if root.is_dir:
            try:
                for entry in os.listdir(root.full_path):
                    if entry.startswith("."):
                        # Ignore hidden files and directories
                        continue
                    entry_path = os.path.join(root.full_path, entry)
                    if os.path.isfile(entry_path) and not entry_path.endswith(".py"):
                        # Only interested in Python files
                        continue

                    if os.path.basename(entry_path) == "__init__.py":
                        # __init__.py does not have a unique module path from its containing package
                        # so users should not be able to mark it as a standalone module
                        continue

                    # Adding a trailing slash lets us match 'tests/' as an exclude pattern
                    entry_path_for_matching = f"{fs.canonical(entry_path)}/"
                    if exclude_paths is not None and any(
                        re.match(exclude_path, entry_path_for_matching)
                        for exclude_path in exclude_paths
                    ):
                        # This path is ignored
                        continue
                    child_node = FileNode.build_from_path(entry_path)
                    if depth > 1:
                        child_node.expanded = True
                    child_node.parent = root
                    root.children.append(child_node)
                    self.nodes[fs.canonical(entry_path)] = child_node
                    if child_node.is_dir:
                        self._build_subtree(
                            child_node,
                            depth=max(depth - 1, 0),
                            exclude_paths=exclude_paths,
                        )
            except PermissionError:
                # This is expected to occur during listdir when the directory cannot be accessed
                # We simply bail if that happens, meaning it won't show up in the interactive viewer
                return

    def set_modules(self, module_paths: list[str]):
        for module_path in module_paths:
            if module_path in self.nodes:
                self.nodes[module_path].is_module = True

    def __iter__(self):
        return file_tree_iterator(self)

    def visible(self):
        return file_tree_iterator(self, visible_only=True)


def file_tree_iterator(
    tree: FileTree, visible_only: bool = False
) -> Generator[FileNode, None, None]:
    # DFS traversal for printing
    stack = deque([tree.root])

    while stack:
        node = stack.popleft()
        yield node
        if visible_only:
            stack.extendleft(
                sorted(node.visible_children, key=lambda n: n.full_path, reverse=True)
            )
        else:
            stack.extendleft(
                sorted(node.children, key=lambda n: n.full_path, reverse=True)
            )


class ExitCode(Enum):
    QUIT_NOSAVE = 1
    QUIT_SAVE = 2


class InteractiveModuleTree:
    TREE_LABEL = "Confirm Your Modules"
    AUTO_EXCLUDE_PATHS = [".*__pycache__"]

    def __init__(
        self,
        path: str,
        project_config: ProjectConfig,
        depth: int | None = 1,
    ):
        # By default, don't save if we exit for any reason
        self.exit_code: ExitCode = ExitCode.QUIT_NOSAVE
        self.exclude_paths = project_config.exclude
        if self.exclude_paths is None:
            self.exclude_paths = self.AUTO_EXCLUDE_PATHS
        else:
            self.exclude_paths.extend(self.AUTO_EXCLUDE_PATHS)
        self.file_tree = FileTree.build_from_path(
            path=path,
            depth=depth,
            exclude_paths=self.exclude_paths,
        )
        module_file_paths = list(
            map(
                str,
                filter(
                    None,
                    [
                        fs.module_to_pyfile_or_dir_path(module_path)
                        for module_path in project_config.module_paths
                    ],
                ),
            )
        )
        self.file_tree.set_modules(module_paths=module_file_paths)
        self.selected_node = self.file_tree.root
        # x location doesn't matter, only need to track hidden cursor for auto-scroll behavior
        # y location starts at 1 because the FileTree is rendered with a labeled header above the first branch
        self.cursor_point = Point(x=0, y=1)
        self.console = Console()
        self.tree_control = FormattedTextControl(
            text=ANSI(self._render_tree()),
            focusable=True,
            show_cursor=False,
            get_cursor_position=self.get_cursor_position_fn(),
        )
        self.footer_control = self._build_footer()
        self.layout = Layout(
            HSplit(
                [
                    Frame(ScrollablePane(Window(self.tree_control))),
                    self.footer_control,
                ]
            )
        )
        self.key_bindings = KeyBindings()
        self._register_keybindings()
        self.styles = self._build_styles()
        self.app: Application[None] = Application(
            layout=self.layout,
            key_bindings=self.key_bindings,
            full_screen=True,
            style=self.styles,
        )

    def get_cursor_position_fn(self) -> Callable[[], Point]:
        def get_cursor_position() -> Point:
            return self.cursor_point

        return get_cursor_position

    def move_cursor_up(self):
        self.cursor_point = Point(x=self.cursor_point.x, y=self.cursor_point.y - 1)

    def move_cursor_down(self):
        self.cursor_point = Point(x=self.cursor_point.x, y=self.cursor_point.y + 1)

    @staticmethod
    def _build_styles() -> Style:
        return Style.from_dict(
            {
                "footer-key": "bold cyan",
            }
        )

    KEY_BINDING_LEGEND_TOP: list[tuple[str, str]] = [
        ("Up/Down", "Navigate"),
        ("Enter", "Mark/unmark module"),
        ("Right", "Expand"),
        ("Left", "Collapse"),
        ("Ctrl + Up", "Jump to parent"),
    ]
    KEY_BINDING_LEGEND_BOTTOM: list[tuple[str, str]] = [
        ("Ctrl + s", "Exit and save"),
        ("Ctrl + c", "Exit without saving"),
        ("Ctrl + a", "Mark/unmark all"),
    ]

    @staticmethod
    def _key_binding_text(binding: str, description: str) -> list[tuple[str, str]]:
        return [("class:footer-key", binding), ("", f": {description}  ")]

    @classmethod
    def _build_footer(cls) -> Container:
        def _build_footer_text(
            bindings: list[tuple[str, str]],
        ) -> AnyFormattedText:
            return list(
                chain(
                    *(
                        cls._key_binding_text(binding[0], binding[1])
                        for binding in bindings
                    )
                )
            )

        footer_text_top: AnyFormattedText = _build_footer_text(
            cls.KEY_BINDING_LEGEND_TOP
        )
        footer_text_bottom: AnyFormattedText = _build_footer_text(
            cls.KEY_BINDING_LEGEND_BOTTOM
        )
        return HSplit(
            [
                Window(
                    FormattedTextControl(text=footer_text_top), dont_extend_height=True
                ),
                Window(
                    FormattedTextControl(text=footer_text_bottom),
                    dont_extend_height=True,
                ),
            ],
            align=VerticalAlign.CENTER,
        )

    def _register_keybindings(self):
        if self.key_bindings.bindings:
            return

        @self.key_bindings.add("c-c")
        def _(event: KeyPressEvent):
            self.exit_code = ExitCode.QUIT_NOSAVE
            self.app.exit()

        @self.key_bindings.add("c-s")
        def _(event: KeyPressEvent):
            self.exit_code = ExitCode.QUIT_SAVE
            self.app.exit()

        @self.key_bindings.add("up")
        def _(event: KeyPressEvent):
            prev_sibling = self.selected_node.prev_sibling
            # If previous sibling exists, want to bubble down to last child of this sibling
            if prev_sibling:
                curr_node = prev_sibling
                while curr_node.visible_children:
                    curr_node = sorted(
                        curr_node.visible_children, key=lambda node: node.full_path
                    )[-1]
                self.selected_node = curr_node
                self.move_cursor_up()
                self._update_display()
            # If no previous sibling, go to parent
            elif self.selected_node.parent:
                self.selected_node = self.selected_node.parent
                self.move_cursor_up()
                self._update_display()

        @self.key_bindings.add("down")
        def _(event: KeyPressEvent):
            # If we have children, should go to first child alphabetically
            if self.selected_node.visible_children:
                self.selected_node = sorted(
                    self.selected_node.visible_children, key=lambda node: node.full_path
                )[0]
                self.move_cursor_down()
                self._update_display()
                return
            # If we have no children and no parent, nothing to do
            elif not self.selected_node.parent:
                return

            # Here we need to bubble up to find the next node
            curr_node = self.selected_node
            next_sibling = self.selected_node.next_sibling
            while next_sibling is None:
                if not curr_node.parent:
                    break
                curr_node = curr_node.parent
                next_sibling = curr_node.next_sibling

            if not next_sibling:
                # We are the last child all the way up to root
                return

            self.selected_node = next_sibling
            self.move_cursor_down()
            self._update_display()

        @self.key_bindings.add("right")
        def _(event: KeyPressEvent):
            self.selected_node.expanded = True
            self._update_display()

        @self.key_bindings.add("left")
        def _(event: KeyPressEvent):
            self.selected_node.expanded = False
            self._update_display()

        @self.key_bindings.add("enter")
        def _(event: KeyPressEvent):
            self.selected_node.is_module = not self.selected_node.is_module
            self._update_display()

        @self.key_bindings.add("c-a")
        def _(event: KeyPressEvent):
            if not self.selected_node.parent:
                # This means we are the root node without siblings
                # We should simply toggle ourselves
                self.selected_node.is_module = not self.selected_node.is_module
                self._update_display()
                return

            # If all siblings are currently modules, we should un-set all of them (target value is False)
            # Otherwise, we want to ensure all of them are set as modules (target value is True)
            all_siblings_are_modules = all(
                node.is_module for node in self.selected_node.siblings()
            )
            for node in self.selected_node.siblings():
                node.is_module = not all_siblings_are_modules

            self._update_display()

        @self.key_bindings.add("c-up")
        def _(event: KeyPressEvent):
            if not self.selected_node.parent:
                return

            # Simple way to keep cursor position accurate while jumping to parent
            while self.selected_node.prev_sibling:
                self.move_cursor_up()
                self.selected_node = self.selected_node.prev_sibling
            self.move_cursor_up()
            self.selected_node = self.selected_node.parent
            self._update_display()

    def _render_node(self, node: FileNode) -> Text:
        text_parts: list[tuple[str, str] | str] = []
        if node == self.selected_node:
            text_parts.append(("-> ", "bold cyan"))

        basename = os.path.basename(node.full_path)
        if node.is_module:
            text_parts.append((f"[Module] {basename}", "bold yellow"))
        elif node == self.selected_node:
            text_parts.append((basename, "bold"))
        else:
            text_parts.append(basename)

        if not node.empty and node.expanded:
            text_parts.append((" ∨", "cyan"))
        elif not node.empty:
            text_parts.append((" >", "cyan"))
        return Text.assemble(*text_parts)

    def _render_tree(self):
        tree_root = Tree(self.TREE_LABEL)
        # Mapping FileNode paths to rich.Tree branches
        # so that we can iterate over the FileTree and use the
        # parent pointers to find the parent rich.Tree branches
        tree_mapping: dict[str, Tree] = {}

        for node in self.file_tree.visible():
            if node.parent is None:
                # If no parent on FileNode, add to rich.Tree root
                tree_node = tree_root.add(self._render_node(node))
            else:
                if node.parent.full_path not in tree_mapping:
                    raise errors.TachError("Failed to render module tree.")
                # Find parent rich.Tree branch,
                # attach this FileNode to the parent's branch
                parent_tree_node = tree_mapping[node.parent.full_path]
                tree_node = parent_tree_node.add(self._render_node(node))

            # Add this new FileNode to the mapping
            tree_mapping[node.full_path] = tree_node

        with self.console.capture() as capture:
            self.console.print(tree_root)
        return capture.get()

    def _update_display(self):
        self.tree_control.text = ANSI(self._render_tree())

    def run(self) -> list[str] | None:
        self.app.run()
        if self.exit_code == ExitCode.QUIT_SAVE:
            return [node.full_path for node in self.file_tree if node.is_module]


def get_selected_modules_interactive(
    path: str,
    project_config: ProjectConfig,
    depth: int | None = 1,
) -> list[str] | None:
    ipt = InteractiveModuleTree(
        path=path,
        project_config=project_config,
        depth=depth,
    )
    return ipt.run()
