from claas.word_converter import WordConverter
from fixtures import full_example, minimal_example


def test_word_converter_minimal(minimal_example):
    converter = WordConverter(minimal_example)
    document = converter.convert()

    assert document.paragraphs[0].text == "Modul 1 Titel"
    assert document.paragraphs[1].text == "Thema: Thema 1.1"
    assert document.paragraphs[2].text == "Dauer: 2 Einheiten"
    assert document.paragraphs[3].text == "Methodik: Frontalunterricht"
    assert document.paragraphs[4].text == "Material: Folien, Notebooks"


def test_word_converter_full(full_example):
    converter = WordConverter(full_example)
    document = converter.convert()

    assert document.paragraphs[0].text == "Modul 1 Titel"
    assert document.paragraphs[1].text == "Modul 1 Beschreibung"
    assert document.paragraphs[2].text == "Thema: Thema 1 Inhalt"
    assert document.paragraphs[3].text == "Dauer: 3 Einheiten"
    assert document.paragraphs[3].style.name == "List Bullet"
    assert document.paragraphs[4].text == "Methodik: Frontalunterricht"
    assert document.paragraphs[4].style.name == "List Bullet"
    assert document.paragraphs[5].text == "Material: Folien, Notebooks"
    assert document.paragraphs[5].style.name == "List Bullet"
    assert document.paragraphs[6].text == "Bemerkung"
    assert document.paragraphs[7].text == "Bemerkung 1"
    assert document.paragraphs[8].text == "Bemerkung"
    assert document.paragraphs[9].text == "Bemerkung 2"
    assert document.paragraphs[10].text == "Thema: Thema 2 Inhalt"
    assert document.paragraphs[11].text == "Dauer: 5 Einheiten"
    assert document.paragraphs[11].style.name == "List Bullet"
    assert document.paragraphs[12].text == "Methodik: Gruppenarbeit"
    assert document.paragraphs[12].style.name == "List Bullet"
    assert document.paragraphs[13].text == "Material: Handouts"
    assert document.paragraphs[13].style.name == "List Bullet"
