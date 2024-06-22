from claas.word_converter import WordConverter
from fixtures import full_example, minimal_example


def test_word_converter_minimal(minimal_example):
    converter = WordConverter(minimal_example)
    document = converter.convert()

    assert document.paragraphs[0].text == "Kurs Titel"
    assert document.paragraphs[1].text == "Modul 1 Titel"
    assert document.paragraphs[2].text == "Thema 1.1 (2 UE)"
    assert document.paragraphs[2].style.name == "List Number"
    assert len(document.paragraphs) == 3


def test_word_converter_full(full_example):
    converter = WordConverter(full_example)
    document = converter.convert()

    assert document.paragraphs[0].text == "Kurs Titel"
    assert document.paragraphs[1].text == "Modul 1 Titel"
    assert document.paragraphs[2].text == "Modul 1 Beschreibung"
    assert document.paragraphs[3].text == "Thema 1 Inhalt (3 UE)"
    assert document.paragraphs[3].style.name == "List Number"
    assert document.paragraphs[4].text == "Bemerkung 1"
    assert document.paragraphs[4].style.name == "Heading 3"
    assert document.paragraphs[5].text == "Bemerkung 2"
    assert document.paragraphs[5].style.name == "Heading 3"
    assert document.paragraphs[6].text == "Thema 2 Inhalt (5 UE)"
    assert document.paragraphs[6].style.name == "List Number"
    assert len(document.paragraphs) == 7
