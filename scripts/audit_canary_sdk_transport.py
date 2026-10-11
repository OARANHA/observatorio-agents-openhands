"""Read-only AST audit of OpenHands SDK 1.53.0 LiteLLM call sites.

Inventory only; it cannot certify absence of dynamic imports, plugins,
provider metadata HTTP, redirects, retries inside LiteLLM or other egress.
It never creates an LLM, opens a network connection or patches the SDK.
"""
from __future__ import annotations

import ast
import importlib
import importlib.metadata
import inspect

from canary_controls import GateError

EXPECTED = {
    "litellm_completion": "_transport_call",
    "litellm_acompletion": "_atransport_call",
    "litellm_responses": "responses",
    "litellm_aresponses": "aresponses",
}
NEEDED_METHODS = (
    "completion", "acompletion", "responses", "aresponses",
    "_make_retry_decorator", "_handle_error", "_ahandle_error",
    "_resolve_refreshed_api_key", "_auth_refreshed_llm",
    "resolve_runtime_metadata", "aresolve_runtime_metadata",
)


def check_source(source: str) -> dict:
    """Reject new/duplicated SDK LiteLLM aliases or unreviewed call sites."""
    try:
        root = ast.parse(source)
    except SyntaxError as exc:
        raise GateError("sdk_source_not_parseable") from exc
    llms = [x for x in root.body if isinstance(x, ast.ClassDef) and x.name == "LLM"]
    if len(llms) != 1:
        raise GateError("sdk_llm_class_changed")
    llm=llms[0]
    properties={x.name for x in llm.body if isinstance(x,ast.FunctionDef)
                and any(isinstance(d,ast.Name) and d.id=='property' for d in x.decorator_list)}
    # Official typing.overload signatures precede one executable implementation.
    method_nodes=[x for x in llm.body if isinstance(x,(ast.FunctionDef,ast.AsyncFunctionDef))
                  and not any((isinstance(d,ast.Name) and d.id=='overload')
                    or (isinstance(d,ast.Attribute) and isinstance(d.value,ast.Name)
                        and d.value.id==x.name and x.name in properties and d.attr=='setter')
                    for d in x.decorator_list)]
    if len({x.name for x in method_nodes}) != len(method_nodes):
        raise GateError('sdk_duplicate_method')
    methods={
        x.name:x for x in llm.body
        if isinstance(x, (ast.FunctionDef, ast.AsyncFunctionDef))
    }
    if not all(name in methods for name in (*NEEDED_METHODS, *EXPECTED.values())):
        raise GateError("sdk_method_inventory_changed")

    imported={}
    module_aliases={'litellm'}
    for node in ast.walk(root):
        if isinstance(node,ast.Import):
            module_aliases.update(alias.asname or alias.name for alias in node.names
                                  if alias.name=='litellm')
        if isinstance(node,ast.ImportFrom) and node.module in ('litellm','litellm.responses.main'):
            for alias in node.names:
                if alias.name in ('completion','acompletion','responses','aresponses'):
                    if alias.asname not in EXPECTED:
                        raise GateError('sdk_unreviewed_transport_alias')
    alias_counts={name:0 for name in EXPECTED}
    for node in root.body:
        if isinstance(node,ast.ImportFrom):
            for alias in node.names:
                if alias.asname in EXPECTED:
                    alias_counts[alias.asname]+=1
                    imported[alias.asname]=(node.module,alias.name)
    required_imports={
        "litellm_completion": ("litellm","completion"),
        "litellm_acompletion": ("litellm","acompletion"),
        "litellm_responses": ("litellm.responses.main","responses"),
        "litellm_aresponses": ("litellm.responses.main","aresponses"),
    }
    if imported != required_imports or alias_counts != {name:1 for name in EXPECTED}:
        raise GateError("sdk_litellm_alias_inventory_changed")

    # All scopes, including module helpers, must not add a direct module sink.
    for node in ast.walk(root):
        if (isinstance(node,ast.Call) and isinstance(node.func,ast.Attribute)
            and isinstance(node.func.value,ast.Name)
            and node.func.value.id in module_aliases
            and node.func.attr in ('completion','acompletion','responses','aresponses')):
            raise GateError('sdk_new_direct_litellm_call')

    locations={name:[] for name in EXPECTED}
    for method, definition in methods.items():
        for node in ast.walk(definition):
            if not isinstance(node,ast.Call):
                continue
            func=node.func
            if isinstance(func,ast.Name) and func.id in EXPECTED:
                locations[func.id].append(method)
            # New direct litellm.completion calls must not evade review.
            if (isinstance(func,ast.Attribute) and isinstance(func.value,ast.Name)
                and func.value.id=="litellm"
                and func.attr in ("completion","acompletion","responses","aresponses")):
                raise GateError("sdk_new_direct_litellm_call")
    if locations != {name:[location] for name,location in EXPECTED.items()}:
        raise GateError("sdk_transport_calls_changed")
    all_hits={
        name: sum(
            1 for node in ast.walk(root)
            if isinstance(node,ast.Call)
            and isinstance(node.func,ast.Name) and node.func.id==name
        )
        for name in EXPECTED
    }
    if all_hits != {name:1 for name in EXPECTED}:
        raise GateError("sdk_unreviewed_litellm_sink_call")

    # Metadata discovery may initiate auxiliary HTTP BEFORE these four sinks.
    metadata_calls={
        key for name in ("resolve_runtime_metadata","aresolve_runtime_metadata")
        for node in ast.walk(methods[name])
        if isinstance(node,ast.Call)
        for key in (
            [node.func.id] if isinstance(node.func,ast.Name) else []
        )
        if key in ("resolve_provider_metadata_sync","aresolve_provider_metadata")
    }
    if metadata_calls != {
        "resolve_provider_metadata_sync","aresolve_provider_metadata"
    }:
        raise GateError("sdk_metadata_egress_inventory_changed")

    return {
        "sdk": "1.53.0",
        "reviewed_sinks": dict(EXPECTED),
        "known_metadata_egress": sorted(metadata_calls),
        "transport_attempts_in_real_sdk": 0,
        "provider_calls_in_audit": 0,
        "verdict": "surface_inventory_only_no_live_go",
    }


def inspect_installed_sdk() -> dict:
    try:
        version = importlib.metadata.version("openhands-sdk")
    except importlib.metadata.PackageNotFoundError as exc:
        raise GateError("sdk_not_installed_for_inventory") from exc
    if version != "1.53.0":
        raise GateError("sdk_version_mismatch")
    module=importlib.import_module("openhands.sdk.llm.llm")
    return check_source(inspect.getsource(module))
