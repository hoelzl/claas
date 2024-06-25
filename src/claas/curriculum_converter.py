import xml.etree.ElementTree as ET  # noqa
from abc import ABC, abstractmethod
from typing import Any


class CurriculumConverter(ABC):
    def __init__(self, tree: ET.ElementTree):
        self.tree = tree
        self.root = self.tree.getroot()
        self.namespace = {"ns": "http://xsd.coding-academy.com/claas/azav-kurs"}
        self.output = None

    def convert(self):
        title = self.root.find("ns:titel", self.namespace).text
        output = self.start_output(title)
        for module in self.root.findall("ns:modul", self.namespace):
            module_title = module.find("ns:titel", self.namespace).text
            module_description = self.get_default_text(
                module.find("ns:beschreibung", self.namespace), ""
            )

            self.start_module(output, module_title, module_description)

            for element in module:
                if element.tag.endswith("thema"):
                    contents = element.find("ns:inhalt", self.namespace).text
                    duration = element.find("ns:dauer", self.namespace)
                    method = element.find("ns:methodik", self.namespace)
                    material = element.find("ns:material", self.namespace)

                    duration_text = self.get_default_text(duration, "1")
                    methodik_text = self.get_default_text(method, "Frontalunterricht")
                    material_text = self.get_default_text(material, "Folien, Notebooks")

                    self.add_topic(
                        output, contents, duration_text, methodik_text, material_text
                    )
                elif element.tag.endswith("abschnitt"):
                    section = element.text
                    self.add_remark(output, section)

            self.finalize_module(output)
        return self.finalize_output(output)

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

    @abstractmethod
    def add_topic(
        self, output, contents: str, duration: str, method: str, material: str
    ):
        pass

    @abstractmethod
    def add_remark(self, output, text: str):
        pass
