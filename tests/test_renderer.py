import unittest

from exam_materials_studio.models import pack_from_dict
from exam_materials_studio.renderer import (
    render_answer_key_html,
    render_answer_key_markdown,
    render_catalog_html,
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
                "resource_type": "worksheet",
                "education_system": "Cambridge International",
                "exam_board": "Cambridge",
                "course": "0478 Computer Science",
                "skills": ["truth tables"],
                "items": [
                    {
                        "prompt": "A AND B where A = 1 and B = 0.",
                        "answer": "0",
                        "explanation": "Both inputs must be 1.",
                    }
                ],
            }
        )

    def test_pack_markdown_contains_question_not_answer(self):
        markdown = render_pack_markdown(self.pack)

        self.assertIn("## Learning Objectives", markdown)
        self.assertIn("Build truth tables for common logic gates.", markdown)
        self.assertIn("A AND B", markdown)
        self.assertNotIn("Both inputs must be 1.", markdown)

    def test_answer_key_contains_explanation(self):
        markdown = render_answer_key_markdown(self.pack)

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
        self.assertIn("**Skills:** truth tables", markdown)
        self.assertIn("[Resource](boolean-logic.md)", markdown)
        self.assertIn("[Answer key](boolean-logic-answer-key.md)", markdown)

    def test_catalog_respects_requested_formats(self):
        html = render_catalog_html([self.pack], formats={"markdown"})

        self.assertIn("boolean-logic.md", html)
        self.assertNotIn("boolean-logic.html", html)

    def test_resource_html_contains_metadata_without_answer(self):
        html = render_pack_html(self.pack)

        self.assertIn("Learning Objectives", html)
        self.assertIn("Build truth tables for common logic gates.", html)
        self.assertIn("Cambridge International", html)
        self.assertIn("A AND B", html)
        self.assertNotIn("Both inputs must be 1.", html)

    def test_answer_key_html_contains_explanation(self):
        html = render_answer_key_html(self.pack)

        self.assertIn("Answer 1", html)
        self.assertIn("Both inputs must be 1.", html)


if __name__ == "__main__":
    unittest.main()
