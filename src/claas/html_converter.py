from claas.curriculum_converter import CurriculumConverter


class HtmlConverter(CurriculumConverter):
    def start_output(self, title) -> list[str]:
        prefix = [
            "<html>",
            "<head>",
            f"<title>Lehrplan: {title}</title>",
            "</head>",
            "<body>",
            f"<h1>{title}</h1>",
        ]
        return prefix

    def finalize_output(self, output) -> str:
        output.extend(["</body>", "</html>"])
        return "\n".join(output)

    def start_module(self, output, title: str, description: str, total_time: int):
        if self.include_time and total_time:
            output.append(f"<h2>{title} ({total_time} UE)</h2>")
        else:
            output.append(f"<h2>{title}</h2>")
        if description:
            output.append(f"<p>{description}</p>")

    def start_topic_list(self, output):
        output.append("<ul>")

    def end_topic_list(self, output):
        output.append("</ul>")

    def add_topic(
        self, output, contents: str, duration: str, method: str, material: str
    ):
        if self.include_time and duration:
            output.append(f"<li>{contents} ({duration} UE)</li>")
        else:
            output.append(f"<li>{contents}</li>")

    def add_section(self, output, text: str, week_time: int = None):
        if self.include_time and week_time:
            output.append(f"<h3>{text} ({week_time} UE)</h3>")
        else:
            output.append(f"<h3>{text}</h3>")
