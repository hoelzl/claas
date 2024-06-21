from xml.etree import ElementTree

import pytest
from pathlib import Path

file_path = Path(__file__).resolve()

minimal_example_xml = file_path.parent / "minimal_example.xml"
assert minimal_example_xml.exists()

full_example_xml = file_path.parent / "full_example.xml"
assert full_example_xml.exists()


@pytest.fixture
def minimal_example():
    return ElementTree.parse(minimal_example_xml)


@pytest.fixture
def full_example():
    return ElementTree.parse(full_example_xml)
