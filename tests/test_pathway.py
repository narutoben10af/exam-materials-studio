import unittest

from exam_materials_studio.models import pack_from_dict
from exam_materials_studio.pathway import render_pathway_markdown


class PathwayTests(unittest.TestCase):
    def test_renders_ordered_course_pathway_with_unsequenced_resources(self):
        packs = [
            pack_from_dict(
                {
                    "title": "Equivalent Fractions Practice",
                    "slug": "equivalent-fractions-practice",
                    "subject": "Mathematics",
                    "level": "Primary",
                    "resource_type": "worksheet",
                    "education_system": "General primary",
                    "course": "Fractions",
                    "unit": "Equivalent fractions",
                    "sequence_order": 2,
                    "duration_minutes": 25,
                    "delivery_modes": ["classroom", "tutoring"],
                    "prerequisites": ["Recognise halves and quarters"],
                    "learning_objectives": ["Compare equivalent fraction models"],
                    "summary": "Practice equivalent fractions.",
                    "skills": ["fractions"],
                    "items": [{"prompt": "Write one half as quarters.", "answer": "2/4"}],
                }
            ),
            pack_from_dict(
                {
                    "title": "Fraction Unit Reflection",
                    "slug": "fraction-unit-reflection",
                    "subject": "Mathematics",
                    "level": "Primary",
                    "resource_type": "reflection",
                    "education_system": "General primary",
                    "course": "Fractions",
                    "unit": "Equivalent fractions",
                    "duration_minutes": 10,
                    "delivery_modes": ["homework"],
                    "summary": "Reflect on equivalent fractions.",
                    "skills": ["reflection"],
                    "items": [{"prompt": "What helped you compare fractions?", "answer": "Models helped."}],
                }
            ),
            pack_from_dict(
                {
                    "title": "Fraction Models Warm-up",
                    "slug": "fraction-models-warm-up",
                    "subject": "Mathematics",
                    "level": "Primary",
                    "resource_type": "activity-sheet",
                    "education_system": "General primary",
                    "course": "Fractions",
                    "unit": "Equivalent fractions",
                    "sequence_order": 1,
                    "duration_minutes": 15,
                    "delivery_modes": ["classroom"],
                    "learning_objectives": ["Represent one half with simple diagrams"],
                    "summary": "Warm up fraction models.",
                    "skills": ["fractions"],
                    "items": [{"prompt": "Shade one half.", "answer": "Half the shape is shaded."}],
                }
            ),
        ]

        report = render_pathway_markdown(packs)

        self.assertIn("# Learning Pathway", report)
        self.assertIn("- Resources: 3", report)
        self.assertIn("- Sequenced resources: 2", report)
        self.assertIn("- Unsequenced resources: 1", report)
        self.assertIn("- Planned time: 50 minutes", report)
        self.assertIn("## Primary / Mathematics / Fractions", report)
        self.assertIn("### Unit: Equivalent fractions", report)
        self.assertIn(
            "| 1 | [Fraction Models Warm-up](fraction-models-warm-up.md) | activity-sheet | 15 min | classroom | Unspecified | Represent one half with simple diagrams | [Answer key](fraction-models-warm-up-answer-key.md) |",
            report,
        )
        self.assertIn(
            "| 2 | [Equivalent Fractions Practice](equivalent-fractions-practice.md) | worksheet | 25 min | classroom;tutoring | Recognise halves and quarters | Compare equivalent fraction models | [Answer key](equivalent-fractions-practice-answer-key.md) |",
            report,
        )
        self.assertIn(
            "| Unsequenced | [Fraction Unit Reflection](fraction-unit-reflection.md) | reflection | 10 min | homework | Unspecified | Unspecified | [Answer key](fraction-unit-reflection-answer-key.md) |",
            report,
        )
        self.assertLess(report.index("Fraction Models Warm-up"), report.index("Equivalent Fractions Practice"))
        self.assertLess(report.index("Equivalent Fractions Practice"), report.index("Fraction Unit Reflection"))


if __name__ == "__main__":
    unittest.main()
