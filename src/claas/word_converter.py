from docx import Document

from claas.curriculum_converter import CurriculumConverter


class WordConverter(CurriculumConverter):
    def start_output(self):
        return Document()

    def add_module(self, output, title, description):
        output.add_heading(title, level=1)
        if description is not None:
            output.add_paragraph(description.text)

    def add_topic(self, output, contents, duration, methodik, material):
        output.add_heading(f"Thema: {contents}", level=2)
        list_items = [
            f"Dauer: {duration} Einheiten",
            f"Methodik: {methodik}",
            f"Material: {material}",
        ]
        for item in list_items:
            output.add_paragraph(item, style="List Bullet")

    def add_remark(self, output, bemerkung):
        output.add_heading("Bemerkung", level=2)
        output.add_paragraph(bemerkung)

    def finalize_output(self, output):
        return output

    def save(self, output_path):
        document = self.convert()
        document.save(output_path)
