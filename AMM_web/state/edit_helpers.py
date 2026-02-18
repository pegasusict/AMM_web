"""Parsing helpers for edit state forms."""

from __future__ import annotations


def none_if_blank(value: str) -> str | None:
    stripped = (value or "").strip()
    return stripped or None


def parse_int_optional(value: str, field_name: str) -> int | None:
    stripped = (value or "").strip()
    if not stripped:
        return None
    try:
        return int(stripped)
    except Exception as exc:
        raise ValueError(f"{field_name} must be an integer") from exc


def parse_int_list(value: str, field_name: str) -> list[int]:
    stripped = (value or "").strip()
    if not stripped:
        return []
    pieces = [part.strip() for part in stripped.split(",")]
    result: list[int] = []
    for part in pieces:
        if not part:
            continue
        try:
            result.append(int(part))
        except Exception as exc:
            raise ValueError(f"{field_name} must be a comma-separated list of integers") from exc
    return result
