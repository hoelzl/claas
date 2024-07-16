import re

from claas.curriculum_converter import CurriculumConverter


class MarkdownConverter(CurriculumConverter):
    def start_output(self, title) -> list[str]:
        return [f"# {title}"]

    def finalize_output(self, output) -> str:
        if self.include_time:
            output.append(
                f"\n\n**Unterrichtseinheiten insgesamt: {self.total_course_hours}**"
            )
        result = "\n".join(output)
        result = re.sub(r"\n{3,}", "\n\n", result)
        return result

    def start_module(self, output, title: str, description: str, total_time: int):
        if self.include_time and total_time:
            output.append(f"\n## {title} ({total_time} UE)")
        else:
            output.append(f"\n## {title}")
        if description:
            output.append(f"\n{description}\n")

    def add_summary_topic(
        self, output, contents: str, duration: str, method: str, material: str
    ):
        if self.include_time and duration:
            output.append(f"- {contents} ({duration} UE)")
        else:
            output.append(f"- {contents}")

    def add_detail_topic(
        self, output, contents: str, duration: str, method: str, material: str
    ):
        if self.include_time and duration:
            output.append(f"  - {contents} ({duration} UE)")
        else:
            output.append(f"  - {contents}")

    def add_section(self, output, text: str, week_time: int = None):
        if self.include_time and week_time:
            output.append(f"\n### {text} ({week_time} UE)\n")
        else:
            output.append(f"\n### {text}\n")

    def add_subtopic(
        self, output, contents: str, duration: str, method: str, material: str
    ):
        if self.include_time and duration:
            output.append(f"  - {contents} ({duration} UE)")
        else:
            output.append(f"  - {contents}")
