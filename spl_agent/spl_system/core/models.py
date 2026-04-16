from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional
import hashlib
import json
import re
import uuid


NODE_TYPES = {"project", "module", "function", "field", "flow", "step"}


def _slugify(value: str) -> str:
    text = value.strip().replace("\\", "/")
    text = text.replace("/", "::")
    text = re.sub(r"\s+", "_", text)
    return text or "node"


def stable_hash(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


@dataclass
class SPLNode:
    node_type: str
    name: str
    path: str
    content: Any = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    children: List["SPLNode"] = field(default_factory=list)
    node_id: str = field(default_factory=lambda: f"node_{uuid.uuid4().hex[:12]}")

    def __post_init__(self) -> None:
        if self.node_type not in NODE_TYPES:
            raise ValueError(f"Unsupported node type: {self.node_type}")

    def add_child(self, child: "SPLNode") -> None:
        self.children.append(child)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "node_id": self.node_id,
            "node_type": self.node_type,
            "name": self.name,
            "path": self.path,
            "content": self.content,
            "metadata": self.metadata,
            "children": [child.to_dict() for child in self.children],
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SPLNode":
        node = cls(
            node_id=data["node_id"],
            node_type=data["node_type"],
            name=data["name"],
            path=data["path"],
            content=data.get("content"),
            metadata=data.get("metadata", {}),
            children=[],
        )
        for child in data.get("children", []):
            node.add_child(cls.from_dict(child))
        return node


@dataclass
class SPLTree:
    schema_version: str
    project_id: str
    project_name: str
    source: Dict[str, Any]
    root: SPLNode
    metadata: Dict[str, Any] = field(default_factory=dict)
    path_index: Dict[str, SPLNode] = field(default_factory=dict, init=False)
    node_index: Dict[str, SPLNode] = field(default_factory=dict, init=False)

    def __post_init__(self) -> None:
        self.rebuild_indexes()

    def rebuild_indexes(self) -> None:
        self.path_index = {}
        self.node_index = {}
        self._index_node(self.root)

    def _index_node(self, node: SPLNode) -> None:
        self.path_index[node.path] = node
        self.node_index[node.node_id] = node
        for child in node.children:
            self._index_node(child)

    def get_node(self, path: str) -> Optional[SPLNode]:
        if path == "" or path == "/":
            return self.root
        return self.path_index.get(path)

    def iter_nodes(self) -> Iterable[SPLNode]:
        return self.path_index.values()

    def function_nodes(self) -> List[SPLNode]:
        return [node for node in self.path_index.values() if node.node_type == "function"]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "project_id": self.project_id,
            "project_name": self.project_name,
            "source": self.source,
            "metadata": self.metadata,
            "root": self.root.to_dict(),
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SPLTree":
        return cls(
            schema_version=data["schema_version"],
            project_id=data["project_id"],
            project_name=data["project_name"],
            source=data["source"],
            metadata=data.get("metadata", {}),
            root=SPLNode.from_dict(data["root"]),
        )

    @classmethod
    def from_json(cls, text: str) -> "SPLTree":
        return cls.from_dict(json.loads(text))


@dataclass
class FunctionSemantics:
    worker_name: str
    brief_description: str
    inputs: List[Dict[str, Any]]
    outputs: List[Dict[str, Any]]
    main_flow: List[Dict[str, Any]]
    alternative_flows: List[Dict[str, Any]]
    exception_flows: List[Dict[str, Any]]
    raw_json: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "worker_name": self.worker_name,
            "brief_description": self.brief_description,
            "inputs": self.inputs,
            "outputs": self.outputs,
            "main_flow": self.main_flow,
            "alternative_flows": self.alternative_flows,
            "exception_flows": self.exception_flows,
        }


@dataclass
class SourceHandle:
    source_type: str
    display_name: str
    project_root: Path
    cache_key: str
    project_id: str
    normalized_source: str
    commit: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


def join_path(parent: str, name: str) -> str:
    parent = parent.rstrip("/")
    child = _slugify(name)
    if not parent:
        return f"/{child}"
    return f"{parent}/{child}"
