from claas.markdown_converter import MarkdownConverter
from fixtures import full_example, minimal_example


def test_markdown_converter_minimal(minimal_example):
    expected = "# Kurs Titel\n## Modul 1 Titel\n- Thema 1.1 (2 UE)"
    converter = MarkdownConverter(minimal_example)

    assert converter.convert() == expected


def test_markdown_converter_full(full_example):
    expected = (
        "# Kurs Titel\n"
        "## Modul 1 Titel\n"
        "\n"
        "Modul 1 Beschreibung\n"
        "\n"
        "- Thema 1 Inhalt (1 UE)\n"
        "\n"
        "### abschnitt 1\n"
        "\n"
        "\n"
        "### Woche 1: Inhalt\n"
        "\n"
        "- Thema 2 Inhalt (5 UE)"
    )
    converter = MarkdownConverter(full_example)

    assert converter.convert() == expected
