import xml.etree.ElementTree as ET  # noqa
from abc import ABC, abstractmethod
from typing import Any


class CurriculumConverter(ABC):
    def __init__(
        self, tree: ET.ElementTree, include_time=True, output_format="detailed"
    ):
        self.tree = tree
        self.root = self.tree.getroot()
        self.namespace = {"ns": "http://xsd.coding-academy.com/claas/azav-kurs"}
        self.output = None
        self.current_week = 0
        self.include_time = include_time
        self.output_format = output_format
        self.weekly_course_hours = 0
        self.total_course_hours = 0
        self.processing_detail_topics = False
        self.method_default = "Frontalunterricht"
        self.material_default = "Folien, Notebooks"

    def convert(self):
        title = self.root.find("ns:titel", self.namespace).text
        output = self.start_output(title)
        for module in self.root.findall("ns:modul", self.namespace):
            module_hours = self.calculate_module_hours(module)
            self.total_course_hours += module_hours  # Add module hours to total
            module_title = module.find("ns:titel", self.namespace).text
            module_description = self.get_default_text(
                module.find("ns:beschreibung", self.namespace), ""
            )

            self.start_module(output, module_title, module_description, module_hours)

            module_content = self.process_module_content(module)
            self.render_module_content(output, module_content)

            self.finalize_module(output)
        return self.finalize_output(output)

    def process_module_content(self, module):
        content = []
        current_week = None
        current_topics = []

        for element in module:
            if element.tag.endswith("themengruppe"):
                topics = self.process_themengruppe(element)
                current_topics.extend(topics)
            elif element.tag.endswith("abschnitt"):
                if current_topics:
                    content.append(("topics", current_topics))
                    current_topics = []
                content.append(("section", element.text))
            elif element.tag.endswith("woche"):
                if current_topics:
                    if current_week is None:
                        content.append(("topics", current_topics))
                    else:
                        content.append(("week", current_week, current_topics))
                current_week = element.text
                current_topics = []

        if current_topics:
            if current_week is None:
                content.append(("topics", current_topics))
            else:
                content.append(("week", current_week, current_topics))

        return content

    def process_themengruppe(self, themengruppe):
        summary = themengruppe.find("ns:zusammenfassung", self.namespace).text
        topics = []

        if self.output_format in ["detailed", "combined"]:
            detail_themes = themengruppe.find("ns:detailthemen", self.namespace)
            if detail_themes is not None:
                for theme in detail_themes.findall("ns:thema", self.namespace):
                    topic = self.process_theme(theme)
                    topics.append(("detail", topic))
            else:
                topics.append(
                    (
                        "detail",
                        (summary, "", self.method_default, self.material_default),
                    )
                )

        if self.output_format in ["summary", "combined"]:
            total_duration = self.compute_total_duration(themengruppe)
            topics.insert(
                0,
                (
                    "summary",
                    (
                        summary,
                        str(total_duration),
                        self.method_default,
                        self.material_default,
                    ),
                ),
            )

        return topics

    def render_module_content(self, output, module_content):
        for item in module_content:
            if item[0] == "section":
                self.add_section(output, item[1])
            elif item[0] == "week":
                week_text, topics = item[1], item[2]
                self.current_week += 1
                week_total_time = sum(
                    int(topic[1][1]) for topic in topics if topic[1][1]
                )
                section = f"Woche {self.current_week}: {week_text}"
                self.add_section(output, section, week_total_time)
                self.add_topics(output, topics)
            elif item[0] == "topics":
                self.add_topics(output, item[1])

    def add_topics(self, output, topics):
        if topics:
            self.start_topic_list(output)
            for topic_type, topic in topics:
                if self.output_format == "combined" and topic_type == "detail":
                    if not self.processing_detail_topics:
                        self.processing_detail_topics = True
                        self.start_topic_list(output)
                    self.add_detail_topic(output, *topic)
                else:
                    if self.processing_detail_topics:
                        self.end_topic_list(output)
                        self.processing_detail_topics = False
                    self.add_summary_topic(output, *topic)
            self.end_topic_list(output)

    def process_theme(self, theme):
        contents = theme.find("ns:inhalt", self.namespace).text
        duration = theme.find("ns:dauer", self.namespace)
        method = theme.find("ns:methodik", self.namespace)
        material = theme.find("ns:material", self.namespace)

        duration_text = self.get_default_text(duration, "1")
        method_text = self.get_default_text(method, self.method_default)
        material_text = self.get_default_text(material, self.material_default)

        return contents, duration_text, method_text, material_text

    def compute_total_duration(self, themengruppe):
        detail_themes = themengruppe.find("ns:detailthemen", self.namespace)
        if detail_themes is None:
            return 1

        total_duration = 0
        for theme in detail_themes.findall("ns:thema", self.namespace):
            duration = theme.find("ns:dauer", self.namespace)
            duration_value = int(self.get_default_text(duration, "1"))
            total_duration += duration_value

        return total_duration if total_duration > 0 else 1

    def calculate_module_hours(self, module):
        total_duration = 0
        for element in module:
            if element.tag.endswith("themengruppe"):
                total_duration += self.compute_total_duration(element)
        return total_duration

    def save(self, output_path):
        doc = self.convert()
        with open(output_path, "w") as f:
            f.write(doc)

    @staticmethod
    def get_default_text(element, default):
        return element.text if element is not None else default

    @abstractmethod
    def start_output(self, title: str):
        pass

    @abstractmethod
    def finalize_output(self, output) -> Any:
        pass

    @abstractmethod
    def start_module(self, output, title: str, description: str, total_time: int):
        pass

    def finalize_module(self, output):
        pass

    def start_topic_list(self, output):
        pass

    def end_topic_list(self, output):
        pass

    @abstractmethod
    def add_summary_topic(
        self, output, contents: str, duration: str, method: str, material: str
    ):
        pass

    @abstractmethod
    def add_detail_topic(
        self, output, contents: str, duration: str, method: str, material: str
    ):
        pass

    @abstractmethod
    def add_section(self, output, text: str, week_time: int = None):
        pass
