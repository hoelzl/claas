from claas.html_converter import HtmlConverter
from fixtures import minimal_example, full_example


def test_html_converter_minimal(minimal_example):
    expected = (
        "<html><body>\n"
        "<h1>Modul 1 Titel</h1>\n"
        "<h2>Thema: Thema 1.1</h2>\n"
        "<ul>\n"
        "<li><strong>Dauer:</strong> 2 Minuten</li>\n"
        "<li><strong>Methodik:</strong> Frontalunterricht</li>\n"
        "<li><strong>Material:</strong> Folien, Notebooks</li>\n"
        "</ul>\n"
        "</body></html>"
    )
    converter = HtmlConverter(minimal_example)

    assert converter.convert() == expected


def test_html_converter_full(full_example):
    expected = (
        "<html><body>\n"
        "<h1>Modul 1 Titel</h1>\n"
        "<p>Modul 1 Beschreibung</p>\n"
        "<h2>Thema: Thema 1 Inhalt</h2>\n"
        "<ul>\n"
        "<li><strong>Dauer:</strong> 3 Minuten</li>\n"
        "<li><strong>Methodik:</strong> Frontalunterricht</li>\n"
        "<li><strong>Material:</strong> Folien, Notebooks</li>\n"
        "</ul>\n"
        "<h2>Bemerkung</h2>\n"
        "<p>Bemerkung 1</p>\n"
        "<h2>Bemerkung</h2>\n"
        "<p>Bemerkung 2</p>\n"
        "<h2>Thema: Thema 2 Inhalt</h2>\n"
        "<ul>\n"
        "<li><strong>Dauer:</strong> 5 Minuten</li>\n"
        "<li><strong>Methodik:</strong> Gruppenarbeit</li>\n"
        "<li><strong>Material:</strong> Handouts</li>\n"
        "</ul>\n"
        "</body></html>"
    )
    converter = HtmlConverter(full_example)

    assert converter.convert() == expected
