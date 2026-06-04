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
materials:
  - Fraction strips
  - Counters
delivery_modes:
  - classroom
  - tutoring
learning_objectives:
  - Represent one half using quarters.
curriculum_references:
  - Local Grade 4 Fractions
skills:
  - equivalent fractions
items:
  - type: question
    phase: Guided Practice
    time_minutes: 8
    standards:
      - Local Grade 4 Fractions 1.2
      - School Scheme Fractions A
    difficulty: foundation
    marks: 2
    command_word: write
    rubric:
      - 1 mark for writing 2/4.
      - 1 mark for showing that quarters are equal parts.
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
            self.assertEqual(pack.materials, ("Fraction strips", "Counters"))
            self.assertEqual(pack.delivery_modes, ("classroom", "tutoring"))
            self.assertEqual(pack.skills, ("equivalent fractions",))
            self.assertEqual(pack.items[0].phase, "guided-practice")
            self.assertEqual(pack.items[0].time_minutes, 8)
            self.assertEqual(pack.items[0].standards, ("Local Grade 4 Fractions 1.2", "School Scheme Fractions A"))
            self.assertEqual(pack.items[0].difficulty, "foundation")
            self.assertEqual(pack.items[0].marks, 2)
            self.assertEqual(pack.items[0].command_word, "write")
            self.assertEqual(
                pack.items[0].rubric,
                ("1 mark for writing 2/4.", "1 mark for showing that quarters are equal parts."),
            )

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
                        "title,slug,subject,level,resource_type,education_system,exam_board,course,duration_minutes,prerequisites,materials,delivery_modes,summary,skills,learning_objectives,curriculum_references,type,phase,time_minutes,standards,difficulty,marks,command_word,rubric,prompt,answer,explanation",
                        "Primary Science,primary-science,Science,Primary,lesson-resource,General primary,,Materials,25,Name common classroom objects,Wood sample;Metal spoon;Plastic bottle,classroom;tutoring,A materials lesson,classification;properties,Classify everyday materials;Link properties to uses,National Curriculum KS1 Materials,activity,warm up,5,National Curriculum KS1 Materials 1a,foundation,1,sort,1 mark for grouping by material,Sort wood and metal objects.,Wood objects and metal objects are grouped separately.,Learners classify materials by observable properties.",
                        "Primary Science,primary-science,Science,Primary,lesson-resource,General primary,,Materials,25,Name common classroom objects,Wood sample;Metal spoon;Plastic bottle,classroom;tutoring,A materials lesson,classification;properties,Classify everyday materials;Link properties to uses,National Curriculum KS1 Materials,question,guided practice,10,National Curriculum KS1 Materials 1b;School Scheme Materials B,core,2,name,1 mark for naming a valid property;1 mark for linking property to metal,Name one property of metal.,Metal is usually strong.,This checks whether learners can connect materials to properties.",
                        "Primary Science,primary-science,Science,Primary,lesson-resource,General primary,,Materials,25,Name common classroom objects,Wood sample;Metal spoon;Plastic bottle,classroom;tutoring,A materials lesson,classification;properties,Classify everyday materials;Link properties to uses,National Curriculum KS1 Materials,discussion,extension,10,National Curriculum KS1 Materials 1c,extension,3,explain,1 mark for transparency;1 mark for function;1 mark for clear explanation,Why use glass for windows?,Glass is transparent.,The learner should connect transparency to the function of a window.",
                    ]
                ),
                encoding="utf-8",
            )

            pack = load_resource(path)

            self.assertEqual(pack.title, "Primary Science")
            self.assertEqual(pack.slug, "primary-science")
            self.assertEqual(pack.duration_minutes, 25)
            self.assertEqual(pack.prerequisites, ("Name common classroom objects",))
            self.assertEqual(pack.materials, ("Wood sample", "Metal spoon", "Plastic bottle"))
            self.assertEqual(pack.delivery_modes, ("classroom", "tutoring"))
            self.assertEqual(pack.skills, ("classification", "properties"))
            self.assertEqual(
                pack.learning_objectives,
                ("Classify everyday materials", "Link properties to uses"),
            )
            self.assertEqual(pack.curriculum_references, ("National Curriculum KS1 Materials",))
            self.assertEqual(len(pack.items), 3)
            self.assertEqual(pack.items[0].item_type, "activity")
            self.assertEqual([item.difficulty for item in pack.items], ["foundation", "core", "extension"])
            self.assertEqual([item.phase for item in pack.items], ["warm-up", "guided-practice", "extension"])
            self.assertEqual([item.time_minutes for item in pack.items], [5, 10, 10])
            self.assertEqual(
                [item.standards for item in pack.items],
                [
                    ("National Curriculum KS1 Materials 1a",),
                    ("National Curriculum KS1 Materials 1b", "School Scheme Materials B"),
                    ("National Curriculum KS1 Materials 1c",),
                ],
            )
            self.assertEqual([item.marks for item in pack.items], [1, 2, 3])
            self.assertEqual([item.command_word for item in pack.items], ["sort", "name", "explain"])
            self.assertEqual(pack.items[1].rubric, ("1 mark for naming a valid property", "1 mark for linking property to metal"))

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
