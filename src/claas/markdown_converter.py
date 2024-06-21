from claas.curriculum_converter import CurriculumConverter


class MarkdownConverter(CurriculumConverter):
    def start_output(self):
        return []

    def add_module(self, output, title, description):
        output.append(f"# {title}")
        if description is not None:
            output.append(f"\n{description.text}\n")

    def add_topic(self, output, contents, duration, methodik, material):
        output.append(f"## Thema: {contents}")
        output.append(f"- **Dauer:** {duration} Minuten")
        output.append(f"- **Methodik:** {methodik}")
        output.append(f"- **Material:** {material}\n")

    def add_remark(self, output, bemerkung):
        output.append(f"## Bemerkung")
        output.append(f"{bemerkung}\n")

    def finalize_output(self, output):
        return "\n".join(output)
