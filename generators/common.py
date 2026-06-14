from __future__ import annotations
from pathlib import Path
import json
import re
from typing import Any

try:
    import yaml  # type: ignore
except ModuleNotFoundError:  # pragma: no cover
    yaml = None

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "contract"


def _indent_of(line: str) -> int:
    return len(line) - len(line.lstrip(" "))


def _parse_scalar(value: str) -> Any:
    if value.startswith("[") and value.endswith("]"):
        inner = value[1:-1].strip()
        if not inner:
            return []
        return [_parse_scalar(item.strip()) for item in inner.split(",")]
    if value == "true":
        return True
    if value == "false":
        return False
    if re.fullmatch(r"-?\d+", value):
        return int(value)
    return value


def _parse_yaml_block(lines: list[str], index: int, indent: int) -> tuple[Any, int]:
    stripped = lines[index].lstrip(" ")
    if stripped.startswith("- "):
        items: list[Any] = []
        while index < len(lines):
            line = lines[index]
            if _indent_of(line) != indent or not line.lstrip(" ").startswith("- "):
                break
            item = line.lstrip(" ")[2:].strip()
            index += 1
            if item and ":" in item:
                key, sep, remainder = item.partition(":")
                current: dict[str, Any] = {key.strip(): _parse_scalar(remainder.strip()) if remainder.strip() else {}}
                if index < len(lines) and _indent_of(lines[index]) > indent:
                    nested, index = _parse_yaml_block(lines, index, _indent_of(lines[index]))
                    if isinstance(nested, dict):
                        current.update(nested)
                    else:
                        current[key.strip()] = nested
                items.append(current)
            elif item:
                items.append(_parse_scalar(item))
            elif index < len(lines) and _indent_of(lines[index]) > indent:
                value, index = _parse_yaml_block(lines, index, _indent_of(lines[index]))
                items.append(value)
            else:
                items.append("")
        return items, index

    mapping: dict[str, Any] = {}
    while index < len(lines):
        line = lines[index]
        if _indent_of(line) != indent or line.lstrip(" ").startswith("- "):
            break
        key, sep, remainder = line.strip().partition(":")
        if not sep:
            raise ValueError(f"Unsupported YAML line: {line}")
        remainder = remainder.strip()
        index += 1
        if remainder:
            mapping[key] = _parse_scalar(remainder)
        elif index < len(lines) and (
            _indent_of(lines[index]) > indent
            or (
                _indent_of(lines[index]) == indent
                and lines[index].lstrip(" ").startswith("- ")
            )
        ):
            next_indent = _indent_of(lines[index])
            value, index = _parse_yaml_block(lines, index, next_indent)
            mapping[key] = value
        else:
            mapping[key] = {}
    return mapping, index


def _simple_yaml_load(text: str) -> Any:
    lines = [
        line.rstrip()
        for line in text.splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    ]
    if not lines:
        return None
    value, index = _parse_yaml_block(lines, 0, _indent_of(lines[0]))
    if index != len(lines):
        raise ValueError("Failed to parse complete YAML document")
    return value

def load_yaml(name: str) -> Any:
    text = (CONTRACT / name).read_text(encoding="utf-8")
    if yaml is not None:
        return yaml.safe_load(text)
    return _simple_yaml_load(text)

def load_json(path: str) -> Any:
    return json.loads((CONTRACT / path).read_text(encoding="utf-8"))

def member_name(value: str) -> str:
    s = re.sub(r"[^A-Za-z0-9]+", "_", value).upper().strip("_")
    if not s or s[0].isdigit():
        s = "_" + s
    return s

def pascal(name: str) -> str:
    return "".join(part.capitalize() for part in re.split(r"[^A-Za-z0-9]+", name) if part)

def camel(name: str) -> str:
    parts = [part for part in re.split(r"[^A-Za-z0-9]+", name) if part]
    if not parts:
        return name
    return parts[0].lower() + "".join(part.capitalize() for part in parts[1:])

def quote_list(values: list[str]) -> str:
    return ", ".join(repr(v) for v in values)

def contract_data() -> dict[str, Any]:
    subevents_map = load_yaml("subevents.yaml")["subevents"]
    all_subevents = [s for items in subevents_map.values() for s in items]
    return {
        "version": (ROOT / "VERSION").read_text(encoding="utf-8").strip(),
        "scope_types": load_yaml("scope_types.yaml")["scope_types"],
        "channels": load_yaml("channels.yaml")["channels"],
        "directions": load_yaml("directions.yaml")["directions"],
        "framings": load_yaml("framing.yaml")["framings"],
        "event_classifications": load_yaml("event_classification.yaml")["event_classifications"],
        "bindings": load_yaml("bindings.yaml")["bindings"],
        "exchanges": load_yaml("exchanges.yaml")["exchanges"],
        "families": load_yaml("families.yaml")["families"],
        "subevents_by_family": subevents_map,
        "all_subevents": all_subevents,
        "capabilities": load_yaml("capabilities.yaml")["fields"],
        "completion": load_yaml("completion.yaml"),
        "semantic_domains": load_yaml("semantics.yaml")["semantic_domains"],
        "compatibility": load_yaml("compatibility.yaml"),
        "ids": load_yaml("ids.yaml")["fields"],
        "binding_family": load_yaml("legality/binding_family.yaml")["binding_family"],
        "family_subevent": load_yaml("legality/family_subevent.yaml")["family_subevent"],
        "binding_subevent": load_yaml("legality/binding_subevent.yaml")["binding_subevent"],
        "protocols": load_yaml("protocols.yaml")["protocols"],
        "automata": load_yaml("automata.yaml")["automata"],
        "frames": load_yaml("frames.yaml")["frames"],
        "extensions": load_yaml("extensions.yaml")["extensions"],
        "manifest": load_json("manifest.json"),
        "schemas": {
            p.name: json.loads(p.read_text(encoding="utf-8"))
            for p in (CONTRACT / "schemas").glob("*.json")
        },
    }
