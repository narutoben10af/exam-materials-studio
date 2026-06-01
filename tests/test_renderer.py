import unittest

from exam_materials_studio.models import pack_from_dict
from exam_materials_studio.renderer import render_answer_key_markdown, render_catalog_html, render_pack_markdown


class RendererTests(unittest.TestCase):
    def setUp(self):
        self.pack = pack_from_dict(
            {
                "title": "Boolean Logic",
                "slug": "boolean-logic",
                "subject": "Computer Science",
                "level": "IGCSE",
                "summary": "Practice logic gates.",
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

        self.assertIn("A AND B", markdown)
        self.assertNotIn("Both inputs must be 1.", markdown)

    def test_answer_key_contains_explanation(self):
        markdown = render_answer_key_markdown(self.pack)

        self.assertIn("0", markdown)
        self.assertIn("Both inputs must be 1.", markdown)

    def test_catalog_links_generated_outputs(self):
        html = render_catalog_html([self.pack])

        self.assertIn("boolean-logic.md", html)
        self.assertIn("boolean-logic-answer-key.md", html)


if __name__ == "__main__":
    unittest.main()

