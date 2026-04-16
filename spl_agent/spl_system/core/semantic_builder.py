from __future__ import annotations

import ast
import importlib.resources
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional

from .config import LLMConfig
from .llm_runtime import chat_completion_with_logging, create_openai_client
from .models import FunctionSemantics
from .python_scanner import FunctionInfo


@dataclass
class FunctionAnalysisBundle:
    info: FunctionInfo
    ast_context: Dict[str, Any]
    subcodes: List[Dict[str, Any]]
    analyzed_subcodes: List[Dict[str, Any]]
    sub_analyses: List[Dict[str, Any]]


class RecursiveASTDecomposer:
    analyzer_map = {
        "For": "control_flow",
        "While": "control_flow",
        "If": "control_flow",
        "Try": "control_flow",
        "With": "control_flow",
        "Match": "control_flow",
        "Assign": "data_flow",
        "AnnAssign": "data_flow",
        "AugAssign": "data_flow",
        "Return": "data_flow",
        "Expr": "data_flow",
        "Call": "function_call",
        "Block": "data_flow",
    }

    simple_nodes = {"Assign", "AnnAssign", "AugAssign", "Return", "Expr"}
    complex_nodes = {"For", "While", "If", "Try", "With", "Match", "Call"}

    def __init__(self, depth_threshold: int = 4, size_threshold: int = 6):
        self.depth_threshold = depth_threshold
        self.size_threshold = size_threshold

    def build_ast_context(self, info: FunctionInfo) -> Dict[str, Any]:
        tree = ast.parse(info.code)
        function_node = next(
            node for node in ast.walk(tree) if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        )
        return {
            "name": info.qualified_name,
            "code": info.code,
            "lineno": info.lineno,
            "signature": info.signature,
            "ast_analysis": {
                "body_analysis": self._analyze_function_body(function_node.body, info.code),
                "ast_structure": self._generate_ast_structure(function_node),
            },
        }

    def decompose(self, ast_context: Dict[str, Any], depth: int = 0, max_depth: int = 5) -> List[Dict[str, Any]]:
        if depth > max_depth:
            return []

        code = ast_context.get("code", "")
        body_analysis = ast_context.get("ast_analysis", {}).get("body_analysis", {})
        ordered_nodes = self._ordered_body_nodes(body_analysis)
        subcodes: List[Dict[str, Any]] = []
        block: List[Dict[str, Any]] = []

        for node in ordered_nodes:
            node_type = node["type"]
            if node_type in self.simple_nodes:
                block.append(node)
                continue

            if block:
                block_entry = self._merge_block(block, depth)
                if block_entry:
                    subcodes.append(block_entry)
                block = []

            subcode = {
                "type": node_type,
                "analyzer_type": self.analyzer_map.get(node_type, "data_flow"),
                "code": node["code"],
                "depth": depth,
                "lineno": node["lineno"],
            }
            if self._should_recurse(node["code"], node_type, depth):
                child_context = {
                    "code": node["code"],
                    "ast_analysis": {"body_analysis": self._analyze_code_structure(node["code"])},
                }
                children = self.decompose(child_context, depth + 1, max_depth=max_depth)
                if children:
                    subcode["children"] = children
            subcodes.append(subcode)

        if block:
            block_entry = self._merge_block(block, depth)
            if block_entry:
                subcodes.append(block_entry)

        if not subcodes and code.strip():
            return [
                {
                    "type": "Block",
                    "analyzer_type": "data_flow",
                    "code": code,
                    "depth": depth,
                    "lineno": ast_context.get("lineno", 1),
                }
            ]
        return subcodes

    def _should_recurse(self, code: str, node_type: str, depth: int) -> bool:
        line_count = len((code or "").splitlines())
        return (
            depth < self.depth_threshold
            and node_type in self.complex_nodes
            and line_count >= self.size_threshold
        )

    def _ordered_body_nodes(self, body_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        ordered: List[Dict[str, Any]] = []
        mapping = [
            ("control_structures", "If"),
            ("loops", None),
            ("assignments", "Assign"),
            ("function_calls", "Call"),
            ("returns", "Return"),
        ]
        for key, fallback_type in mapping:
            for item in body_analysis.get(key, []):
                raw_type = str(item.get("type") or fallback_type or "Block")
                node_type = raw_type.capitalize()
                if node_type == "Function_call":
                    node_type = "Call"
                ordered.append(
                    {
                        "type": node_type if node_type in self.analyzer_map else (fallback_type or node_type),
                        "code": item.get("code", ""),
                        "lineno": item.get("lineno", 0),
                    }
                )
        ordered.sort(key=lambda item: item["lineno"])
        return ordered

    def _merge_block(self, block: List[Dict[str, Any]], depth: int) -> Optional[Dict[str, Any]]:
        code_parts = [item["code"] for item in block if item.get("code")]
        if not code_parts:
            return None
        return {
            "type": "Block",
            "analyzer_type": "data_flow",
            "code": "\n".join(code_parts),
            "depth": depth,
            "lineno": block[0]["lineno"],
            "node_count": len(block),
        }

    def _generate_ast_structure(self, node: ast.AST) -> Dict[str, Any]:
        result = {
            "type": type(node).__name__,
            "lineno": getattr(node, "lineno", None),
        }
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            result["name"] = node.name
            result["args_count"] = len(node.args.args)
        return result

    def _analyze_function_body(self, body: List[ast.stmt], content: str) -> Dict[str, Any]:
        analysis = {
            "statements_count": len(body),
            "control_structures": [],
            "loops": [],
            "assignments": [],
            "function_calls": [],
            "returns": [],
        }
        for node in body:
            if isinstance(node, ast.If):
                analysis["control_structures"].append(
                    {"type": "if", "lineno": node.lineno, "code": ast.get_source_segment(content, node)}
                )
            elif isinstance(node, (ast.For, ast.AsyncFor)):
                analysis["loops"].append(
                    {"type": "for", "lineno": node.lineno, "code": ast.get_source_segment(content, node)}
                )
            elif isinstance(node, ast.While):
                analysis["loops"].append(
                    {"type": "while", "lineno": node.lineno, "code": ast.get_source_segment(content, node)}
                )
            elif isinstance(node, (ast.Assign, ast.AnnAssign, ast.AugAssign)):
                analysis["assignments"].append(
                    {"type": type(node).__name__.lower(), "lineno": node.lineno, "code": ast.get_source_segment(content, node)}
                )
            elif isinstance(node, ast.Expr) and isinstance(node.value, ast.Call):
                analysis["function_calls"].append(
                    {"type": "function_call", "lineno": node.lineno, "code": ast.get_source_segment(content, node)}
                )
            elif isinstance(node, ast.Return):
                analysis["returns"].append(
                    {"type": "return", "lineno": node.lineno, "code": ast.get_source_segment(content, node)}
                )
        return analysis

    def _analyze_code_structure(self, code: str) -> Dict[str, Any]:
        try:
            tree = ast.parse(code)
        except SyntaxError:
            return {
                "control_structures": [],
                "loops": [],
                "assignments": [],
                "function_calls": [],
                "returns": [],
            }

        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                return self._analyze_function_body(node.body, code)

        return self._analyze_function_body(tree.body, code)


class FunctionSemanticBuilder:
    def __init__(self, llm_config: LLMConfig, base_dir: str | Path):
        self.llm_config = llm_config
        self.base_dir = Path(base_dir)
        self.template_text = self._load_text(
            self.base_dir / "template" / "Method.txt",
            "spl_system.resources.template",
            "Method.txt",
        )
        self.decomposer = RecursiveASTDecomposer()
        self.client = None
        if llm_config.enabled:
            self.client, self.llm_config = create_openai_client(llm_config)

    def _load_text(self, filesystem_path: Path, package_name: str, resource_name: str) -> str:
        if filesystem_path.exists():
            return filesystem_path.read_text(encoding="utf-8")
        return importlib.resources.files(package_name).joinpath(resource_name).read_text(encoding="utf-8")

    def prepare_analysis_bundle(self, info: FunctionInfo, use_llm: bool = True) -> FunctionAnalysisBundle:
        ast_context = self.decomposer.build_ast_context(info)
        subcodes = self.decomposer.decompose(ast_context)
        analyzed_subcodes = self._analyze_subcodes(subcodes, use_llm=use_llm)
        sub_analyses = self._flatten_analyses(analyzed_subcodes)
        return FunctionAnalysisBundle(
            info=info,
            ast_context=ast_context,
            subcodes=subcodes,
            analyzed_subcodes=analyzed_subcodes,
            sub_analyses=sub_analyses,
        )

    def build_from_bundle(
        self,
        bundle: FunctionAnalysisBundle,
        dependency_context: Optional[List[Dict[str, Any]]] = None,
        use_llm: bool = True,
    ) -> FunctionSemantics:
        dependency_context = dependency_context or []
        if use_llm and self.client is not None:
            try:
                return self._build_with_llm(bundle, dependency_context)
            except Exception:
                return self._build_heuristically(bundle, dependency_context)
        return self._build_heuristically(bundle, dependency_context)

    def build(
        self,
        info: FunctionInfo,
        dependency_context: Optional[List[Dict[str, Any]]] = None,
        use_llm: bool = True,
    ) -> FunctionSemantics:
        bundle = self.prepare_analysis_bundle(info, use_llm=use_llm)
        return self.build_from_bundle(bundle, dependency_context=dependency_context, use_llm=use_llm)

    def _build_with_llm(
        self,
        bundle: FunctionAnalysisBundle,
        dependency_context: List[Dict[str, Any]],
    ) -> FunctionSemantics:
        request_payload = {
            "task": "build_function_semantics",
            "function": {
                "qualified_name": bundle.info.qualified_name,
                "module_path": bundle.info.module_path,
                "signature": bundle.info.signature,
                "docstring": bundle.info.docstring,
                "code": bundle.info.code,
                "call_names": bundle.info.call_names,
                "annotations": bundle.info.annotations,
                "return_annotation": bundle.info.return_annotation,
            },
            "template": self.template_text,
            "ast_context": bundle.ast_context,
            "sub_analyses": bundle.sub_analyses,
            "dependency_context": dependency_context,
            "schema": {
                "worker_name": "string",
                "brief_description": "string",
                "inputs": [{"name": "string", "type": "string", "desc": "string"}],
                "outputs": [{"name": "string", "type": "string", "desc": "string"}],
                "main_flow": [{"command": "string", "result": "string", "calls": ["optional_function_name"]}],
                "alternative_flows": [{"condition": "string", "steps": [{"command": "string", "result": "string"}]}],
                "exception_flows": [{"condition": "string", "log": "string", "throw": {"name": "string", "desc": "string"}}],
            },
            "requirements": [
                "Output JSON only.",
                "Use the recursive sub_analyses as the primary structure for understanding the function.",
                "If dependency_context is present, use callee summaries, interfaces, and flow snippets to refine the current function semantics.",
                "Do not invent helpers that are absent from the function body or dependency context.",
                "Keep brief_description to one sentence.",
            ],
        }
        response_obj = self._call_json_llm(
            system_instruction=(
                "You convert Python function analysis into structured SPL semantics. "
                "Return a single JSON object and nothing else."
            ),
            payload=request_payload,
        )
        return self._dict_to_semantics(response_obj, bundle, dependency_context)

    def _build_heuristically(
        self,
        bundle: FunctionAnalysisBundle,
        dependency_context: List[Dict[str, Any]],
    ) -> FunctionSemantics:
        tree = ast.parse(bundle.info.code)
        function_node = next(
            node for node in ast.walk(tree) if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        )
        summary = self._build_summary(bundle, dependency_context)
        inputs = self._build_inputs(bundle.info, function_node)
        outputs = self._build_outputs(bundle.info)
        main_flow, alternative_flows, exception_flows = self._build_flows(function_node, dependency_context)
        raw_json = {
            "worker_name": bundle.info.qualified_name,
            "brief_description": summary,
            "inputs": inputs,
            "outputs": outputs,
            "main_flow": main_flow,
            "alternative_flows": alternative_flows,
            "exception_flows": exception_flows,
            "analysis_context": {
                "ast_context": bundle.ast_context,
                "sub_analyses": bundle.sub_analyses,
                "dependency_context": dependency_context,
            },
        }
        return FunctionSemantics(
            worker_name=bundle.info.qualified_name,
            brief_description=summary,
            inputs=inputs,
            outputs=outputs,
            main_flow=main_flow,
            alternative_flows=alternative_flows,
            exception_flows=exception_flows,
            raw_json=raw_json,
        )

    def render_spl(self, semantics: FunctionSemantics) -> str:
        lines: List[str] = []
        lines.append(
            f'[DEFINE_WORKER: "{self._sanitize(semantics.brief_description)}" {semantics.worker_name}]'
        )
        lines.append("    [INPUTS]")
        for item in semantics.inputs:
            lines.append(
                f'        <REF> {item["name"]} </REF>: {item.get("type", "data_type")} "{self._sanitize(item.get("desc", ""))}"'
            )
        lines.append("    [END_INPUTS]")
        lines.append("")
        lines.append("    [OUTPUTS]")
        for item in semantics.outputs:
            lines.append(
                f'        <REF> {item["name"]} </REF>: {item.get("type", "data_type")} "{self._sanitize(item.get("desc", ""))}"'
            )
        lines.append("    [END_OUTPUTS]")
        lines.append("")
        lines.append("    [MAIN_FLOW]")
        lines.append("        [SEQUENTIAL_BLOCK]")
        for step in semantics.main_flow:
            lines.append(
                f'            [COMMAND {step.get("command", "").strip()} RESULT {step.get("result", "result").strip()}]'
            )
        lines.append("        [END_SEQUENTIAL_BLOCK]")
        lines.append("    [END_MAIN_FLOW]")

        for flow in semantics.alternative_flows:
            lines.append("")
            lines.append(f'    [ALTERNATIVE_FLOW: {flow.get("condition", "")}]')
            lines.append("        [SEQUENTIAL_BLOCK]")
            for step in flow.get("steps", []):
                lines.append(
                    f'            [COMMAND {step.get("command", "").strip()} RESULT {step.get("result", "result").strip()}]'
                )
            lines.append("        [END_SEQUENTIAL_BLOCK]")
            lines.append("    [END_ALTERNATIVE_FLOW]")

        for flow in semantics.exception_flows:
            throw = flow.get("throw", {})
            lines.append("")
            lines.append(f'    [EXCEPTION_FLOW: {flow.get("condition", "")}]')
            lines.append(f'        [LOG "{self._sanitize(flow.get("log", "Exception information"))}"]')
            lines.append(
                f'        [THROW {throw.get("name", "Exception")} "{self._sanitize(throw.get("desc", ""))}"]'
            )
            lines.append("    [END_EXCEPTION_FLOW]")

        lines.append("")
        lines.append("[END_WORKER]")
        return "\n".join(lines)

    def _analyze_subcodes(self, subcodes: List[Dict[str, Any]], use_llm: bool) -> List[Dict[str, Any]]:
        analyzed: List[Dict[str, Any]] = []
        for subcode in subcodes:
            node = dict(subcode)
            node["analysis"] = self._analyze_single_subcode(node, use_llm=use_llm)
            if subcode.get("children"):
                node["children"] = self._analyze_subcodes(subcode["children"], use_llm=use_llm)
            analyzed.append(node)
        return analyzed

    def _analyze_single_subcode(self, subcode: Dict[str, Any], use_llm: bool) -> str:
        if use_llm and self.client is not None:
            try:
                response = self._call_json_llm(
                    system_instruction=(
                        "You explain one Python code fragment. Return JSON only with the key 'analysis'."
                    ),
                    payload={
                        "task": "analyze_subcode",
                        "analyzer_type": subcode.get("analyzer_type", "data_flow"),
                        "node_type": subcode.get("type", "Block"),
                        "depth": subcode.get("depth", 0),
                        "code": subcode.get("code", ""),
                    },
                )
                analysis = str(response.get("analysis") or "").strip()
                if analysis:
                    return analysis
            except Exception:
                pass
        return self._heuristic_subanalysis(subcode)

    def _heuristic_subanalysis(self, subcode: Dict[str, Any]) -> str:
        analyzer_type = str(subcode.get("analyzer_type") or "data_flow")
        code = str(subcode.get("code") or "")
        node_type = str(subcode.get("type") or "Block")
        lines = [line.strip() for line in code.splitlines() if line.strip()]
        joined = " ".join(lines[:3])
        if analyzer_type == "control_flow":
            return f"{node_type} controls branching or iteration around: {joined}"
        if analyzer_type == "function_call":
            call_names = self._extract_call_names_from_code(code)
            if call_names:
                return f"Calls helper functions: {', '.join(call_names)}."
            return f"Executes a function call fragment: {joined}"
        if analyzer_type == "data_flow":
            return f"Moves or transforms data through statements such as: {joined}"
        return f"{node_type} contributes to the function behavior through: {joined}"

    def _flatten_analyses(self, analyzed_subcodes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        flat: List[Dict[str, Any]] = []

        def visit(nodes: List[Dict[str, Any]]) -> None:
            for node in nodes:
                flat.append(
                    {
                        "type": node.get("type", "Block"),
                        "analyzer_type": node.get("analyzer_type", "data_flow"),
                        "depth": node.get("depth", 0),
                        "code": node.get("code", ""),
                        "analysis": node.get("analysis", ""),
                        "lineno": node.get("lineno", 0),
                    }
                )
                children = node.get("children") or []
                if children:
                    visit(children)

        visit(analyzed_subcodes)
        return flat

    def _call_json_llm(self, system_instruction: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        messages = [
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": json.dumps(payload, ensure_ascii=False)},
        ]
        response = chat_completion_with_logging(
            self.client,
            self.llm_config,
            messages,
            model=self.llm_config.model,
            temperature=self.llm_config.temperature,
            timeout=self.llm_config.timeout_sec,
            context={"component": "FunctionSemanticBuilder._call_json_llm", "task": payload.get("task")},
        )
        text = response.choices[0].message.content or ""
        return json.loads(self._extract_json_payload(text))

    def _dict_to_semantics(
        self,
        obj: Dict[str, Any],
        bundle: FunctionAnalysisBundle,
        dependency_context: List[Dict[str, Any]],
    ) -> FunctionSemantics:
        raw_json = dict(obj)
        raw_json["analysis_context"] = {
            "ast_context": bundle.ast_context,
            "sub_analyses": bundle.sub_analyses,
            "dependency_context": dependency_context,
        }
        return FunctionSemantics(
            worker_name=str(obj.get("worker_name") or bundle.info.qualified_name).strip(),
            brief_description=str(obj.get("brief_description") or self._build_summary(bundle, dependency_context)).strip(),
            inputs=obj.get("inputs") or self._build_inputs_from_signature(bundle.info),
            outputs=obj.get("outputs") or self._build_outputs(bundle.info),
            main_flow=obj.get("main_flow") or [],
            alternative_flows=obj.get("alternative_flows") or [],
            exception_flows=obj.get("exception_flows") or [],
            raw_json=raw_json,
        )

    def _extract_json_payload(self, text: str) -> str:
        s = (text or "").strip()
        if not s:
            raise ValueError("LLM returned empty output")
        first_obj = s.find("{")
        if first_obj != -1:
            depth = 0
            in_string = False
            escape = False
            for index in range(first_obj, len(s)):
                char = s[index]
                if escape:
                    escape = False
                    continue
                if char == "\\":
                    escape = True
                    continue
                if char == '"':
                    in_string = not in_string
                    continue
                if in_string:
                    continue
                if char == "{":
                    depth += 1
                elif char == "}":
                    depth -= 1
                    if depth == 0:
                        return s[first_obj:index + 1]
        raise ValueError("No JSON object found in LLM output")

    def _sanitize(self, text: str) -> str:
        return str(text or "").replace('"', "'").strip()

    def _build_summary(self, bundle: FunctionAnalysisBundle, dependency_context: List[Dict[str, Any]]) -> str:
        if bundle.info.docstring:
            first_line = bundle.info.docstring.strip().splitlines()[0].strip()
            if first_line:
                return first_line

        leading_analysis = next(
            (item["analysis"] for item in bundle.sub_analyses if item.get("analysis")),
            "",
        )
        if dependency_context:
            helpers = ", ".join(item["worker_name"] for item in dependency_context[:3])
            return f"{bundle.info.qualified_name} coordinates local logic and helper calls such as {helpers}."
        if leading_analysis:
            return f"{bundle.info.qualified_name} handles logic summarized as: {leading_analysis}"
        return f"Describe the behavior of {bundle.info.qualified_name} in module {bundle.info.module_path}."

    def _build_inputs_from_signature(self, info: FunctionInfo) -> List[Dict[str, str]]:
        try:
            tree = ast.parse(info.code)
            function_node = next(
                node for node in ast.walk(tree) if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
            )
            return self._build_inputs(info, function_node)
        except Exception:
            return []

    def _build_inputs(
        self,
        info: FunctionInfo,
        function_node: ast.FunctionDef | ast.AsyncFunctionDef,
    ) -> List[Dict[str, str]]:
        inputs: List[Dict[str, str]] = []
        for arg in function_node.args.args:
            if arg.arg == "self":
                continue
            inputs.append(
                {
                    "name": arg.arg,
                    "type": info.annotations.get(arg.arg) or "data_type",
                    "desc": f"Input parameter {arg.arg}.",
                }
            )
        return inputs

    def _build_outputs(self, info: FunctionInfo) -> List[Dict[str, str]]:
        output_type = info.return_annotation or "data_type"
        return [{"name": "result", "type": output_type, "desc": f"Return value of {info.qualified_name}."}]

    def _build_flows(
        self,
        function_node: ast.FunctionDef | ast.AsyncFunctionDef,
        dependency_context: List[Dict[str, Any]],
    ) -> tuple[List[Dict[str, Any]], List[Dict[str, Any]], List[Dict[str, Any]]]:
        main_flow: List[Dict[str, Any]] = []
        alternative_flows: List[Dict[str, Any]] = []
        exception_flows: List[Dict[str, Any]] = []

        for stmt in function_node.body:
            if isinstance(stmt, ast.If):
                condition = f"When {ast.unparse(stmt.test)}"
                alternative_flows.append(
                    {"condition": condition, "steps": self._describe_statements(stmt.body, dependency_context)}
                )
                if stmt.orelse:
                    main_flow.append(
                        {
                            "command": f"Evaluate condition {ast.unparse(stmt.test)} and continue with the fallback branch when needed.",
                            "result": "branch_result",
                            "calls": self._extract_call_names_from_stmt(stmt.test),
                        }
                    )
            elif isinstance(stmt, ast.Raise):
                exc_name = self._raise_name(stmt)
                exception_flows.append(
                    {
                        "condition": f"When raising {exc_name}",
                        "log": f"Raised {exc_name}.",
                        "throw": {"name": exc_name, "desc": ast.unparse(stmt.exc) if stmt.exc else exc_name},
                    }
                )
            else:
                main_flow.extend(self._describe_statements([stmt], dependency_context))

        if not main_flow:
            main_flow.append({"command": "Execute the function body.", "result": "result", "calls": []})
        return main_flow, alternative_flows, exception_flows

    def _describe_statements(
        self,
        statements: List[ast.stmt],
        dependency_context: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        steps: List[Dict[str, Any]] = []
        dependency_lookup = self._dependency_lookup(dependency_context)
        for stmt in statements:
            call_names = self._extract_call_names_from_stmt(stmt)
            call_hint = self._dependency_hint(call_names, dependency_lookup)
            if isinstance(stmt, ast.Assign):
                targets = ", ".join(ast.unparse(target) for target in stmt.targets)
                value_text = ast.unparse(stmt.value)
                command = f"Assign {value_text} to {targets}."
                if call_hint:
                    command = f"{command} {call_hint}"
                steps.append({"command": command, "result": targets.replace(', ', '_'), "calls": call_names})
            elif isinstance(stmt, ast.AugAssign):
                target = ast.unparse(stmt.target)
                command = f"Update {target} using {type(stmt.op).__name__} with {ast.unparse(stmt.value)}."
                if call_hint:
                    command = f"{command} {call_hint}"
                steps.append({"command": command, "result": target, "calls": call_names})
            elif isinstance(stmt, (ast.For, ast.AsyncFor)):
                command = f"Iterate over {ast.unparse(stmt.iter)} with loop target {ast.unparse(stmt.target)}."
                steps.append({"command": command, "result": ast.unparse(stmt.target), "calls": call_names})
            elif isinstance(stmt, ast.While):
                steps.append(
                    {
                        "command": f"Repeat while {ast.unparse(stmt.test)} remains true.",
                        "result": "loop_state",
                        "calls": call_names,
                    }
                )
            elif isinstance(stmt, ast.Return):
                expr = ast.unparse(stmt.value) if stmt.value is not None else "None"
                command = f"Return {expr}."
                if call_hint:
                    command = f"{command} {call_hint}"
                steps.append({"command": command, "result": "result", "calls": call_names})
            elif isinstance(stmt, ast.Expr):
                expr_text = ast.unparse(stmt.value)
                command = f"Evaluate {expr_text}."
                if call_hint:
                    command = f"{command} {call_hint}"
                steps.append({"command": command, "result": "expression_result", "calls": call_names})
            elif isinstance(stmt, ast.Try):
                steps.append(
                    {
                        "command": "Execute protected operations and handle exceptional branches if they occur.",
                        "result": "try_result",
                        "calls": call_names,
                    }
                )
            else:
                steps.append(
                    {
                        "command": f"Execute statement {type(stmt).__name__}.",
                        "result": "statement_result",
                        "calls": call_names,
                    }
                )
        return steps

    def _dependency_lookup(self, dependency_context: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
        lookup: Dict[str, Dict[str, Any]] = {}
        for item in dependency_context:
            worker_name = str(item.get("worker_name") or "")
            short_name = worker_name.split(".")[-1]
            if worker_name:
                lookup[worker_name] = item
            if short_name:
                lookup[short_name] = item
        return lookup

    def _dependency_hint(self, call_names: List[str], dependency_lookup: Dict[str, Dict[str, Any]]) -> str:
        for call_name in call_names:
            helper = dependency_lookup.get(call_name) or dependency_lookup.get(call_name.split(".")[-1])
            if helper:
                summary = str(helper.get("brief_description") or "").strip()
                if summary:
                    return f"This step relies on helper {helper['worker_name']}: {summary}"
                return f"This step relies on helper {helper['worker_name']}."
        return ""

    def _extract_call_names_from_stmt(self, node: ast.AST) -> List[str]:
        names: List[str] = []
        for child in ast.walk(node):
            if isinstance(child, ast.Call):
                name = self._call_name(child.func)
                if name and name not in names:
                    names.append(name)
        return names

    def _extract_call_names_from_code(self, code: str) -> List[str]:
        try:
            tree = ast.parse(code)
        except SyntaxError:
            return []
        return self._extract_call_names_from_stmt(tree)

    def _call_name(self, func: ast.AST) -> Optional[str]:
        if isinstance(func, ast.Name):
            return func.id
        if isinstance(func, ast.Attribute):
            base = ast.unparse(func.value) if hasattr(ast, "unparse") else ""
            return f"{base}.{func.attr}" if base else func.attr
        return None

    def _raise_name(self, stmt: ast.Raise) -> str:
        if stmt.exc is None:
            return "Exception"
        if isinstance(stmt.exc, ast.Call):
            func = stmt.exc.func
            if isinstance(func, ast.Name):
                return func.id
            if isinstance(func, ast.Attribute):
                return func.attr
        if isinstance(stmt.exc, ast.Name):
            return stmt.exc.id
        return "Exception"


def tokenize_text(value: str) -> List[str]:
    return [token for token in re.split(r"[^A-Za-z0-9_]+", value.lower()) if token]
