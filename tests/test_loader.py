import tempfile
import unittest
from pathlib import Path

from exam_materials_studio.loader import ResourceLoadError, load_resource


class LoaderTests(unittest.TestCase):
    def test_loads_csv_resource_rows_as_one_pack(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "primary_science.csv"
            path.write_text(
                "\n".join(
                    [
                        "title,slug,subject,level,resource_type,education_system,exam_board,course,summary,skills,type,prompt,answer,explanation",
                        "Primary Science,primary-science,Science,Primary,lesson-resource,General primary,,Materials,A materials lesson,classification;properties,activity,Sort wood and metal objects.,Wood objects and metal objects are grouped separately.,Learners classify materials by observable properties.",
                        "Primary Science,primary-science,Science,Primary,lesson-resource,General primary,,Materials,A materials lesson,classification;properties,question,Name one property of metal.,Metal is usually strong.,This checks whether learners can connect materials to properties.",
                        "Primary Science,primary-science,Science,Primary,lesson-resource,General primary,,Materials,A materials lesson,classification;properties,discussion,Why use glass for windows?,Glass is transparent.,The learner should connect transparency to the function of a window.",
                    ]
                ),
                encoding="utf-8",
            )

            pack = load_resource(path)

            self.assertEqual(pack.title, "Primary Science")
            self.assertEqual(pack.slug, "primary-science")
            self.assertEqual(pack.skills, ("classification", "properties"))
            self.assertEqual(len(pack.items), 3)
            self.assertEqual(pack.items[0].item_type, "activity")

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

