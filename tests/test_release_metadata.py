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


def _project_version() -> str:
    pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    match = re.search(r'^version = "([^"]+)"$', pyproject, flags=re.MULTILINE)
    if match is None:
        raise AssertionError("pyproject.toml is missing project version")
    return match.group(1)


if __name__ == "__main__":
    unittest.main()
