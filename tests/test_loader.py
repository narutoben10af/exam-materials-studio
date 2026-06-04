import tempfile
import unittest
from pathlib import Path

from exam_materials_studio.loader import ResourceLoadError, load_resource


class LoaderTests(unittest.TestCase):
    def test_loads_yaml_resource(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "primary_fractions.yaml"
            path.write_text(
                """title: Primary Fractions YAML
slug: primary-fractions-yaml
subject: Mathematics
level: Primary
resource_type: worksheet
education_system: General primary
course: Fractions
duration_minutes: 30
summary: A YAML-authored fractions resource.
prerequisites:
  - Count equal parts in a shape.
learning_objectives:
  - Represent one half using quarters.
curriculum_references:
  - Local Grade 4 Fractions
skills:
  - equivalent fractions
items:
  - type: question
    difficulty: foundation
    prompt: Write one half as quarters.
    answer: 2/4
    explanation: Two quarters cover the same amount as one half.
""",
                encoding="utf-8",
            )

            pack = load_resource(path)

            self.assertEqual(pack.title, "Primary Fractions YAML")
            self.assertEqual(pack.slug, "primary-fractions-yaml")
            self.assertEqual(pack.duration_minutes, 30)
            self.assertEqual(pack.prerequisites, ("Count equal parts in a shape.",))
            self.assertEqual(pack.skills, ("equivalent fractions",))
            self.assertEqual(pack.items[0].difficulty, "foundation")

    def test_loads_yml_resource(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "primary_fractions.yml"
            path.write_text(
                """title: Primary Fractions YML
slug: primary-fractions-yml
subject: Mathematics
level: Primary
summary: A YML-authored fractions resource.
skills:
  - equivalent fractions
items:
  - prompt: Write two quarters in simplest form.
    answer: 1/2
""",
                encoding="utf-8",
            )

            pack = load_resource(path)

            self.assertEqual(pack.title, "Primary Fractions YML")
            self.assertEqual(pack.items[0].answer, "1/2")

    def test_loads_csv_resource_rows_as_one_pack(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "primary_science.csv"
            path.write_text(
                "\n".join(
                    [
                        "title,slug,subject,level,resource_type,education_system,exam_board,course,duration_minutes,prerequisites,summary,skills,learning_objectives,curriculum_references,type,difficulty,prompt,answer,explanation",
                        "Primary Science,primary-science,Science,Primary,lesson-resource,General primary,,Materials,25,Name common classroom objects,A materials lesson,classification;properties,Classify everyday materials;Link properties to uses,National Curriculum KS1 Materials,activity,foundation,Sort wood and metal objects.,Wood objects and metal objects are grouped separately.,Learners classify materials by observable properties.",
                        "Primary Science,primary-science,Science,Primary,lesson-resource,General primary,,Materials,25,Name common classroom objects,A materials lesson,classification;properties,Classify everyday materials;Link properties to uses,National Curriculum KS1 Materials,question,core,Name one property of metal.,Metal is usually strong.,This checks whether learners can connect materials to properties.",
                        "Primary Science,primary-science,Science,Primary,lesson-resource,General primary,,Materials,25,Name common classroom objects,A materials lesson,classification;properties,Classify everyday materials;Link properties to uses,National Curriculum KS1 Materials,discussion,extension,Why use glass for windows?,Glass is transparent.,The learner should connect transparency to the function of a window.",
                    ]
                ),
                encoding="utf-8",
            )

            pack = load_resource(path)

            self.assertEqual(pack.title, "Primary Science")
            self.assertEqual(pack.slug, "primary-science")
            self.assertEqual(pack.duration_minutes, 25)
            self.assertEqual(pack.prerequisites, ("Name common classroom objects",))
            self.assertEqual(pack.skills, ("classification", "properties"))
            self.assertEqual(
                pack.learning_objectives,
                ("Classify everyday materials", "Link properties to uses"),
            )
            self.assertEqual(pack.curriculum_references, ("National Curriculum KS1 Materials",))
            self.assertEqual(len(pack.items), 3)
            self.assertEqual(pack.items[0].item_type, "activity")
            self.assertEqual([item.difficulty for item in pack.items], ["foundation", "core", "extension"])

    def test_csv_requires_prompt_and_answer_per_row(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "broken.csv"
            path.write_text(
                "\n".join(
                    [
                        "title,slug,subject,level,summary,skills,prompt,answer",
                        "Broken,broken,Science,Primary,A broken CSV,classification,Question,",
                    ]
                ),
                encoding="utf-8",
            )

            with self.assertRaises(ResourceLoadError):
                load_resource(path)

    def test_rejects_unsupported_resource_extension(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "resource.txt"
            path.write_text("nope", encoding="utf-8")

            with self.assertRaises(ResourceLoadError):
                load_resource(path)


if __name__ == "__main__":
    unittest.main()
