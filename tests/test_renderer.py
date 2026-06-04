import json
import unittest

from exam_materials_studio.models import pack_from_dict
from exam_materials_studio.renderer import (
    render_answer_key_html,
    render_answer_key_markdown,
    render_catalog_html,
    render_catalog_json,
    render_catalog_markdown,
    render_pack_html,
    render_pack_markdown,
)


class RendererTests(unittest.TestCase):
    def setUp(self):
        self.pack = pack_from_dict(
            {
                "title": "Boolean Logic",
                "slug": "boolean-logic",
                "subject": "Computer Science",
                "level": "IGCSE",
                "summary": "Practice logic gates.",
                "learning_objectives": [
                    "Build truth tables for common logic gates.",
                    "Explain Boolean outputs from binary inputs.",
                ],
                "curriculum_references": ["Cambridge 0478 4.1"],
                "resource_type": "worksheet",
                "education_system": "Cambridge International",
                "exam_board": "Cambridge",
                "course": "0478 Computer Science",
                "duration_minutes": 40,
                "prerequisites": ["Binary inputs", "Truth-table columns"],
                "skills": ["truth tables"],
                "items": [
                    {
                        "prompt": "A AND B where A = 1 and B = 0.",
                        "answer": "0",
                        "explanation": "Both inputs must be 1.",
                        "difficulty": "core",
                    }
                ],
            }
        )

    def test_pack_markdown_contains_question_not_answer(self):
        markdown = render_pack_markdown(self.pack)

        self.assertIn("## Learning Objectives", markdown)
        self.assertIn("Build truth tables for common logic gates.", markdown)
        self.assertIn("## Curriculum References", markdown)
        self.assertIn("Cambridge 0478 4.1", markdown)
        self.assertIn("## Prerequisites", markdown)
        self.assertIn("- Binary inputs", markdown)
        self.assertIn("**Estimated time:** 40 minutes", markdown)
        self.assertIn("**Difficulty:** core", markdown)
        self.assertIn("A AND B", markdown)
        self.assertNotIn("Both inputs must be 1.", markdown)

    def test_answer_key_contains_explanation(self):
        markdown = render_answer_key_markdown(self.pack)

        self.assertIn("**Estimated time:** 40 minutes", markdown)
        self.assertIn("## Prerequisites", markdown)
        self.assertIn("**Difficulty:** core", markdown)
        self.assertIn("0", markdown)
        self.assertIn("Both inputs must be 1.", markdown)

    def test_catalog_links_generated_outputs(self):
        html = render_catalog_html([self.pack])

        self.assertIn("boolean-logic.md", html)
        self.assertIn("boolean-logic.html", html)
        self.assertIn("boolean-logic-answer-key.md", html)
        self.assertIn("boolean-logic-answer-key.html", html)
        self.assertIn("Cambridge International / Cambridge / 0478 Computer Science", html)

    def test_catalog_markdown_links_generated_markdown_outputs(self):
        markdown = render_catalog_markdown([self.pack])

        self.assertIn("# Exam Materials Catalog", markdown)
        self.assertIn("## Boolean Logic", markdown)
        self.assertIn("Practice logic gates.", markdown)
        self.assertIn("**Type:** worksheet", markdown)
        self.assertIn("**Subject:** Computer Science", markdown)
        self.assertIn("**Level:** IGCSE", markdown)
        self.assertIn("**Track:** Cambridge International / Cambridge / 0478 Computer Science", markdown)
        self.assertIn("**Prerequisites:** Binary inputs, Truth-table columns", markdown)
        self.assertIn("**Skills:** truth tables", markdown)
        self.assertIn("[Resource](boolean-logic.md)", markdown)
        self.assertIn("[Answer key](boolean-logic-answer-key.md)", markdown)

    def test_catalog_json_includes_machine_readable_resource_metadata(self):
        catalog = json.loads(render_catalog_json([self.pack], formats={"markdown", "html"}))

        self.assertEqual(catalog["schema_version"], 1)
        self.assertEqual(catalog["resource_count"], 1)
        resource = catalog["resources"][0]
        self.assertEqual(resource["title"], "Boolean Logic")
        self.assertEqual(resource["slug"], "boolean-logic")
        self.assertEqual(resource["subject"], "Computer Science")
        self.assertEqual(resource["level"], "IGCSE")
        self.assertEqual(resource["resource_type"], "worksheet")
        self.assertEqual(resource["education_system"], "Cambridge International")
        self.assertEqual(resource["exam_board"], "Cambridge")
        self.assertEqual(resource["course"], "0478 Computer Science")
        self.assertEqual(resource["duration_minutes"], 40)
        self.assertEqual(resource["prerequisites"], ["Binary inputs", "Truth-table columns"])
        self.assertEqual(resource["skills"], ["truth tables"])
        self.assertEqual(resource["learning_objectives"], ["Build truth tables for common logic gates.", "Explain Boolean outputs from binary inputs."])
        self.assertEqual(resource["curriculum_references"], ["Cambridge 0478 4.1"])
        self.assertEqual(resource["item_count"], 1)
        self.assertEqual(resource["difficulty_counts"], {"core": 1})
        self.assertEqual(resource["files"]["markdown"], "boolean-logic.md")
        self.assertEqual(resource["files"]["answer_key_markdown"], "boolean-logic-answer-key.md")
        self.assertEqual(resource["files"]["html"], "boolean-logic.html")
        self.assertEqual(resource["files"]["answer_key_html"], "boolean-logic-answer-key.html")

    def test_catalog_json_orders_difficulty_counts_by_learning_progression(self):
        pack = pack_from_dict(
            {
                "title": "Progression",
                "slug": "progression",
                "subject": "Science",
                "level": "Primary",
                "summary": "Practice ordered difficulty metadata.",
                "skills": ["progression"],
                "items": [
                    {"prompt": "Starter", "answer": "A", "difficulty": "extension"},
                    {"prompt": "Core", "answer": "B", "difficulty": "core"},
                    {"prompt": "Foundation", "answer": "C", "difficulty": "foundation"},
                ],
            }
        )

        catalog = json.loads(render_catalog_json([pack], formats={"markdown"}))

        self.assertEqual(
            list(catalog["resources"][0]["difficulty_counts"]),
            ["foundation", "core", "extension"],
        )

    def test_catalog_respects_requested_formats(self):
        html = render_catalog_html([self.pack], formats={"markdown"})

        self.assertIn("boolean-logic.md", html)
        self.assertNotIn("boolean-logic.html", html)

    def test_resource_html_contains_metadata_without_answer(self):
        html = render_pack_html(self.pack)

        self.assertIn("Learning Objectives", html)
        self.assertIn("Build truth tables for common logic gates.", html)
        self.assertIn("Curriculum References", html)
        self.assertIn("Cambridge 0478 4.1", html)
        self.assertIn("Prerequisites", html)
        self.assertIn("Binary inputs", html)
        self.assertIn("<strong>Estimated time:</strong> 40 minutes", html)
        self.assertIn("<strong>Difficulty:</strong> core", html)
        self.assertIn("Cambridge International", html)
        self.assertIn("A AND B", html)
        self.assertNotIn("Both inputs must be 1.", html)

    def test_answer_key_html_contains_explanation(self):
        html = render_answer_key_html(self.pack)

        self.assertIn("Answer 1", html)
        self.assertIn("<strong>Difficulty:</strong> core", html)
        self.assertIn("Both inputs must be 1.", html)


if __name__ == "__main__":
    unittest.main()
