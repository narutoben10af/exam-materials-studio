import json
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path

from exam_materials_studio.cli import build_packs


class CliTests(unittest.TestCase):
    def test_build_packs_writes_markdown_and_html_outputs(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            pack_path = root / "resource.json"
            output_dir = root / "generated"
            pack_path.write_text(
                json.dumps(
                    {
                        "title": "Primary Fractions Worksheet",
                        "slug": "primary-fractions-worksheet",
                        "subject": "Mathematics",
                        "level": "Primary",
                        "resource_type": "worksheet",
                        "education_system": "General primary",
                        "summary": "A short worksheet for equivalent fractions.",
                        "skills": ["equivalent fractions"],
                        "items": [{"prompt": "Write one half as quarters.", "answer": "2/4"}],
                    }
                ),
                encoding="utf-8",
            )

            with redirect_stdout(StringIO()):
                result = build_packs([pack_path], output_dir, {"markdown", "html"})

            self.assertEqual(result, 0)
            self.assertTrue((output_dir / "primary-fractions-worksheet.md").exists())
            self.assertTrue((output_dir / "primary-fractions-worksheet.html").exists())
            self.assertTrue((output_dir / "primary-fractions-worksheet-answer-key.md").exists())
            self.assertTrue((output_dir / "primary-fractions-worksheet-answer-key.html").exists())
            self.assertTrue((output_dir / "index.html").exists())


if __name__ == "__main__":
    unittest.main()
