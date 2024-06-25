from claas.curriculum_converter import CurriculumConverter


class TableHtmlConverter(CurriculumConverter):
    def __init__(self, tree):
        super().__init__(tree)
        self._current_table = []
        self._current_table_total_duration = 0
        self._need_new_table = True

    def start_output(self, title) -> list[str]:
        return [
            "<html>",
            "<head>",
            f"<title>Lehrplan: {title}</title>",
            "<style>",
            "table { border-collapse: collapse; width: 100%; margin-bottom: 20px; }",
            "th, td { border: 1px solid black; padding: 8px; text-align: left; }",
            "th { background-color: #f2f2f2; }",
            ".center { text-align: center; }",
            ".right { text-align: right; }",
            "</style>",
            "</head>",
            "<body>",
            f"<h1>{title}</h1>",
        ]

    def finalize_output(self, output) -> str:
        if self._current_table:
            self._add_table_footer(output)
        output.append("</body>")
        output.append("</html>")
        return "\n".join(output)

    def start_module(self, output, title: str, description: str):
        if self._current_table:
            self._add_table_footer(output)

        output.append(f"<h2>{title}</h2>")
        if description:
            output.append(f"<p>{description}</p>")

        self._need_new_table = True

    def add_topic(
        self, output, contents: str, duration: str, methodik: str, material: str
    ):
        if self._need_new_table:
            self._create_new_table(output)
            self._need_new_table = False

        self._current_table_total_duration += int(duration)
        self._current_table.append(
            f"<tr>"
            f"<td>{contents}</td>"
            f"<td class='center'>{duration}</td>"
            f"<td>{methodik}</td>"
            f"<td>{material}</td>"
            f"</tr>"
        )

    def add_remark(self, output, abschnitt: str):
        if self._current_table:
            self._add_table_footer(output)
        output.append(f"<p><strong>{abschnitt}</strong></p>")
        self._need_new_table = True

    def _create_new_table(self, output):
        output.extend(
            [
                "<table>",
                "<tr>",
                "<th>Inhalt</th>",
                "<th>UE</th>",
                "<th>Methodik/Didaktik</th>",
                "<th>Materialien</th>",
                "</tr>",
            ]
        )
        self._current_table = []
        self._current_table_total_duration = 0

    def _add_table_footer(self, output):
        output.extend(self._current_table)
        output.append(
            f"<tr>"
            f"<td class='right'><strong>Summe:</strong></td>"
            f"<td class='center'><strong>{self._current_table_total_duration}</strong></td>"
            f"<td></td>"
            f"<td></td>"
            f"</tr>"
        )
        output.append("</table>")
        self._current_table = []
        self._current_table_total_duration = 0
