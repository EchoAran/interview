from __future__ import annotations

import ast
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, List, Optional


IGNORED_DIRS = {
    ".git",
    ".idea",
    ".venv",
    "__pycache__",
    "node_modules",
    "venv",
    "env",
    "Result",
    "AST_Result",
    ".spl_cache",
}


@dataclass
class FunctionInfo:
    module_path: str
    module_abspath: str
    function_name: str
    qualified_name: str
    class_name: Optional[str]
    code: str
    lineno: int
    end_lineno: int
    signature: str
    docstring: str
    annotations: dict[str, Any] = field(default_factory=dict)
    return_annotation: Optional[str] = None
    call_names: List[str] = field(default_factory=list)


class PythonProjectScanner:
    def discover_python_files(self, project_root: str | Path) -> List[Path]:
        root = Path(project_root)
        files: List[Path] = []
        for path in root.rglob("*.py"):
            try:
                relative_parts = path.resolve().relative_to(root.resolve()).parts
            except ValueError:
                relative_parts = path.parts
            if any(part in IGNORED_DIRS for part in relative_parts[:-1]):
                continue
            files.append(path)
        return sorted(files)

    def scan_project(self, project_root: str | Path) -> List[FunctionInfo]:
        root = Path(project_root).resolve()
        infos: List[FunctionInfo] = []
        for file_path in self.discover_python_files(root):
            infos.extend(self.scan_file(root, file_path))
        return infos

    def scan_file(self, project_root: Path, file_path: Path) -> List[FunctionInfo]:
        content = file_path.read_text(encoding="utf-8")
        tree = ast.parse(content)
        rel_path = file_path.resolve().relative_to(project_root).as_posix()
        visitor = _FunctionVisitor(
            content=content,
            module_path=rel_path,
            module_abspath=str(file_path.resolve()),
        )
        visitor.visit(tree)
        return visitor.functions


class _FunctionVisitor(ast.NodeVisitor):
    def __init__(self, content: str, module_path: str, module_abspath: str) -> None:
        self.content = content
        self.module_path = module_path
        self.module_abspath = module_abspath
        self.class_stack: List[str] = []
        self.functions: List[FunctionInfo] = []

    def visit_ClassDef(self, node: ast.ClassDef) -> Any:
        self.class_stack.append(node.name)
        self.generic_visit(node)
        self.class_stack.pop()

    def visit_FunctionDef(self, node: ast.FunctionDef) -> Any:
        self._record_function(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> Any:
        self._record_function(node)

    def _record_function(self, node: ast.FunctionDef | ast.AsyncFunctionDef) -> None:
        class_name = self.class_stack[-1] if self.class_stack else None
        qualified_name = f"{class_name}.{node.name}" if class_name else node.name
        code = ast.get_source_segment(self.content, node) or ""
        signature = self._build_signature(node)
        annotations = {arg.arg: self._annotation_to_text(arg.annotation) for arg in node.args.args}
        return_annotation = self._annotation_to_text(node.returns)
        call_names = self._extract_call_names(node)

        self.functions.append(
            FunctionInfo(
                module_path=self.module_path,
                module_abspath=self.module_abspath,
                function_name=node.name,
                qualified_name=qualified_name,
                class_name=class_name,
                code=code,
                lineno=getattr(node, "lineno", 0),
                end_lineno=getattr(node, "end_lineno", getattr(node, "lineno", 0)),
                signature=signature,
                docstring=ast.get_docstring(node) or "",
                annotations=annotations,
                return_annotation=return_annotation,
                call_names=call_names,
            )
        )
        self.generic_visit(node)

    def _build_signature(self, node: ast.FunctionDef | ast.AsyncFunctionDef) -> str:
        parts: List[str] = []
        total_args = list(node.args.args)
        defaults = [None] * (len(total_args) - len(node.args.defaults)) + list(node.args.defaults)
        for arg, default in zip(total_args, defaults):
            part = arg.arg
            ann = self._annotation_to_text(arg.annotation)
            if ann:
                part += f": {ann}"
            if default is not None:
                part += f" = {ast.unparse(default)}"
            parts.append(part)
        if node.args.vararg:
            parts.append(f"*{node.args.vararg.arg}")
        if node.args.kwarg:
            parts.append(f"**{node.args.kwarg.arg}")
        sig = ", ".join(parts)
        if node.returns is not None:
            return f"{node.name}({sig}) -> {self._annotation_to_text(node.returns)}"
        return f"{node.name}({sig})"

    def _annotation_to_text(self, annotation: Any) -> Optional[str]:
        if annotation is None:
            return None
        try:
            return ast.unparse(annotation)
        except Exception:
            return None

    def _extract_call_names(self, node: ast.AST) -> List[str]:
        names: List[str] = []
        for child in ast.walk(node):
            if isinstance(child, ast.Call):
                name = self._call_name(child.func)
                if name and name not in names:
                    names.append(name)
        return names

    def _call_name(self, func: ast.AST) -> Optional[str]:
        if isinstance(func, ast.Name):
            return func.id
        if isinstance(func, ast.Attribute):
            return func.attr
        return None
