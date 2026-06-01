import unittest

from exam_materials_studio.models import PackValidationError, pack_from_dict


class PackModelTests(unittest.TestCase):
    def test_valid_pack_loads(self):
        pack = pack_from_dict(
            {
                "title": "Sample",
                "slug": "sample-pack",
                "subject": "Computer Science",
                "level": "IGCSE",
                "summary": "A sample pack.",
                "learning_objectives": [
                    "Understand how logic gates process binary inputs.",
                    "Apply truth tables to simple Boolean expressions.",
                ],
                "curriculum_references": ["Cambridge 0478 4.1.1", "Cambridge 0478 4.1.2"],
                "resource_type": "worksheet",
                "education_system": "Cambridge International",
                "exam_board": "Cambridge",
                "course": "0478 Computer Science",
                "skills": ["logic"],
                "items": [{"prompt": "Question?", "answer": "Answer."}],
            }
        )

        self.assertEqual(pack.slug, "sample-pack")
        self.assertEqual(pack.resource_type, "worksheet")
        self.assertEqual(pack.education_system, "Cambridge International")
        self.assertEqual(pack.exam_board, "Cambridge")
        self.assertEqual(pack.course, "0478 Computer Science")
        self.assertEqual(
            pack.learning_objectives,
            (
                "Understand how logic gates process binary inputs.",
                "Apply truth tables to simple Boolean expressions.",
            ),
        )
        self.assertEqual(pack.curriculum_references, ("Cambridge 0478 4.1.1", "Cambridge 0478 4.1.2"))
        self.assertEqual(len(pack.items), 1)

    def test_invalid_slug_is_rejected(self):
        with self.assertRaises(PackValidationError):
            pack_from_dict(
                {
                    "title": "Sample",
                    "slug": "Bad Slug",
                    "subject": "Computer Science",
                    "level": "IGCSE",
                    "summary": "A sample pack.",
                    "skills": ["logic"],
                    "items": [{"prompt": "Question?", "answer": "Answer."}],
                }
            )

    def test_empty_skills_are_rejected(self):
        with self.assertRaises(PackValidationError):
            pack_from_dict(
                {
                    "title": "Sample",
                    "slug": "sample-pack",
                    "subject": "Early Years",
                    "level": "Preschool",
                    "summary": "A sample pack.",
                    "skills": [" "],
                    "items": [{"prompt": "Question?", "answer": "Answer."}],
                }
            )


if __name__ == "__main__":
    unittest.main()
