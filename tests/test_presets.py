import unittest

from exam_materials_studio.presets import PresetError, get_preset, render_presets_markdown


class PresetTests(unittest.TestCase):
    def test_get_preset_returns_common_education_system_defaults(self):
        preset = get_preset("ib-dp")

        self.assertEqual(preset.level, "IB")
        self.assertEqual(preset.resource_type, "study-guide")
        self.assertEqual(preset.education_system, "International Baccalaureate")
        self.assertEqual(preset.exam_board, "IB")

    def test_get_preset_rejects_unknown_name(self):
        with self.assertRaisesRegex(PresetError, "unknown preset: mystery"):
            get_preset("mystery")

    def test_render_presets_markdown_lists_level_range(self):
        report = render_presets_markdown()

        self.assertIn("| preschool | Preschool |", report)
        self.assertIn("| university | University |", report)
        self.assertIn("| cambridge-a-level | A Level |", report)


if __name__ == "__main__":
    unittest.main()
