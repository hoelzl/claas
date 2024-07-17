from claas.word_converter import WordConverter
from fixtures import full_example, minimal_example


def test_word_converter_minimal_summary(minimal_example):
    converter = WordConverter(minimal_example, output_format="summary")
    document = converter.convert()

    assert document.paragraphs[0].text == "Kurs Titel"
    assert document.paragraphs[1].text == "Modul 1 Titel (2 UE)"
    assert document.paragraphs[2].text == "Zusammenfassung 1 (2 UE)"
    assert document.paragraphs[2].style.name == "List Bullet"
    assert document.paragraphs[3].text == "Unterrichtseinheiten insgesamt: 2"
    assert len(document.paragraphs) == 4


def test_word_converter_minimal_detailed(minimal_example):
    converter = WordConverter(minimal_example, output_format="detailed")
    document = converter.convert()

    assert document.paragraphs[0].text == "Kurs Titel"
    assert document.paragraphs[1].text == "Modul 1 Titel (2 UE)"
    assert document.paragraphs[2].text == "Thema 1.1 (2 UE)"
    assert document.paragraphs[2].style.name == "List Bullet"
    assert document.paragraphs[3].text == "Unterrichtseinheiten insgesamt: 2"
    assert len(document.paragraphs) == 4


def test_word_converter_full_summary(full_example):
    converter = WordConverter(full_example, output_format="summary")
    document = converter.convert()

    assert document.paragraphs[0].text == "Kurs Titel"
    assert document.paragraphs[1].text == "Modul 1 Titel (9 UE)"
    assert document.paragraphs[2].text == "Modul 1 Beschreibung"
    assert document.paragraphs[3].text == "Zusammenfassung 1 (4 UE)"
    assert document.paragraphs[3].style.name == "List Bullet"
    assert document.paragraphs[4].text == "Abschnitt 1"
    assert document.paragraphs[4].style.name == "Heading 3"
    assert document.paragraphs[5].text == "Woche 1: Wocheninhalt 1 (5 UE)"
    assert document.paragraphs[5].style.name == "Heading 3"
    assert document.paragraphs[6].text == "Zusammenfassung 2 (3 UE)"
    assert document.paragraphs[6].style.name == "List Bullet"
    assert document.paragraphs[7].text == "Zusammenfassung 3 (1 UE)"
    assert document.paragraphs[7].style.name == "List Bullet"
    assert document.paragraphs[8].text == "Zusammenfassung 4 (1 UE)"
    assert document.paragraphs[8].style.name == "List Bullet"
    assert document.paragraphs[9].text == "Unterrichtseinheiten insgesamt: 9"
    assert len(document.paragraphs) == 10


def test_word_converter_full_detailed(full_example):
    converter = WordConverter(full_example, output_format="detailed")
    document = converter.convert()

    assert document.paragraphs[0].text == "Kurs Titel"
    assert document.paragraphs[1].text == "Modul 1 Titel (9 UE)"
    assert document.paragraphs[2].text == "Modul 1 Beschreibung"
    assert document.paragraphs[3].text == "Thema 1.1 (1 UE)"
    assert document.paragraphs[3].style.name == "List Bullet"
    assert document.paragraphs[4].text == "Thema 1.2 (3 UE)"
    assert document.paragraphs[4].style.name == "List Bullet"
    assert document.paragraphs[5].text == "Abschnitt 1"
    assert document.paragraphs[5].style.name == "Heading 3"
    assert document.paragraphs[6].text == "Woche 1: Wocheninhalt 1 (4 UE)"
    assert document.paragraphs[6].style.name == "Heading 3"
    assert document.paragraphs[7].text == "Thema 2.1 (2 UE)"
    assert document.paragraphs[7].style.name == "List Bullet"
    assert document.paragraphs[8].text == "Thema 2.2 (1 UE)"
    assert document.paragraphs[8].style.name == "List Bullet"
    assert document.paragraphs[9].text == "Zusammenfassung 3"
    assert document.paragraphs[9].style.name == "List Bullet"
    assert document.paragraphs[10].text == "(kein Text) (1 UE)"
    assert document.paragraphs[10].style.name == "List Bullet"
    assert document.paragraphs[11].text == "Unterrichtseinheiten insgesamt: 9"
    assert len(document.paragraphs) == 12
