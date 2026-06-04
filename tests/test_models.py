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
                "duration_minutes": "45",
                "prerequisites": ["Binary inputs", "Truth-table basics"],
                "materials": ["Mini whiteboards", "Logic-gate reference sheet"],
                "delivery_modes": ["classroom", "self-study"],
                "skills": ["logic"],
                "items": [
                    {
                        "prompt": "Question?",
                        "answer": "Answer.",
                        "difficulty": "Core",
                        "marks": "2",
                        "command_word": "Explain",
                        "phase": "Guided Practice",
                        "time_minutes": "7",
                        "standards": [
                            "Cambridge 0478 4.1.1",
                            "Cambridge 0478 4.1.2",
                            " ",
                        ],
                        "rubric": [
                            "1 mark for identifying the output.",
                            "1 mark for explaining the gate rule.",
                            " ",
                        ],
                    }
                ],
            }
        )

        self.assertEqual(pack.slug, "sample-pack")
        self.assertEqual(pack.resource_type, "worksheet")
        self.assertEqual(pack.education_system, "Cambridge International")
        self.assertEqual(pack.exam_board, "Cambridge")
        self.assertEqual(pack.course, "0478 Computer Science")
        self.assertEqual(pack.duration_minutes, 45)
        self.assertEqual(pack.prerequisites, ("Binary inputs", "Truth-table basics"))
        self.assertEqual(pack.materials, ("Mini whiteboards", "Logic-gate reference sheet"))
        self.assertEqual(pack.delivery_modes, ("classroom", "self-study"))
        self.assertEqual(
            pack.learning_objectives,
            (
                "Understand how logic gates process binary inputs.",
                "Apply truth tables to simple Boolean expressions.",
            ),
        )
        self.assertEqual(pack.curriculum_references, ("Cambridge 0478 4.1.1", "Cambridge 0478 4.1.2"))
        self.assertEqual(pack.items[0].difficulty, "core")
        self.assertEqual(pack.items[0].marks, 2)
        self.assertEqual(pack.items[0].command_word, "explain")
        self.assertEqual(pack.items[0].phase, "guided-practice")
        self.assertEqual(pack.items[0].time_minutes, 7)
        self.assertEqual(pack.items[0].standards, ("Cambridge 0478 4.1.1", "Cambridge 0478 4.1.2"))
        self.assertEqual(
            pack.items[0].rubric,
            ("1 mark for identifying the output.", "1 mark for explaining the gate rule."),
        )
        self.assertEqual(len(pack.items), 1)

    def test_invalid_duration_is_rejected(self):
        with self.assertRaisesRegex(PackValidationError, "duration_minutes must be a positive integer"):
            pack_from_dict(
                {
                    "title": "Sample",
                    "slug": "sample-pack",
                    "subject": "Computer Science",
                    "level": "IGCSE",
                    "summary": "A sample pack.",
                    "skills": ["logic"],
                    "duration_minutes": "soon",
                    "items": [{"prompt": "Question?", "answer": "Answer."}],
                }
            )

        with self.assertRaisesRegex(PackValidationError, "duration_minutes must be a positive integer"):
            pack_from_dict(
                {
                    "title": "Sample",
                    "slug": "sample-pack",
                    "subject": "Computer Science",
                    "level": "IGCSE",
                    "summary": "A sample pack.",
                    "skills": ["logic"],
                    "duration_minutes": 0,
                    "items": [{"prompt": "Question?", "answer": "Answer."}],
                }
            )

    def test_prerequisites_must_be_a_list_when_provided(self):
        with self.assertRaisesRegex(PackValidationError, "prerequisites must be a list"):
            pack_from_dict(
                {
                    "title": "Sample",
                    "slug": "sample-pack",
                    "subject": "Computer Science",
                    "level": "IGCSE",
                    "summary": "A sample pack.",
                    "skills": ["logic"],
                    "prerequisites": "truth tables",
                    "items": [{"prompt": "Question?", "answer": "Answer."}],
                }
            )

    def test_materials_must_be_a_list_when_provided(self):
        with self.assertRaisesRegex(PackValidationError, "materials must be a list"):
            pack_from_dict(
                {
                    "title": "Sample",
                    "slug": "sample-pack",
                    "subject": "Science",
                    "level": "Primary",
                    "summary": "A sample pack.",
                    "skills": ["materials"],
                    "materials": "scissors",
                    "items": [{"prompt": "Question?", "answer": "Answer."}],
                }
            )

    def test_delivery_modes_must_be_a_list_when_provided(self):
        with self.assertRaisesRegex(PackValidationError, "delivery_modes must be a list"):
            pack_from_dict(
                {
                    "title": "Sample",
                    "slug": "sample-pack",
                    "subject": "Science",
                    "level": "Primary",
                    "summary": "A sample pack.",
                    "skills": ["materials"],
                    "delivery_modes": "classroom",
                    "items": [{"prompt": "Question?", "answer": "Answer."}],
                }
            )

    def test_invalid_item_difficulty_is_rejected(self):
        with self.assertRaisesRegex(PackValidationError, "item 1 difficulty"):
            pack_from_dict(
                {
                    "title": "Sample",
                    "slug": "sample-pack",
                    "subject": "Computer Science",
                    "level": "IGCSE",
                    "summary": "A sample pack.",
                    "skills": ["logic"],
                    "items": [{"prompt": "Question?", "answer": "Answer.", "difficulty": "impossible"}],
                }
            )

    def test_invalid_item_marks_are_rejected(self):
        for marks in ("two", 0):
            with self.subTest(marks=marks):
                with self.assertRaisesRegex(PackValidationError, "item 1 marks must be a positive integer"):
                    pack_from_dict(
                        {
                            "title": "Sample",
                            "slug": "sample-pack",
                            "subject": "Computer Science",
                            "level": "IGCSE",
                            "summary": "A sample pack.",
                            "skills": ["logic"],
                            "items": [{"prompt": "Question?", "answer": "Answer.", "marks": marks}],
                        }
                    )

    def test_invalid_item_rubric_is_rejected(self):
        with self.assertRaisesRegex(PackValidationError, "item 1 rubric must be a list"):
            pack_from_dict(
                {
                    "title": "Sample",
                    "slug": "sample-pack",
                    "subject": "Computer Science",
                    "level": "IGCSE",
                    "summary": "A sample pack.",
                    "skills": ["logic"],
                    "items": [{"prompt": "Question?", "answer": "Answer.", "rubric": "two marks"}],
                }
            )

    def test_invalid_item_phase_is_rejected(self):
        with self.assertRaisesRegex(PackValidationError, "item 1 phase must be text"):
            pack_from_dict(
                {
                    "title": "Sample",
                    "slug": "sample-pack",
                    "subject": "Computer Science",
                    "level": "IGCSE",
                    "summary": "A sample pack.",
                    "skills": ["logic"],
                    "items": [{"prompt": "Question?", "answer": "Answer.", "phase": ["warm-up"]}],
                }
            )

    def test_invalid_item_time_minutes_are_rejected(self):
        for time_minutes in ("soon", 0):
            with self.subTest(time_minutes=time_minutes):
                with self.assertRaisesRegex(PackValidationError, "item 1 time_minutes must be a positive integer"):
                    pack_from_dict(
                        {
                            "title": "Sample",
                            "slug": "sample-pack",
                            "subject": "Computer Science",
                            "level": "IGCSE",
                            "summary": "A sample pack.",
                            "skills": ["logic"],
                            "items": [{"prompt": "Question?", "answer": "Answer.", "time_minutes": time_minutes}],
                        }
                    )

    def test_invalid_item_standards_are_rejected(self):
        with self.assertRaisesRegex(PackValidationError, "item 1 standards must be a list"):
            pack_from_dict(
                {
                    "title": "Sample",
                    "slug": "sample-pack",
                    "subject": "Computer Science",
                    "level": "IGCSE",
                    "summary": "A sample pack.",
                    "skills": ["logic"],
                    "items": [{"prompt": "Question?", "answer": "Answer.", "standards": "Cambridge 0478"}],
                }
            )

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
