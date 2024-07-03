import xml.etree.ElementTree as ET  # noqa
from abc import ABC, abstractmethod
from typing import Any, List, Tuple


class CurriculumConverter(ABC):
    def __init__(self, tree: ET.ElementTree, include_time=True, detailed=True):
        self.tree = tree
        self.root = self.tree.getroot()
        self.namespace = {"ns": "http://xsd.coding-academy.com/claas/azav-kurs"}
        self.output = None
        self.current_week = 0
        self.include_time = include_time
        self.detailed = detailed
        self.week_total_time = 0

    def convert(self):
        title = self.root.find("ns:titel", self.namespace).text
        output = self.start_output(title)
        for module in self.root.findall("ns:modul", self.namespace):
            module_total_time = self.calculate_module_duration(module)
            module_title = module.find("ns:titel", self.namespace).text
            module_description = self.get_default_text(
                module.find("ns:beschreibung", self.namespace), ""
            )

            self.start_module(
                output, module_title, module_description, module_total_time
            )

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

        if self.detailed:
            detail_themes = themengruppe.find("ns:detailthemen", self.namespace)
            if detail_themes is not None:
                for theme in detail_themes.findall("ns:thema", self.namespace):
                    topic = self.process_theme(theme)
                    topics.append(topic)
            else:
                topics.append((summary, "", "", ""))
        else:
            total_duration = self.compute_total_duration(themengruppe)
            topics.append((summary, str(total_duration), "", ""))

        return topics

    def process_theme(self, theme):
        contents = theme.find("ns:inhalt", self.namespace).text
        duration = theme.find("ns:dauer", self.namespace)
        method = theme.find("ns:methodik", self.namespace)
        material = theme.find("ns:material", self.namespace)

        duration_text = self.get_default_text(duration, "1")
        methodik_text = self.get_default_text(method, "Frontalunterricht")
        material_text = self.get_default_text(material, "Folien, Notebooks")

        return contents, duration_text, methodik_text, material_text

    def render_module_content(self, output, module_content):
        for item in module_content:
            if item[0] == "section":
                self.add_section(output, item[1])
            elif item[0] == "week":
                week_text, topics = item[1], item[2]
                self.current_week += 1
                week_total_time = sum(int(topic[1]) for topic in topics)
                section = f"Woche {self.current_week}: {week_text}"
                self.add_section(output, section, week_total_time)
                self.add_topics(output, topics)
            elif item[0] == "topics":
                self.add_topics(output, item[1])

    def add_topics(self, output, topics):
        if topics:
            self.start_topic_list(output)
            for topic in topics:
                self.add_topic(output, *topic)
            self.end_topic_list(output)

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

    def calculate_module_duration(self, module):
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
    def add_topic(
        self, output, contents: str, duration: str, method: str, material: str
    ):
        pass

    @abstractmethod
    def add_section(self, output, text: str, week_time: int = None):
        pass
