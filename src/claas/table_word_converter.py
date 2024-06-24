import xml.etree.ElementTree as ET  # noqa

from docx import Document
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt

from claas.curriculum_converter import CurriculumConverter


class TableWordConverter(CurriculumConverter):
    def __init__(self, tree: ET.ElementTree):
        super().__init__(tree)
        self._current_table = None
        self._current_table_total_duration = 0
        self._need_new_table = True

    def start_output(self, title: str) -> Document:
        document = Document()

        # Set page size to A4
        section = document.sections[0]
        section.page_height = Cm(29.7)  # A4 height in cm
        section.page_width = Cm(21.0)  # A4 width in cm

        # Set margins
        section.left_margin = Cm(2.0)
        section.right_margin = Cm(2.0)
        section.top_margin = Cm(2.0)
        section.bottom_margin = Cm(2.0)

        document.add_heading(title, level=1)
        return document

    def finalize_output(self, output) -> Document:
        if self._current_table:
            self._add_table_footer()
        return output

    def start_module(self, output, title: str, description: str):
        if self._current_table:
            self._add_table_footer()
            output.add_page_break()

        output.add_heading(title, level=2)
        if description:
            output.add_paragraph(description)

        self._need_new_table = True

    def add_topic(
        self, output, contents: str, duration: str, methodik: str, material: str
    ):
        if self._need_new_table or self._current_table is None:
            self._create_new_table(output)
            self._need_new_table = False
        self._current_table_total_duration += int(duration)
        self._current_table.add_row()
        row_cells = self._current_table.rows[-1].cells
        row_cells[0].text = contents
        row_cells[1].text = str(duration)
        row_cells[1].paragraphs[0].alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
        row_cells[2].text = methodik
        row_cells[3].text = material
        self._set_cell_margins(row_cells)

    def add_remark(self, output, bemerkung: str):
        if self._current_table:
            self._add_table_footer()
            output.add_paragraph()  # Add space between tables
        # Add the remark as a bold paragraph
        p = output.add_paragraph()
        run = p.add_run(bemerkung)
        run.bold = True
        p.alignment = WD_PARAGRAPH_ALIGNMENT.LEFT
        self._need_new_table = True

    def save(self, output_path):
        doc = self.convert()
        doc.save(output_path)

    def _create_new_table(self, output):
        self._current_table = output.add_table(rows=1, cols=4)
        self._current_table.style = "Table Grid"
        hdr_cells = self._current_table.rows[0].cells
        hdr_cells[0].text = "Inhalt"
        hdr_cells[0].width = Cm(18)
        hdr_cells[1].text = "UE"
        hdr_cells[2].text = "Methodik/Didaktik"
        hdr_cells[2].width = Cm(5)
        hdr_cells[3].text = "Materialien"
        hdr_cells[3].width = Cm(8)
        self._set_header_style(hdr_cells)
        self._set_cell_margins(hdr_cells)
        self._need_new_table = False
        self._current_table_total_duration = 0

    def _add_table_footer(self):
        # Write a table footer with the total duration
        self._current_table.add_row()
        row_cells = self._current_table.rows[-1].cells
        row_cells[0].text = "Summe:"
        row_cells[1].text = str(self._current_table_total_duration)
        for i in range(2, 4):
            row_cells[i].text = ""
        self._set_footer_style(row_cells)
        row_cells[0].paragraphs[0].alignment = WD_PARAGRAPH_ALIGNMENT.RIGHT
        self._set_cell_margins(row_cells)
        self._current_table = None

    @staticmethod
    def _set_header_style(cells):
        for cell in cells:
            cell_paragraph = cell.paragraphs[0]
            cell_paragraph.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
            run = cell_paragraph.runs[0]
            run.bold = True
            run.font.size = Pt(12)
            cell_shading = OxmlElement("w:shd")
            cell_shading.set(qn("w:fill"), "D9D9D9")  # Light grey background
            cell._element.get_or_add_tcPr().append(cell_shading)  # noqa

    @staticmethod
    def _set_footer_style(cells):
        for cell in cells:
            cell_paragraph = cell.paragraphs[0]
            cell_paragraph.alignment = (
                WD_PARAGRAPH_ALIGNMENT.RIGHT
                if cell.text == "Summe:"
                else WD_PARAGRAPH_ALIGNMENT.CENTER
            )
            run = cell_paragraph.runs[0]
            run.bold = False
            run.font.size = Pt(11)
            cell_shading = OxmlElement("w:shd")
            cell_shading.set(qn("w:fill"), "D9D9D9")  # Light grey background
            cell._element.get_or_add_tcPr().append(cell_shading)  # noqa

    @staticmethod
    def _set_cell_margins(cells, top=100, start=100, bottom=100, end=100):
        for cell in cells:
            tc = cell._element
            tcPr = tc.get_or_add_tcPr()
            tcMar = OxmlElement("w:tcMar")
            for margin, value in [
                ("top", top),
                ("start", start),
                ("bottom", bottom),
                ("end", end),
            ]:
                node = OxmlElement(f"w:{margin}")
                node.set(qn("w:w"), str(value))
                node.set(qn("w:type"), "dxa")
                tcMar.append(node)
            tcPr.append(tcMar)
