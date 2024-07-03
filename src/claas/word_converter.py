from docx import Document

from claas.curriculum_converter import CurriculumConverter


class WordConverter(CurriculumConverter):
    def start_output(self, title):
        document = Document()
        document.add_heading(title, level=1)
        return document

    def start_module(self, output, title: str, description: str, total_time: int):
        if self.include_time and total_time:
            output.add_heading(f"{title} ({total_time} UE)", level=2)
        else:
            output.add_heading(title, level=2)
        if description:
            output.add_paragraph(description)

    def add_topic(
        self, output, contents: str, duration: str, method: str, material: str
    ):
        if self.include_time and duration:
            output.add_paragraph(f"{contents} ({duration} UE)", style="List Number")
        else:
            output.add_paragraph(contents, style="List Number")

    def add_section(self, output, text: str, week_time: int = None):
        if self.include_time and week_time:
            output.add_heading(f"{text} ({week_time} UE)", level=3)
        else:
            output.add_heading(text, level=3)

    def finalize_output(self, output):
        return output

    def save(self, output_path):
        doc = self.convert()
        doc.save(output_path)
