import xml.etree.ElementTree as ET  # noqa
from abc import ABC, abstractmethod
from typing import Any


class CurriculumConverter(ABC):
    def __init__(self, tree: ET.ElementTree, include_time=True, detailed=True):
        self.tree = tree
        self.root = self.tree.getroot()
        self.namespace = {"ns": "http://xsd.coding-academy.com/claas/azav-kurs"}
        self.output = None
        self.current_week = 0
        self.include_time = include_time
        self.detailed = detailed

    def convert(self):
        title = self.root.find("ns:titel", self.namespace).text
        output = self.start_output(title)
        for module in self.root.findall("ns:modul", self.namespace):
            module_title = module.find("ns:titel", self.namespace).text
            module_description = self.get_default_text(
                module.find("ns:beschreibung", self.namespace), ""
            )

            self.start_module(output, module_title, module_description)

            topics = []
            for element in module:
                if element.tag.endswith("themengruppe"):
                    summary = element.find("ns:zusammenfassung", self.namespace).text
                    if self.detailed:
                        detail_themes = element.find("ns:detailthemen", self.namespace)
                        if detail_themes is not None:
                            for theme in detail_themes.findall(
                                "ns:thema", self.namespace
                            ):
                                contents = theme.find("ns:inhalt", self.namespace).text
                                duration = theme.find("ns:dauer", self.namespace)
                                method = theme.find("ns:methodik", self.namespace)
                                material = theme.find("ns:material", self.namespace)

                                duration_text = self.get_default_text(duration, "1")
                                methodik_text = self.get_default_text(
                                    method, "Frontalunterricht"
                                )
                                material_text = self.get_default_text(
                                    material, "Folien, Notebooks"
                                )

                                topics.append(
                                    (
                                        contents,
                                        duration_text,
                                        methodik_text,
                                        material_text,
                                    )
                                )
                    else:
                        total_duration = self.compute_total_duration(element)
                        topics.append((summary, str(total_duration), "", ""))
                elif element.tag.endswith("abschnitt"):
                    self.add_topics(output, topics)
                    topics = []
                    section = element.text
                    self.add_section(output, section)
                elif element.tag.endswith("woche"):
                    self.add_topics(output, topics)
                    topics = []
                    self.current_week += 1
                    section = f"Woche {self.current_week}: {element.text}"
                    self.add_section(output, section)

            self.add_topics(output, topics)
            self.finalize_module(output)
        return self.finalize_output(output)

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
    def start_module(self, output, title: str, description: str):
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
    def add_section(self, output, text: str):
        pass
