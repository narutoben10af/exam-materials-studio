import re
import unittest
from pathlib import Path

import exam_materials_studio


ROOT = Path(__file__).resolve().parents[1]


class ReleaseMetadataTests(unittest.TestCase):
    def test_package_version_matches_project_metadata(self):
        project_version = _project_version()

        self.assertEqual(exam_materials_studio.__version__, project_version)

    def test_changelog_top_entry_matches_project_version(self):
        changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
        match = re.search(r"^## v([0-9]+\.[0-9]+\.[0-9]+)", changelog, flags=re.MULTILINE)

        self.assertIsNotNone(match)
        self.assertEqual(match.group(1), _project_version())

    def test_v040_release_documents_metadata_workflows(self):
        changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
        section = _changelog_section(changelog, "v0.4.0")

        for expected in (
            "delivery_modes",
            "duration_minutes",
            "prerequisites",
            "materials",
            "scaffold",
            "catalogs",
            "inventory",
        ):
            self.assertIn(expected, section)

    def test_v050_release_documents_assessment_metadata(self):
        changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
        section = _changelog_section(changelog, "v0.5.0")

        for expected in (
            "command_word",
            "marks",
            "assessment",
            "answer keys",
            "JSON catalogs",
            "inventory",
            "scaffold",
        ):
            self.assertIn(expected, section)

    def test_v060_release_documents_rubric_metadata(self):
        changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
        section = _changelog_section(changelog, "v0.6.0")

        for expected in (
            "rubric",
            "answer keys",
            "learner-facing resources",
            "JSON catalogs",
            "inventory",
            "scaffold",
        ):
            self.assertIn(expected, section)


def _project_version() -> str:
    pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    match = re.search(r'^version = "([^"]+)"$', pyproject, flags=re.MULTILINE)
    if match is None:
        raise AssertionError("pyproject.toml is missing project version")
    return match.group(1)


def _changelog_section(changelog: str, heading: str) -> str:
    match = re.search(
        rf"^## {re.escape(heading)}\n(?P<section>.*?)(?=^## |\Z)",
        changelog,
        flags=re.MULTILINE | re.DOTALL,
    )
    if match is None:
        raise AssertionError(f"CHANGELOG.md is missing {heading}")
    return match.group("section")


if __name__ == "__main__":
    unittest.main()
