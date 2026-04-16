from __future__ import annotations

from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any, Callable, Dict, List, Sequence, TypeVar
import re

from .models import FunctionSemantics, SPLNode, SPLTree, SourceHandle, join_path
from .python_scanner import FunctionInfo, PythonProjectScanner
from .semantic_builder import FunctionAnalysisBundle, FunctionSemanticBuilder


T = TypeVar("T")
R = TypeVar("R")


class ProjectSPLBuilder:
    def __init__(self, semantic_builder: FunctionSemanticBuilder, max_workers: int = 4):
        self.semantic_builder = semantic_builder
        self.max_workers = max(1, max_workers)
        self.scanner = PythonProjectScanner()

    def build_from_source(
        self,
        source_handle: SourceHandle,
        use_llm: bool,
    ) -> tuple[SPLTree, Dict[str, str]]:
        function_infos = self.scanner.scan_project(source_handle.project_root)
        bundles = self._parallel_map(
            function_infos,
            lambda info: self.semantic_builder.prepare_analysis_bundle(info, use_llm=use_llm),
        )

        base_semantics = self._parallel_map(
            bundles,
            lambda bundle: self.semantic_builder.build_from_bundle(bundle, dependency_context=[], use_llm=use_llm),
        )
        base_semantics_by_name = {
            bundle.info.qualified_name: semantics for bundle, semantics in zip(bundles, base_semantics)
        }
        resolved_calls = self._resolve_call_targets(function_infos)
        dependency_contexts = self._build_dependency_contexts(resolved_calls, base_semantics_by_name)

        refined_semantics = self._parallel_map(
            bundles,
            lambda bundle: self.semantic_builder.build_from_bundle(
                bundle,
                dependency_context=dependency_contexts.get(bundle.info.qualified_name, []),
                use_llm=use_llm,
            ),
        )

        module_docs: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
        exported_spl: Dict[str, str] = {}
        for bundle, semantics in zip(bundles, refined_semantics):
            info = bundle.info
            spl_text = self.semantic_builder.render_spl(semantics)
            export_key = f"{info.module_path}::{info.qualified_name}"
            exported_spl[export_key] = spl_text
            module_docs[info.module_path].append(
                {
                    "semantics": semantics,
                    "module_path": info.module_path,
                    "qualified_name": info.qualified_name,
                    "function_info": info,
                    "spl_text": spl_text,
                    "call_names": resolved_calls.get(info.qualified_name, []),
                    "analysis_bundle": bundle,
                }
            )
        tree = self._tree_from_function_docs(source_handle, module_docs)
        return tree, exported_spl

    def _parallel_map(self, items: Sequence[T], fn: Callable[[T], R]) -> List[R]:
        if len(items) <= 1 or self.max_workers <= 1:
            return [fn(item) for item in items]

        results: List[Optional[R]] = [None] * len(items)
        with ThreadPoolExecutor(max_workers=min(self.max_workers, len(items))) as executor:
            future_map = {executor.submit(fn, item): index for index, item in enumerate(items)}
            for future in as_completed(future_map):
                index = future_map[future]
                results[index] = future.result()
        return [result for result in results if result is not None]

    def _resolve_call_targets(self, function_infos: List[FunctionInfo]) -> Dict[str, List[str]]:
        by_qualified = {info.qualified_name: info for info in function_infos}
        by_short: Dict[str, List[FunctionInfo]] = defaultdict(list)
        by_module_short: Dict[tuple[str, str], List[FunctionInfo]] = defaultdict(list)
        by_class_short: Dict[tuple[str, str, str], List[FunctionInfo]] = defaultdict(list)

        for info in function_infos:
            short_name = info.qualified_name.split(".")[-1]
            by_short[short_name].append(info)
            by_module_short[(info.module_path, short_name)].append(info)
            if info.class_name:
                by_class_short[(info.module_path, info.class_name, short_name)].append(info)

        resolved: Dict[str, List[str]] = {}
        for info in function_infos:
            targets: List[str] = []
            for call_name in info.call_names:
                target = self._pick_call_target(
                    info=info,
                    call_name=call_name,
                    by_qualified=by_qualified,
                    by_short=by_short,
                    by_module_short=by_module_short,
                    by_class_short=by_class_short,
                )
                if target and target != info.qualified_name and target not in targets:
                    targets.append(target)
            resolved[info.qualified_name] = targets
        return resolved

    def _pick_call_target(
        self,
        info: FunctionInfo,
        call_name: str,
        by_qualified: Dict[str, FunctionInfo],
        by_short: Dict[str, List[FunctionInfo]],
        by_module_short: Dict[tuple[str, str], List[FunctionInfo]],
        by_class_short: Dict[tuple[str, str, str], List[FunctionInfo]],
    ) -> Optional[str]:
        normalized = self._normalize_call_name(call_name)
        if normalized in by_qualified:
            return normalized

        short_name = normalized.split(".")[-1]
        if info.class_name:
            class_candidates = by_class_short.get((info.module_path, info.class_name, short_name), [])
            if len(class_candidates) == 1:
                return class_candidates[0].qualified_name

        module_candidates = by_module_short.get((info.module_path, short_name), [])
        if len(module_candidates) == 1:
            return module_candidates[0].qualified_name

        candidates = by_short.get(short_name, [])
        if len(candidates) == 1:
            return candidates[0].qualified_name
        if candidates:
            same_module = [candidate for candidate in candidates if candidate.module_path == info.module_path]
            if len(same_module) == 1:
                return same_module[0].qualified_name
            if same_module:
                return same_module[0].qualified_name
            return candidates[0].qualified_name
        return None

    def _build_dependency_contexts(
        self,
        resolved_calls: Dict[str, List[str]],
        semantics_by_name: Dict[str, FunctionSemantics],
    ) -> Dict[str, List[Dict[str, Any]]]:
        contexts: Dict[str, List[Dict[str, Any]]] = {}
        for qualified_name, callees in resolved_calls.items():
            items: List[Dict[str, Any]] = []
            for callee_name in callees:
                semantics = semantics_by_name.get(callee_name)
                if semantics is None:
                    continue
                items.append(
                    {
                        "worker_name": callee_name,
                        "brief_description": semantics.brief_description,
                        "inputs": semantics.inputs,
                        "outputs": semantics.outputs,
                        "main_flow_excerpt": semantics.main_flow[:3],
                    }
                )
            contexts[qualified_name] = items
        return contexts

    def _tree_from_function_docs(
        self,
        source_handle: SourceHandle,
        module_docs: Dict[str, List[Dict[str, Any]]],
    ) -> SPLTree:
        root = SPLNode(
            node_type="project",
            name=source_handle.display_name,
            path="/",
            content={
                "project_name": source_handle.display_name,
                "source_type": source_handle.source_type,
            },
            metadata={
                "source": source_handle.normalized_source,
                "commit": source_handle.commit,
            },
        )
        modules_root = SPLNode(node_type="field", name="modules", path="/modules", content=None)
        root.add_child(modules_root)

        function_lookup: Dict[str, str] = {}
        unresolved_calls: Dict[str, List[str]] = {}
        function_nodes: List[SPLNode] = []

        for module_path in sorted(module_docs.keys()):
            module_node = SPLNode(
                node_type="module",
                name=module_path,
                path=join_path(modules_root.path, module_path),
                content={"module_path": module_path},
            )
            modules_root.add_child(module_node)
            functions_field = SPLNode(
                node_type="field",
                name="functions",
                path=join_path(module_node.path, "functions"),
            )
            module_node.add_child(functions_field)

            for entry in sorted(module_docs[module_path], key=lambda item: item["qualified_name"]):
                semantics: FunctionSemantics = entry["semantics"]
                qualified_name = entry["qualified_name"]
                function_node = self._build_function_node(module_path, qualified_name, semantics, entry)
                functions_field.add_child(function_node)
                function_lookup[qualified_name] = function_node.path
                function_lookup[qualified_name.split(".")[-1]] = function_node.path
                unresolved_calls[function_node.path] = entry.get("call_names") or []
                function_nodes.append(function_node)

        reverse_calls: Dict[str, List[str]] = defaultdict(list)
        for function_node in function_nodes:
            calls = self._resolve_call_paths(unresolved_calls[function_node.path], function_lookup)
            self._set_field_content(function_node, "calls", calls)
            for call_path in calls:
                reverse_calls[call_path].append(function_node.path)

        for function_node in function_nodes:
            callers = sorted(reverse_calls.get(function_node.path, []))
            self._set_field_content(function_node, "called_by", callers)

        return SPLTree(
            schema_version="1.0",
            project_id=source_handle.project_id,
            project_name=source_handle.display_name,
            source={
                "type": source_handle.source_type,
                "value": source_handle.normalized_source,
                "commit": source_handle.commit,
            },
            root=root,
            metadata=source_handle.metadata,
        )

    def _build_function_node(
        self,
        module_path: str,
        qualified_name: str,
        semantics: FunctionSemantics,
        entry: Dict[str, Any],
    ) -> SPLNode:
        function_path = join_path(join_path("/modules", module_path), f"function::{qualified_name}")
        info: Optional[FunctionInfo] = entry.get("function_info")
        function_node = SPLNode(
            node_type="function",
            name=qualified_name,
            path=function_path,
            content={"summary": semantics.brief_description},
            metadata={
                "module_path": module_path,
                "qualified_name": qualified_name,
                "signature": info.signature if info else "",
                "lineno": info.lineno if info else None,
                "end_lineno": info.end_lineno if info else None,
                "source_file": info.module_abspath if info else None,
                "sub_analysis_count": len((semantics.raw_json or {}).get("analysis_context", {}).get("sub_analyses", [])),
                "dependency_count": len((semantics.raw_json or {}).get("analysis_context", {}).get("dependency_context", [])),
            },
        )

        function_node.add_child(
            SPLNode(
                node_type="field",
                name="summary",
                path=join_path(function_path, "summary"),
                content=semantics.brief_description,
            )
        )
        function_node.add_child(self._list_field(function_path, "inputs", semantics.inputs))
        function_node.add_child(self._list_field(function_path, "outputs", semantics.outputs))
        function_node.add_child(self._main_flow_field(function_path, semantics.main_flow))
        function_node.add_child(self._alternative_flows_field(function_path, semantics.alternative_flows))
        function_node.add_child(self._exception_flows_field(function_path, semantics.exception_flows))
        function_node.add_child(self._list_field(function_path, "calls", []))
        function_node.add_child(self._list_field(function_path, "called_by", []))
        function_node.add_child(
            SPLNode(
                node_type="field",
                name="analysis_context",
                path=join_path(function_path, "analysis_context"),
                content=(semantics.raw_json or {}).get("analysis_context", {}),
            )
        )
        function_node.add_child(
            SPLNode(
                node_type="field",
                name="raw_spl",
                path=join_path(function_path, "raw_spl"),
                content=entry.get("spl_text", ""),
            )
        )
        return function_node

    def _list_field(self, function_path: str, field_name: str, content: List[Any]) -> SPLNode:
        return SPLNode(
            node_type="field",
            name=field_name,
            path=join_path(function_path, field_name),
            content=content,
        )

    def _main_flow_field(self, function_path: str, steps: List[Dict[str, Any]]) -> SPLNode:
        node = SPLNode(
            node_type="field",
            name="main_flow",
            path=join_path(function_path, "main_flow"),
            content=steps,
        )
        for index, step in enumerate(steps, start=1):
            node.add_child(
                SPLNode(
                    node_type="step",
                    name=f"step_{index:03d}",
                    path=join_path(node.path, f"step_{index:03d}"),
                    content=step,
                )
            )
        return node

    def _alternative_flows_field(self, function_path: str, flows: List[Dict[str, Any]]) -> SPLNode:
        node = SPLNode(
            node_type="field",
            name="alternative_flows",
            path=join_path(function_path, "alternative_flows"),
            content=flows,
        )
        for flow_index, flow in enumerate(flows, start=1):
            flow_node = SPLNode(
                node_type="flow",
                name=f"alternative_{flow_index:03d}",
                path=join_path(node.path, f"alternative_{flow_index:03d}"),
                content={"condition": flow.get("condition", ""), "type": "alternative"},
            )
            for step_index, step in enumerate(flow.get("steps", []), start=1):
                flow_node.add_child(
                    SPLNode(
                        node_type="step",
                        name=f"step_{step_index:03d}",
                        path=join_path(flow_node.path, f"step_{step_index:03d}"),
                        content=step,
                    )
                )
            node.add_child(flow_node)
        return node

    def _exception_flows_field(self, function_path: str, flows: List[Dict[str, Any]]) -> SPLNode:
        node = SPLNode(
            node_type="field",
            name="exception_flows",
            path=join_path(function_path, "exception_flows"),
            content=flows,
        )
        for flow_index, flow in enumerate(flows, start=1):
            node.add_child(
                SPLNode(
                    node_type="flow",
                    name=f"exception_{flow_index:03d}",
                    path=join_path(node.path, f"exception_{flow_index:03d}"),
                    content=flow,
                )
            )
        return node

    def _set_field_content(self, function_node: SPLNode, field_name: str, content: List[str]) -> None:
        for child in function_node.children:
            if child.name == field_name:
                child.content = content
                return

    def _resolve_call_paths(self, call_names: List[str], lookup: Dict[str, str]) -> List[str]:
        resolved: List[str] = []
        for name in call_names:
            key = self._normalize_call_name(name)
            if key in lookup and lookup[key] not in resolved:
                resolved.append(lookup[key])
        return resolved

    def _normalize_call_name(self, name: str) -> str:
        text = re.sub(r"</?SPL>", "", name).strip()
        return text.split(".")[-1]
