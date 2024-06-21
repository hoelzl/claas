import xml.etree.ElementTree as ET  # noqa

from docx import Document
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Pt

from claas.curriculum_converter import CurriculumConverter


class TableWordConverter(CurriculumConverter):
    def __init__(self, tree: ET.ElementTree):
        super().__init__(tree)
        self._current_table = None
        self._need_new_table = True
        self._last_output = None

    def start_output(self):
        return Document()

    def add_module(self, output, title, description):
        self._create_new_table(output)

    def add_topic(self, output, contents, duration, methodik, material):
        if self._need_new_table:
            self._create_new_table(output)
            self._need_new_table = False
        self._current_table.add_row()
        row_cells = self._current_table.rows[-1].cells
        row_cells[0].text = contents
        row_cells[1].text = str(duration)
        row_cells[2].text = methodik
        row_cells[3].text = material
        self._last_output = "row"

    def add_remark(self, output, bemerkung):
        if self._last_output == "row":
            output.add_paragraph()  # Add space between tables
        # Add the remark as a bold paragraph
        p = output.add_paragraph()
        run = p.add_run(bemerkung)
        run.bold = True
        p.alignment = WD_PARAGRAPH_ALIGNMENT.LEFT
        self._need_new_table = True
        self._last_output = "remark"

    def _create_new_table(self, output):
        self._current_table = output.add_table(rows=1, cols=4)
        self._current_table.style = "Table Grid"
        hdr_cells = self._current_table.rows[0].cells
        hdr_cells[0].text = "Inhalt"
        hdr_cells[1].text = "UE"
        hdr_cells[2].text = "Methodik/Didaktik"
        hdr_cells[3].text = "Materialien"
        self._set_header_style(hdr_cells)
        self._need_new_table = False

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

    def finalize_output(self, output):
        return output
