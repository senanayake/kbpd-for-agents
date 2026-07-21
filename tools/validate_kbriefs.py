#!/usr/bin/env python3
"""Validate K-Brief and portable Agent Skill structure.

This validator intentionally checks structure only. It does not prove that a
K-Brief's evidence is true or that its conclusion is sound.
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any


ALLOWED_TYPES = {"tradeoff", "limit", "standard", "design-space", "failure-mode"}
ALLOWED_STATUS = {"draft", "candidate", "validated", "superseded", "deprecated"}
REQUIRED_METADATA = ("id", "type", "status", "created", "updated", "tags", "related")
TEMPLATE_BY_TYPE = {
    "tradeoff": "tradeoff.md",
    "limit": "limit.md",
    "standard": "standard.md",
    "design-space": "design-space.md",
    "failure-mode": "failure-mode.md",
}
REQUIRED_SECTIONS_BY_TYPE = {
    "tradeoff": (
        "Context",
        "Variables",
        "Options Considered",
        "Evidence",
        "Analysis",
        "Recommendations",
        "Applicability",
        "Assumptions And Unknowns",
        "Related Knowledge",
    ),
    "limit": (
        "Context",
        "Question",
        "Boundary",
        "Conditions",
        "Evidence",
        "Implications",
        "Recommendations",
        "Applicability",
        "Assumptions And Unknowns",
        "Related Knowledge",
    ),
    "standard": (
        "Context",
        "Standard",
        "Rationale",
        "Evidence",
        "Applicability",
        "Verification",
        "Exceptions",
        "Assumptions And Unknowns",
        "Related Knowledge",
    ),
    "design-space": (
        "Context",
        "Problem Statement",
        "Dimensions",
        "Options In The Space",
        "Evidence",
        "Current Learning",
        "Narrowing Guidance",
        "Applicability",
        "Assumptions And Unknowns",
        "Related Knowledge",
    ),
    "failure-mode": (
        "Context",
        "Trigger",
        "Symptoms",
        "Root Cause",
        "Evidence",
        "Detection",
        "Prevention",
        "Recovery",
        "Applicability",
        "Assumptions And Unknowns",
        "Related Knowledge",
    ),
}

KBRIEF_RE = re.compile(r"^(KB-\d{4}-\d{3})-[a-z0-9][a-z0-9-]*\.md$")
EXAMPLE_RE = re.compile(r"^(KB-EX-\d{3})-[a-z0-9][a-z0-9-]*\.md$")
SKILL_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
TEMPLATE_REF_RE = re.compile(r"\.kbriefs/templates/([a-z0-9-]+\.md)")


@dataclass
class ParsedMarkdown:
    metadata: dict[str, Any]
    body: str


class ValidationError(ValueError):
    pass


def _display(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def parse_frontmatter(path: Path) -> ParsedMarkdown:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValidationError("missing opening frontmatter delimiter")

    closing = text.find("\n---\n", 4)
    if closing == -1:
        raise ValidationError("missing closing frontmatter delimiter")

    raw_frontmatter = text[4:closing]
    body = text[closing + 5 :]
    metadata: dict[str, Any] = {}

    for line_number, raw_line in enumerate(raw_frontmatter.splitlines(), start=2):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if raw_line.startswith((" ", "\t", "-")):
            raise ValidationError(
                f"unsupported nested YAML at frontmatter line {line_number}"
            )
        if ":" not in line:
            raise ValidationError(f"invalid frontmatter line {line_number}: {raw_line}")
        key, raw_value = line.split(":", 1)
        key = key.strip()
        raw_value = raw_value.strip()
        if not key:
            raise ValidationError(f"empty frontmatter key at line {line_number}")
        if key in metadata:
            raise ValidationError(f"duplicate frontmatter key: {key}")
        metadata[key] = parse_scalar_or_list(raw_value)

    return ParsedMarkdown(metadata=metadata, body=body)


def parse_scalar_or_list(raw_value: str) -> Any:
    if raw_value.startswith("[") and raw_value.endswith("]"):
        content = raw_value[1:-1].strip()
        if not content:
            return []
        return [_strip_quotes(item.strip()) for item in content.split(",")]
    return _strip_quotes(raw_value)


def _strip_quotes(value: str) -> str:
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        return value[1:-1]
    return value


def has_section(body: str, section: str) -> bool:
    pattern = re.compile(rf"^##\s+{re.escape(section)}\s*$", re.MULTILINE)
    return bool(pattern.search(body))


def validate_repository(root: Path) -> list[str]:
    root = root.resolve()
    errors: list[str] = []
    kbriefs_dir = root / ".kbriefs"
    skills_dir = root / ".agents" / "skills"

    if not kbriefs_dir.is_dir():
        errors.append("missing .kbriefs/ directory")
        return errors

    if not (kbriefs_dir / "README.md").is_file():
        errors.append("missing .kbriefs/README.md")

    errors.extend(validate_templates(root))

    id_to_path: dict[str, Path] = {}
    related_refs: list[tuple[Path, str]] = []

    for path in kbrief_files(kbriefs_dir):
        parsed = _parse_or_error(path, root, errors)
        if parsed is None:
            continue
        validate_kbrief_file(path, root, parsed, id_to_path, related_refs, errors)

    for path, related_id in related_refs:
        if related_id not in id_to_path:
            errors.append(
                f"{_display(path, root)}: related K-Brief does not exist: {related_id}"
            )

    errors.extend(validate_skills(root, skills_dir))
    errors.extend(validate_template_references(root))

    return errors


def kbrief_files(kbriefs_dir: Path) -> list[Path]:
    files: list[Path] = []
    files.extend(
        path
        for path in sorted(kbriefs_dir.glob("*.md"))
        if path.name != "README.md"
    )
    examples_dir = kbriefs_dir / "examples"
    if examples_dir.is_dir():
        files.extend(sorted(examples_dir.glob("*.md")))
    return files


def validate_templates(root: Path) -> list[str]:
    errors: list[str] = []
    templates_dir = root / ".kbriefs" / "templates"
    if not templates_dir.is_dir():
        return ["missing .kbriefs/templates/ directory"]

    for brief_type, filename in TEMPLATE_BY_TYPE.items():
        path = templates_dir / filename
        if not path.is_file():
            errors.append(f"missing template: .kbriefs/templates/{filename}")
            continue
        parsed = _parse_or_error(path, root, errors)
        if parsed is None:
            continue
        if parsed.metadata.get("type") != brief_type:
            errors.append(
                f"{_display(path, root)}: template type must be {brief_type}"
            )
        for section in REQUIRED_SECTIONS_BY_TYPE[brief_type]:
            if not has_section(parsed.body, section):
                errors.append(
                    f"{_display(path, root)}: missing required section: {section}"
                )

    return errors


def validate_kbrief_file(
    path: Path,
    root: Path,
    parsed: ParsedMarkdown,
    id_to_path: dict[str, Path],
    related_refs: list[tuple[Path, str]],
    errors: list[str],
) -> None:
    rel = _display(path, root)
    metadata = parsed.metadata

    for field in REQUIRED_METADATA:
        if field not in metadata:
            errors.append(f"{rel}: missing required metadata field: {field}")

    filename_match = EXAMPLE_RE.match(path.name) if path.parent.name == "examples" else KBRIEF_RE.match(path.name)
    if filename_match is None:
        expected = "KB-EX-NNN-title.md" if path.parent.name == "examples" else "KB-YYYY-NNN-title.md"
        errors.append(f"{rel}: invalid filename; expected {expected}")
    else:
        filename_id = filename_match.group(1)
        if metadata.get("id") != filename_id:
            errors.append(f"{rel}: id must match filename prefix {filename_id}")

    brief_id = metadata.get("id")
    if isinstance(brief_id, str):
        if brief_id in id_to_path:
            errors.append(
                f"{rel}: duplicate id {brief_id}; first seen in {_display(id_to_path[brief_id], root)}"
            )
        id_to_path[brief_id] = path
    else:
        errors.append(f"{rel}: id must be a string")

    brief_type = metadata.get("type")
    if brief_type not in ALLOWED_TYPES:
        errors.append(f"{rel}: invalid type {brief_type!r}")
    else:
        for section in REQUIRED_SECTIONS_BY_TYPE[brief_type]:
            if not has_section(parsed.body, section):
                errors.append(f"{rel}: missing required section: {section}")

    status = metadata.get("status")
    if status not in ALLOWED_STATUS:
        errors.append(f"{rel}: invalid status {status!r}")

    for field in ("created", "updated"):
        value = metadata.get(field)
        if not isinstance(value, str) or not is_iso_date(value):
            errors.append(f"{rel}: {field} must be YYYY-MM-DD")

    for field in ("tags", "related"):
        value = metadata.get(field)
        if not isinstance(value, list):
            errors.append(f"{rel}: {field} must be an inline list")

    related = metadata.get("related", [])
    if isinstance(related, list):
        for related_id in related:
            if not isinstance(related_id, str):
                errors.append(f"{rel}: related entries must be strings")
            elif not (re.fullmatch(r"KB-\d{4}-\d{3}", related_id) or re.fullmatch(r"KB-EX-\d{3}", related_id)):
                errors.append(f"{rel}: invalid related id format: {related_id}")
            else:
                related_refs.append((path, related_id))

    if not re.search(r"^#\s+\S", parsed.body, re.MULTILINE):
        errors.append(f"{rel}: missing top-level title")


def validate_skills(root: Path, skills_dir: Path) -> list[str]:
    errors: list[str] = []
    if not skills_dir.is_dir():
        errors.append("missing .agents/skills/ directory")
        return errors

    for skill_dir in sorted(path for path in skills_dir.iterdir() if path.is_dir()):
        rel_dir = _display(skill_dir, root)
        if not SKILL_RE.fullmatch(skill_dir.name):
            errors.append(f"{rel_dir}: skill directory must be lowercase hyphen-case")
        skill_file = skill_dir / "SKILL.md"
        if not skill_file.is_file():
            errors.append(f"{rel_dir}: missing SKILL.md")
            continue
        parsed = _parse_or_error(skill_file, root, errors)
        if parsed is None:
            continue
        metadata = parsed.metadata
        extra = set(metadata) - {"name", "description"}
        if extra:
            errors.append(
                f"{_display(skill_file, root)}: unsupported skill metadata fields: {sorted(extra)}"
            )
        if metadata.get("name") != skill_dir.name:
            errors.append(
                f"{_display(skill_file, root)}: skill name must match directory"
            )
        description = metadata.get("description")
        if not isinstance(description, str) or not description.strip():
            errors.append(f"{_display(skill_file, root)}: description is required")
        if not parsed.body.strip():
            errors.append(f"{_display(skill_file, root)}: skill body is empty")

    return errors


def validate_template_references(root: Path) -> list[str]:
    errors: list[str] = []
    referenced_files = [
        root / "AGENTS.md",
        root / "README.md",
        root / ".kbriefs" / "README.md",
    ]
    skills_dir = root / ".agents" / "skills"
    if skills_dir.is_dir():
        referenced_files.extend(sorted(skills_dir.glob("*/SKILL.md")))

    for path in referenced_files:
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        for match in TEMPLATE_REF_RE.finditer(text):
            template = root / ".kbriefs" / "templates" / match.group(1)
            if not template.is_file():
                errors.append(
                    f"{_display(path, root)}: missing referenced template {match.group(0)}"
                )

    return errors


def _parse_or_error(path: Path, root: Path, errors: list[str]) -> ParsedMarkdown | None:
    try:
        return parse_frontmatter(path)
    except ValidationError as exc:
        errors.append(f"{_display(path, root)}: {exc}")
        return None


def is_iso_date(value: str) -> bool:
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
        return False
    try:
        date.fromisoformat(value)
    except ValueError:
        return False
    return True


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "root",
        nargs="?",
        default=".",
        help="repository root to validate; defaults to current directory",
    )
    args = parser.parse_args(argv)

    errors = validate_repository(Path(args.root))
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        print(f"Validation failed: {len(errors)} error(s)", file=sys.stderr)
        return 1

    print("K-Brief validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
