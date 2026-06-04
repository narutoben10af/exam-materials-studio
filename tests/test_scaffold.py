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
            duration_minutes=30,
            prerequisites=("Count equal parts in a shape.",),
            materials=("Fraction strips", "Counters"),
            summary="A starter worksheet for equivalent fractions.",
            learning_objectives=("Represent equivalent fractions with simple models.",),
            curriculum_references=("Local primary mathematics: fractions",),
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
            self.assertEqual(pack.duration_minutes, 30)
            self.assertEqual(pack.prerequisites, ("Count equal parts in a shape.",))
            self.assertEqual(pack.materials, ("Fraction strips", "Counters"))
            self.assertEqual(pack.learning_objectives, ("Represent equivalent fractions with simple models.",))
            self.assertEqual(pack.curriculum_references, ("Local primary mathematics: fractions",))
            self.assertEqual(len(pack.items), 3)
            self.assertEqual([item.difficulty for item in pack.items], ["foundation", "core", "extension"])
            self.assertTrue(result.ok)
            self.assertEqual(result.warnings, ())

    def test_scaffold_csv_creates_valid_resource(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "resource.csv"

            scaffold_resource(self.spec, path, "csv")
            pack = load_resource(path)

            self.assertEqual(pack.skills, ("fractions", "equivalent fractions"))
            self.assertEqual(pack.duration_minutes, 30)
            self.assertEqual(pack.prerequisites, ("Count equal parts in a shape.",))
            self.assertEqual(pack.materials, ("Fraction strips", "Counters"))
            self.assertEqual(pack.learning_objectives, ("Represent equivalent fractions with simple models.",))
            self.assertEqual(pack.curriculum_references, ("Local primary mathematics: fractions",))
            self.assertEqual(pack.items[0].item_type, "concept-check")
            self.assertEqual([item.difficulty for item in pack.items], ["foundation", "core", "extension"])

    def test_scaffold_yaml_creates_valid_resource(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "resource.yaml"

            scaffold_resource(self.spec, path, "yaml")
            pack = load_resource(path)
            result = validate_resource(path)

            self.assertIn("title: Primary Fractions Starter", path.read_text(encoding="utf-8"))
            self.assertEqual(pack.skills, ("fractions", "equivalent fractions"))
            self.assertEqual(pack.duration_minutes, 30)
            self.assertEqual(pack.prerequisites, ("Count equal parts in a shape.",))
            self.assertEqual(pack.materials, ("Fraction strips", "Counters"))
            self.assertEqual(pack.learning_objectives, ("Represent equivalent fractions with simple models.",))
            self.assertEqual(pack.curriculum_references, ("Local primary mathematics: fractions",))
            self.assertEqual(pack.items[0].item_type, "concept-check")
            self.assertEqual([item.difficulty for item in pack.items], ["foundation", "core", "extension"])
            self.assertTrue(result.ok)
            self.assertEqual(result.warnings, ())

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
