from claas.markdown_converter import MarkdownConverter
from fixtures import full_example, minimal_example


def test_markdown_converter_minimal(minimal_example):
    expected = (
        "# Modul 1 Titel\n"
        "## Thema: Thema 1.1\n"
        "- **Dauer:** 2 Einheiten\n"
        "- **Methodik:** Frontalunterricht\n"
        "- **Material:** Folien, Notebooks\n"
    )
    converter = MarkdownConverter(minimal_example)

    assert converter.convert() == expected


def test_markdown_converter_full(full_example):
    expected = (
        "# Modul 1 Titel\n"
        "\n"
        "Modul 1 Beschreibung\n"
        "\n"
        "## Thema: Thema 1 Inhalt\n"
        "- **Dauer:** 3 Einheiten\n"
        "- **Methodik:** Frontalunterricht\n"
        "- **Material:** Folien, Notebooks\n"
        "\n"
        "## Bemerkung\n"
        "Bemerkung 1\n"
        "\n"
        "## Bemerkung\n"
        "Bemerkung 2\n"
        "\n"
        "## Thema: Thema 2 Inhalt\n"
        "- **Dauer:** 5 Einheiten\n"
        "- **Methodik:** Gruppenarbeit\n"
        "- **Material:** Handouts\n"
    )
    converter = MarkdownConverter(full_example)

    assert converter.convert() == expected
