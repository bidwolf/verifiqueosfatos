#!/usr/bin/env python3
"""Validate the shape of the site's posts.json using only the Python stdlib.

Rules follow METODOLOGIA.md (sections 4, 5, 7 and 12):

- "c" is the short seal: 0 em verificação, 1 verdadeiro, 2 falso, 3 parcial/ressalva, 4 não verificável.
- "r" (optional, recommended) is the detailed label and must belong to the family of "c".
- Posts in the new scheme (those with "r") that carry a verdict (c in 1, 2, 3) must cite at least
  one http(s) source in "s". Legacy posts without "r" only get a warning for a missing source.
- "hist" records every change of verdict; "chk" lists who checked and reviewed; "ia" flags AI drafts.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from urllib.parse import urlsplit


VALID_CANDIDATES = {1, 2}
VALID_CHECKS = {0, 1, 2, 3, 4}
VERDICT_CHECKS = {1, 2, 3}

# Detailed label -> the "c" seal it belongs to (METODOLOGIA.md, section 4)
LABELS = {
    "em_verificacao": 0,
    "verdadeiro": 1,
    "falta_contexto": 3,
    "exagerado": 3,
    "subestimado": 3,
    "impreciso": 3,
    "contraditorio": 3,
    "insustentavel": 2,
    "falso": 2,
    "nao_verificavel": 4,
}


def reject_non_json_constant(value: str) -> None:
    raise ValueError(f"{value} is not a valid JSON value")


def valid_http_url(value: object) -> bool:
    if not isinstance(value, str) or any(character.isspace() for character in value):
        return False

    try:
        parsed = urlsplit(value)
        # Accessing .port also validates that a supplied port is numeric and in range.
        _ = parsed.port
    except ValueError:
        return False

    return parsed.scheme.lower() in {"http", "https"} and bool(parsed.hostname)


def non_empty_string(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def check(path: Path) -> tuple[list[str], list[str]]:
    """Return (errors, warnings). Errors fail the build; warnings only inform."""
    try:
        with path.open("r", encoding="utf-8") as source:
            posts = json.load(source, parse_constant=reject_non_json_constant)
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as error:
        return [f"{path}: could not read valid JSON ({error})"], []

    if not isinstance(posts, list):
        return [f"{path}: top-level value must be an array"], []

    errors: list[str] = []
    warnings: list[str] = []
    seen_ids: set[int] = set()
    for index, post in enumerate(posts):
        location = f"{path}[{index}]"
        if not isinstance(post, dict):
            errors.append(f"{location}: each post must be an object")
            continue

        post_id = post.get("id")
        if type(post_id) is not int or post_id < 1:
            errors.append(f"{location}.id: expected a positive integer")
        elif post_id in seen_ids:
            errors.append(f"{location}.id: {post_id} is already used by another post")
        else:
            seen_ids.add(post_id)

        candidate = post.get("n")
        if type(candidate) is not int or candidate not in VALID_CANDIDATES:
            errors.append(f"{location}.n: expected 1 (Lula) or 2 (Flávio)")

        check_value = post.get("c")
        if type(check_value) is not int or check_value not in VALID_CHECKS:
            errors.append(
                f"{location}.c: expected 0 (em verificação), 1 (verdadeiro), 2 (falso), "
                "3 (parcial/ressalva) or 4 (não verificável)"
            )

        for field in ("t", "v"):
            if not isinstance(post.get(field), str):
                errors.append(f"{location}.{field}: expected a string")

        detailed = post.get("r")
        if "r" in post:
            if not isinstance(detailed, str) or detailed not in LABELS:
                errors.append(f"{location}.r: expected one of {', '.join(sorted(LABELS))}")
            elif type(check_value) is int and LABELS[detailed] != check_value:
                errors.append(
                    f"{location}.r: '{detailed}' belongs to c={LABELS[detailed]}, but c={check_value}"
                )

        sources = post.get("s")
        if "s" in post:
            if not isinstance(sources, list):
                errors.append(f"{location}.s: expected an array of http(s) URLs")
            else:
                for source_index, url in enumerate(sources):
                    if not valid_http_url(url):
                        errors.append(
                            f"{location}.s[{source_index}]: expected a valid http(s) URL"
                        )

        has_source = isinstance(sources, list) and any(valid_http_url(url) for url in sources)
        if check_value in VERDICT_CHECKS and not has_source:
            if "r" in post:
                errors.append(f"{location}.s: a verdict needs at least one http(s) source (METODOLOGIA.md, section 5)")
            else:
                warnings.append(f"{location}.s: legacy post without a linked source")

        if "e" in post and not non_empty_string(post["e"]):
            errors.append(f"{location}.e: expected a non-empty string")

        for field in ("h", "a"):
            if field in post and not isinstance(post[field], str):
                errors.append(f"{location}.{field}: expected a string")

        if "hist" in post:
            history = post["hist"]
            if not isinstance(history, list):
                errors.append(f"{location}.hist: expected an array of changes")
            else:
                for change_index, change in enumerate(history):
                    where = f"{location}.hist[{change_index}]"
                    if not isinstance(change, dict):
                        errors.append(f"{where}: each change must be an object")
                        continue
                    for field in ("de", "para"):
                        if not non_empty_string(change.get(field)):
                            errors.append(f"{where}.{field}: expected a non-empty string (label or seal)")
                    for field in ("quando", "motivo"):
                        if field in change and not non_empty_string(change[field]):
                            errors.append(f"{where}.{field}: expected a non-empty string")

        if "chk" in post:
            reviewers = post["chk"]
            if not isinstance(reviewers, list) or not reviewers or not all(non_empty_string(x) for x in reviewers):
                errors.append(f"{location}.chk: expected a non-empty array of names")

        if "ia" in post and type(post["ia"]) is not bool:
            errors.append(f"{location}.ia: expected true or false")

        # Review trail: the check as it was before a methodology review
        if "v0" in post and not non_empty_string(post["v0"]):
            errors.append(f"{location}.v0: expected a non-empty string (original verification text)")
        if "c0" in post and (type(post["c0"]) is not int or post["c0"] not in VALID_CHECKS):
            errors.append(f"{location}.c0: expected the original seal (0-4)")

        # What independent agencies concluded about this same statement
        if "outras" in post:
            others = post["outras"]
            if not isinstance(others, list):
                errors.append(f"{location}.outras: expected an array")
            else:
                for other_index, other in enumerate(others):
                    where = f"{location}.outras[{other_index}]"
                    if not isinstance(other, dict) or not non_empty_string(other.get("agencia")):
                        errors.append(f"{where}: expected an object with a non-empty 'agencia'")
                        continue
                    if "rotulo" in other and not non_empty_string(other["rotulo"]):
                        errors.append(f"{where}.rotulo: expected a non-empty string")
                    if "url" in other and not valid_http_url(other["url"]):
                        errors.append(f"{where}.url: expected a valid http(s) URL")

    return errors, warnings


def validate(path: Path) -> list[str]:
    """Errors only (kept for the tests and other callers)."""
    return check(path)[0]


def main() -> int:
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("posts.json")
    errors, warnings = check(path)
    for warning in warnings:
        print(f"WARNING: {warning}", file=sys.stderr)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print(f"{path}: valid" + (f" ({len(warnings)} warnings)" if warnings else ""))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
