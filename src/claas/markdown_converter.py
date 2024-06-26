from claas.curriculum_converter import CurriculumConverter


class MarkdownConverter(CurriculumConverter):
    def start_output(self, title) -> list[str]:
        return [f"# {title}"]

    def finalize_output(self, output) -> str:
        return "\n".join(output)

    def start_module(self, output, title: str, description: str):
        output.append(f"## {title}")
        if description:
            output.append(f"\n{description}\n")

    def add_topic(
        self, output, contents: str, duration: str, method: str, material: str
    ):
        output.append(f"- {contents} ({duration} UE)")

    def add_section(self, output, text: str):
        output.append(f"\n### {text}\n")
