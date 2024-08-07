from claas.html_converter import HtmlConverter
from fixtures import full_example, minimal_example


def test_html_converter_minimal_summary(minimal_example):
    expected = (
        "<html>\n"
        "<head>\n"
        "<title>Lehrplan: Kurs Titel</title>\n"
        "</head>\n"
        "<body>\n"
        "<h1>Kurs Titel</h1>\n"
        "<h2>Modul 1 Titel (2 UE)</h2>\n"
        "<ul>\n"
        "<li>Zusammenfassung 1 (2 UE)</li>\n"
        "</ul>\n"
        "<p><strong>Unterrichtseinheiten insgesamt: 2</strong></p>\n"
        "</body>\n"
        "</html>"
    )
    converter = HtmlConverter(minimal_example, output_format="summary")

    assert converter.convert() == expected


def test_html_converter_minimal_detailed(minimal_example):
    expected = (
        "<html>\n"
        "<head>\n"
        "<title>Lehrplan: Kurs Titel</title>\n"
        "</head>\n"
        "<body>\n"
        "<h1>Kurs Titel</h1>\n"
        "<h2>Modul 1 Titel (2 UE)</h2>\n"
        "<ul>\n"
        "<li>Thema 1.1 (2 UE)</li>\n"
        "</ul>\n"
        "<p><strong>Unterrichtseinheiten insgesamt: 2</strong></p>\n"
        "</body>\n"
        "</html>"
    )
    converter = HtmlConverter(minimal_example, output_format="detailed")

    assert converter.convert() == expected


def test_html_converter_minimal_combined(minimal_example):
    expected = (
        "<html>\n"
        "<head>\n"
        "<title>Lehrplan: Kurs Titel</title>\n"
        "</head>\n"
        "<body>\n"
        "<h1>Kurs Titel</h1>\n"
        "<h2>Modul 1 Titel (2 UE)</h2>\n"
        "<ul>\n"
        "<li>Zusammenfassung 1 (2 UE)</li>\n"
        "<ul>\n"
        "<li>Thema 1.1 (2 UE)</li>\n"
        "</ul>\n"
        "<p><strong>Unterrichtseinheiten insgesamt: 2</strong></p>\n"
        "</body>\n"
        "</html>"
    )
    converter = HtmlConverter(minimal_example, output_format="combined")

    assert converter.convert() == expected


def test_html_converter_full_summary(full_example):
    expected = (
        "<html>\n"
        "<head>\n"
        "<title>Lehrplan: Kurs Titel</title>\n"
        "</head>\n"
        "<body>\n"
        "<h1>Kurs Titel</h1>\n"
        "<h2>Modul 1 Titel (9 UE)</h2>\n"
        "<p>Modul 1 Beschreibung</p>\n"
        "<ul>\n"
        "<li>Zusammenfassung 1 (4 UE)</li>\n"
        "</ul>\n"
        "<h3>Abschnitt 1</h3>\n"
        "<h3>Woche 1: Wocheninhalt 1 (5 UE)</h3>\n"
        "<ul>\n"
        "<li>Zusammenfassung 2 (3 UE)</li>\n"
        "<li>Zusammenfassung 3 (1 UE)</li>\n"
        "<li>Zusammenfassung 4 (1 UE)</li>\n"
        "</ul>\n"
        "<p><strong>Unterrichtseinheiten insgesamt: 9</strong></p>\n"
        "</body>\n"
        "</html>"
    )
    converter = HtmlConverter(full_example, output_format="summary")

    assert converter.convert() == expected


def test_html_converter_full_detailed(full_example):
    expected = (
        "<html>\n"
        "<head>\n"
        "<title>Lehrplan: Kurs Titel</title>\n"
        "</head>\n"
        "<body>\n"
        "<h1>Kurs Titel</h1>\n"
        "<h2>Modul 1 Titel (9 UE)</h2>\n"
        "<p>Modul 1 Beschreibung</p>\n"
        "<ul>\n"
        "<li>Thema 1.1 (1 UE)</li>\n"
        "<li>Thema 1.2 (3 UE)</li>\n"
        "</ul>\n"
        "<h3>Abschnitt 1</h3>\n"
        "<h3>Woche 1: Wocheninhalt 1 (4 UE)</h3>\n"
        "<ul>\n"
        "<li>Thema 2.1 (2 UE)</li>\n"
        "<li>Thema 2.2 (1 UE)</li>\n"
        "<li>Zusammenfassung 3</li>\n"
        "<li>(kein Text) (1 UE)</li>\n"
        "</ul>\n"
        "<p><strong>Unterrichtseinheiten insgesamt: 9</strong></p>\n"
        "</body>\n"
        "</html>"
    )
    converter = HtmlConverter(full_example, output_format="detailed")

    assert converter.convert() == expected


def test_html_converter_full_combined(full_example):
    expected = (
        "<html>\n"
        "<head>\n"
        "<title>Lehrplan: Kurs Titel</title>\n"
        "</head>\n"
        "<body>\n"
        "<h1>Kurs Titel</h1>\n"
        "<h2>Modul 1 Titel (9 UE)</h2>\n"
        "<p>Modul 1 Beschreibung</p>\n"
        "<ul>\n"
        "<li>Zusammenfassung 1 (4 UE)</li>\n"
        "<ul>\n"
        "<li>Thema 1.1 (1 UE)</li>\n"
        "<li>Thema 1.2 (3 UE)</li>\n"
        "</ul>\n"
        "</ul>\n"
        "<h3>Abschnitt 1</h3>\n"
        "<h3>Woche 1: Wocheninhalt 1 (9 UE)</h3>\n"
        "<ul>\n"
        "<li>Zusammenfassung 2 (3 UE)</li>\n"
        "<ul>\n"
        "<li>Thema 2.1 (2 UE)</li>\n"
        "<li>Thema 2.2 (1 UE)</li>\n"
        "</ul>\n"
        "<li>Zusammenfassung 3 (1 UE)</li>\n"
        "<ul>\n"
        "<li>Zusammenfassung 3</li>\n"
        "</ul>\n"
        "<li>Zusammenfassung 4 (1 UE)</li>\n"
        "<ul>\n"
        "<li>(kein Text) (1 UE)</li>\n"
        "</ul>\n"
        "<p><strong>Unterrichtseinheiten insgesamt: 9</strong></p>\n"
        "</body>\n"
        "</html>"
    )
    converter = HtmlConverter(full_example, output_format="combined")

    assert converter.convert() == expected
