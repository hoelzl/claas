from claas.word_converter import WordConverter
from fixtures import full_example, minimal_example


def test_word_converter_minimal_summary(minimal_example):
    converter = WordConverter(minimal_example, detailed=False)
    document = converter.convert()

    assert document.paragraphs[0].text == "Kurs Titel"
    assert document.paragraphs[1].text == "Modul 1 Titel (2 UE)"
    assert document.paragraphs[2].text == "Zusammenfassung 1 (2 UE)"
    assert document.paragraphs[2].style.name == "List Number"
    assert document.paragraphs[3].text == "Unterrichtseinheiten insgesamt: 2"
    assert len(document.paragraphs) == 4


def test_word_converter_minimal_detailed(minimal_example):
    converter = WordConverter(minimal_example, detailed=True)
    document = converter.convert()

    assert document.paragraphs[0].text == "Kurs Titel"
    assert document.paragraphs[1].text == "Modul 1 Titel (2 UE)"
    assert document.paragraphs[2].text == "Thema 1.1 (2 UE)"
    assert document.paragraphs[2].style.name == "List Number"
    assert document.paragraphs[3].text == "Unterrichtseinheiten insgesamt: 2"
    assert len(document.paragraphs) == 4


def test_word_converter_full_summary(full_example):
    converter = WordConverter(full_example, detailed=False)
    document = converter.convert()

    assert document.paragraphs[0].text == "Kurs Titel"
    assert document.paragraphs[1].text == "Modul 1 Titel (7 UE)"
    assert document.paragraphs[2].text == "Modul 1 Beschreibung"
    assert document.paragraphs[3].text == "Zusammenfassung 1 (4 UE)"
    assert document.paragraphs[3].style.name == "List Number"
    assert document.paragraphs[4].text == "Abschnitt 1"
    assert document.paragraphs[4].style.name == "Heading 3"
    assert document.paragraphs[5].text == "Woche 1: Wocheninhalt 1 (3 UE)"
    assert document.paragraphs[5].style.name == "Heading 3"
    assert document.paragraphs[6].text == "Zusammenfassung 2 (3 UE)"
    assert document.paragraphs[6].style.name == "List Number"
    assert document.paragraphs[7].text == "Unterrichtseinheiten insgesamt: 7"
    assert len(document.paragraphs) == 8


def test_word_converter_full_detailed(full_example):
    converter = WordConverter(full_example, detailed=True)
    document = converter.convert()

    assert document.paragraphs[0].text == "Kurs Titel"
    assert document.paragraphs[1].text == "Modul 1 Titel (7 UE)"
    assert document.paragraphs[2].text == "Modul 1 Beschreibung"
    assert document.paragraphs[3].text == "Thema 1.1 (1 UE)"
    assert document.paragraphs[3].style.name == "List Number"
    assert document.paragraphs[4].text == "Thema 1.2 (3 UE)"
    assert document.paragraphs[4].style.name == "List Number"
    assert document.paragraphs[5].text == "Abschnitt 1"
    assert document.paragraphs[5].style.name == "Heading 3"
    assert document.paragraphs[6].text == "Woche 1: Wocheninhalt 1 (3 UE)"
    assert document.paragraphs[6].style.name == "Heading 3"
    assert document.paragraphs[7].text == "Thema 2.1 (2 UE)"
    assert document.paragraphs[7].style.name == "List Number"
    assert document.paragraphs[8].text == "Thema 2.2 (1 UE)"
    assert document.paragraphs[8].style.name == "List Number"
    assert document.paragraphs[9].text == "Unterrichtseinheiten insgesamt: 7"
    assert len(document.paragraphs) == 10
