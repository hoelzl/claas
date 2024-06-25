from claas.html_converter import HtmlConverter
from fixtures import full_example, minimal_example


def test_html_converter_minimal(minimal_example):
    expected = (
        "<html>\n"
        "<head>\n"
        "<title>Lehrplan: Kurs Titel</title>\n"
        "</head>\n"
        "<body>\n"
        "<h1>Kurs Titel</h1>\n"
        "<h2>Modul 1 Titel</h2>\n"
        "<ul>\n"
        "<li>Thema 1.1 (2 UE)</li>\n"
        "</ul>\n"
        "</body>\n"
        "</html>"
    )
    converter = HtmlConverter(minimal_example)

    assert converter.convert() == expected


def test_html_converter_full(full_example):
    expected = (
        "<html>\n"
        "<head>\n"
        "<title>Lehrplan: Kurs Titel</title>\n"
        "</head>\n"
        "<body>\n"
        "<h1>Kurs Titel</h1>\n"
        "<h2>Modul 1 Titel</h2>\n"
        "<p>Modul 1 Beschreibung</p>\n"
        "<ul>\n"
        "<li>Thema 1 Inhalt (1 UE)</li>\n"
        "</ul>\n"
        "<h3>abschnitt 1</h3>\n"
        "<ul>\n"
        "</ul>\n"
        "<h3>abschnitt 2</h3>\n"
        "<ul>\n"
        "<li>Thema 2 Inhalt (5 UE)</li>\n"
        "</ul>\n"
        "</body>\n"
        "</html>"
    )
    converter = HtmlConverter(full_example)

    assert converter.convert() == expected
