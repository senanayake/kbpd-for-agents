from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from tools import validate_kbriefs


class ValidatorTests(unittest.TestCase):
    def test_valid_minimal_repository_passes(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = build_repo(Path(tmpdir))

            errors = validate_kbriefs.validate_repository(root)

            self.assertEqual([], errors)

    def test_duplicate_ids_fail(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = build_repo(Path(tmpdir))
            write_kbrief(
                root / ".kbriefs" / "KB-2026-002-second.md",
                brief_id="KB-2026-001",
                brief_type="tradeoff",
            )

            errors = validate_kbriefs.validate_repository(root)

            self.assertTrue(any("duplicate id KB-2026-001" in err for err in errors))

    def test_missing_related_brief_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = build_repo(Path(tmpdir))
            write_kbrief(
                root / ".kbriefs" / "KB-2026-001-first.md",
                brief_id="KB-2026-001",
                brief_type="tradeoff",
                related=["KB-2026-999"],
            )

            errors = validate_kbriefs.validate_repository(root)

            self.assertTrue(
                any("related K-Brief does not exist: KB-2026-999" in err for err in errors)
            )

    def test_skill_name_must_match_directory(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = build_repo(Path(tmpdir))
            skill_file = root / ".agents" / "skills" / "search-kbriefs" / "SKILL.md"
            skill_file.write_text(
                "---\n"
                "name: wrong-name\n"
                "description: Search K-Briefs.\n"
                "---\n"
                "\n"
                "# Search\n",
                encoding="utf-8",
            )

            errors = validate_kbriefs.validate_repository(root)

            self.assertTrue(any("skill name must match directory" in err for err in errors))

    def test_unresolved_template_reference_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = build_repo(Path(tmpdir))
            (root / "AGENTS.md").write_text(
                "Use .kbriefs/templates/missing.md\n", encoding="utf-8"
            )

            errors = validate_kbriefs.validate_repository(root)

            self.assertTrue(
                any("missing referenced template .kbriefs/templates/missing.md" in err for err in errors)
            )


def build_repo(root: Path) -> Path:
    (root / ".kbriefs" / "templates").mkdir(parents=True)
    (root / ".agents" / "skills" / "search-kbriefs").mkdir(parents=True)

    (root / "README.md").write_text("# Test\n", encoding="utf-8")
    (root / "AGENTS.md").write_text(
        "Use .kbriefs/templates/tradeoff.md\n", encoding="utf-8"
    )
    (root / ".kbriefs" / "README.md").write_text("# K-Briefs\n", encoding="utf-8")

    for brief_type, filename in validate_kbriefs.TEMPLATE_BY_TYPE.items():
        write_kbrief(
            root / ".kbriefs" / "templates" / filename,
            brief_id="KB-YYYY-NNN",
            brief_type=brief_type,
            created="YYYY-MM-DD",
            updated="YYYY-MM-DD",
            is_template=True,
        )

    write_kbrief(
        root / ".kbriefs" / "KB-2026-001-first.md",
        brief_id="KB-2026-001",
        brief_type="tradeoff",
    )

    (root / ".agents" / "skills" / "search-kbriefs" / "SKILL.md").write_text(
        "---\n"
        "name: search-kbriefs\n"
        "description: Search K-Briefs before material decisions.\n"
        "---\n"
        "\n"
        "# Search K-Briefs\n"
        "\n"
        "Use .kbriefs/templates/tradeoff.md.\n",
        encoding="utf-8",
    )

    return root


def write_kbrief(
    path: Path,
    *,
    brief_id: str,
    brief_type: str,
    status: str = "candidate",
    created: str = "2026-07-21",
    updated: str = "2026-07-21",
    related: list[str] | None = None,
    is_template: bool = False,
) -> None:
    related = [] if related is None else related
    sections = validate_kbriefs.REQUIRED_SECTIONS_BY_TYPE[brief_type]
    body = "\n".join(
        [
            f"# {'[Template]' if is_template else 'First'}",
            "",
            *[
                f"## {section}\n\nContent for {section}."
                for section in sections
            ],
            "",
        ]
    )
    path.write_text(
        "---\n"
        f"id: {brief_id}\n"
        f"type: {brief_type}\n"
        f"status: {status}\n"
        f"created: {created}\n"
        f"updated: {updated}\n"
        "tags: [test]\n"
        f"related: [{', '.join(related)}]\n"
        "---\n"
        "\n"
        f"{body}",
        encoding="utf-8",
    )


if __name__ == "__main__":
    unittest.main()
