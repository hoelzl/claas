import xml.etree.ElementTree as ET  # noqa
from abc import ABC, abstractmethod


class CurriculumConverter(ABC):
    def __init__(self, tree: ET.ElementTree):
        self.tree = tree
        self.root = self.tree.getroot()
        self.namespace = {"ns": "http://xsd.coding-academy.com/claas/azav-kurs"}

    def convert(self):
        output = self.start_output()
        for module in self.root.findall("ns:modul", self.namespace):
            module_title = module.find("ns:titel", self.namespace).text
            module_description = module.find("ns:beschreibung", self.namespace)

            self.add_module(output, module_title, module_description)

            for element in module:
                if element.tag.endswith("thema"):
                    contents = element.find("ns:inhalt", self.namespace).text
                    duration = element.find("ns:dauer", self.namespace).text
                    method = element.find("ns:methodik", self.namespace)
                    material = element.find("ns:material", self.namespace)

                    methodik_text = self.get_default_text(method, "Frontalunterricht")
                    material_text = self.get_default_text(material, "Folien, Notebooks")

                    self.add_topic(
                        output, contents, duration, methodik_text, material_text
                    )
                elif element.tag.endswith("bemerkung"):
                    bemerkung = element.text
                    self.add_remark(output, bemerkung)
        return self.finalize_output(output)

    def save(self, output_path):
        document = self.convert()
        document.save(output_path)

    @staticmethod
    def get_default_text(element, default):
        return element.text if element is not None else default

    @abstractmethod
    def start_output(self):
        pass

    @abstractmethod
    def add_module(self, output, title, description):
        pass

    @abstractmethod
    def add_topic(self, output, contents, duration, methodik, material):
        pass

    @abstractmethod
    def add_remark(self, output, bemerkung):
        pass

    @abstractmethod
    def finalize_output(self, output):
        pass
