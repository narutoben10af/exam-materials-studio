import json
import tempfile
import unittest
from pathlib import Path

from exam_materials_studio.loader import load_resource
from exam_materials_studio.scaffold import ScaffoldError, ScaffoldSpec, default_slug, scaffold_resource
from exam_materials_studio.validator import validate_resource


class ScaffoldTests(unittest.TestCase):
    def setUp(self):
        self.spec = ScaffoldSpec(
            title="Primary Fractions Starter",
            slug="primary-fractions-starter",
            subject="Mathematics",
            level="Primary",
            resource_type="worksheet",
            education_system="General primary",
            exam_board="",
            course="Fractions",
            summary="A starter worksheet for equivalent fractions.",
            learning_objectives=("Represent equivalent fractions with simple models.",),
            skills=("fractions", "equivalent fractions"),
        )

    def test_default_slug_normalizes_title(self):
        self.assertEqual(default_slug("A Level Biology: Enzymes!"), "a-level-biology-enzymes")

    def test_scaffold_json_creates_valid_resource(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "resource.json"

            scaffold_resource(self.spec, path, "json")
            pack = load_resource(path)
            result = validate_resource(path)

            self.assertEqual(pack.title, "Primary Fractions Starter")
            self.assertEqual(pack.learning_objectives, ("Represent equivalent fractions with simple models.",))
            self.assertEqual(len(pack.items), 3)
            self.assertTrue(result.ok)
            self.assertEqual(result.warnings, ())

    def test_scaffold_csv_creates_valid_resource(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "resource.csv"

            scaffold_resource(self.spec, path, "csv")
            pack = load_resource(path)

            self.assertEqual(pack.skills, ("fractions", "equivalent fractions"))
            self.assertEqual(pack.learning_objectives, ("Represent equivalent fractions with simple models.",))
            self.assertEqual(pack.items[0].item_type, "concept-check")

    def test_scaffold_refuses_to_overwrite_without_force(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "resource.json"
            path.write_text(json.dumps({"existing": True}), encoding="utf-8")

            with self.assertRaises(ScaffoldError):
                scaffold_resource(self.spec, path, "json")

    def test_scaffold_force_overwrites_existing_file(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "resource.json"
            path.write_text(json.dumps({"existing": True}), encoding="utf-8")

            scaffold_resource(self.spec, path, "json", force=True)

            self.assertEqual(load_resource(path).slug, "primary-fractions-starter")


if __name__ == "__main__":
    unittest.main()
