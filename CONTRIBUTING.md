# Contributing

Contributions are welcome when they improve the reusable education-materials
workflow.

Good first contributions include:

- New sample packs using public-domain or original questions.
- Better validation messages.
- Export improvements.
- Documentation for school or tutoring-centre workflows.

Please avoid committing:

- Student data.
- Customer or prospect lists.
- Paid pack content that you do not want to release under the MIT license.
- Copyrighted past-paper questions copied from exam boards.

Before opening a pull request, run:

```bash
python3 -m unittest discover
python3 -m exam_materials_studio build examples/igcse_computer_science_boolean_logic.json --out generated
```

