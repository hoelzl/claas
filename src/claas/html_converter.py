from claas.curriculum_converter import CurriculumConverter


class HtmlConverter(CurriculumConverter):
    def start_output(self):
        return ["<html><body>"]

    def add_module(self, output, title, description):
        output.append(f"<h1>{title}</h1>")
        if description is not None:
            output.append(f"<p>{description.text}</p>")

    def add_topic(self, output, contents, duration, methodik, material):
        output.append(f"<h2>Thema: {contents}</h2>")
        output.append(f"<ul>")
        output.append(f"<li><strong>Dauer:</strong> {duration} Einheiten</li>")
        output.append(f"<li><strong>Methodik:</strong> {methodik}</li>")
        output.append(f"<li><strong>Material:</strong> {material}</li>")
        output.append(f"</ul>")

    def add_remark(self, output, bemerkung):
        output.append(f"<h2>Bemerkung</h2>")
        output.append(f"<p>{bemerkung}</p>")

    def finalize_output(self, output):
        output.append("</body></html>")
        return "\n".join(output)
