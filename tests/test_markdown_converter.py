from claas.markdown_converter import MarkdownConverter
from fixtures import full_example, minimal_example


def test_markdown_converter_minimal_summary(minimal_example):
    expected = (
        "# Kurs Titel\n"
        "\n"
        "## Modul 1 Titel (2 UE)\n"
        "- Zusammenfassung 1 (2 UE)\n"
        "\n"
        "**Unterrichtseinheiten insgesamt: 2**"
    )
    converter = MarkdownConverter(minimal_example, output_format="summary")

    assert converter.convert() == expected


def test_markdown_converter_minimal_detailed(minimal_example):
    expected = (
        "# Kurs Titel\n"
        "\n"
        "## Modul 1 Titel (2 UE)\n"
        "- Thema 1.1 (2 UE)\n"
        "\n"
        "**Unterrichtseinheiten insgesamt: 2**"
    )
    converter = MarkdownConverter(minimal_example, output_format="detailed")

    assert converter.convert() == expected


def test_markdown_converter_full_summary(full_example):
    expected = (
        "# Kurs Titel\n"
        "\n"
        "## Modul 1 Titel (9 UE)\n"
        "\n"
        "Modul 1 Beschreibung\n"
        "\n"
        "- Zusammenfassung 1 (4 UE)\n"
        "\n"
        "### Abschnitt 1\n"
        "\n"
        "### Woche 1: Wocheninhalt 1 (5 UE)\n"
        "\n"
        "- Zusammenfassung 2 (3 UE)\n"
        "- Zusammenfassung 3 (1 UE)\n"
        "- Zusammenfassung 4 (1 UE)\n"
        "\n"
        "**Unterrichtseinheiten insgesamt: 9**"
    )
    converter = MarkdownConverter(full_example, output_format="summary")

    assert converter.convert() == expected


def test_markdown_converter_full_detailed(full_example):
    expected = (
        "# Kurs Titel\n"
        "\n"
        "## Modul 1 Titel (9 UE)\n"
        "\n"
        "Modul 1 Beschreibung\n"
        "\n"
        "- Thema 1.1 (1 UE)\n"
        "- Thema 1.2 (3 UE)\n"
        "\n"
        "### Abschnitt 1\n"
        "\n"
        "### Woche 1: Wocheninhalt 1 (4 UE)\n"
        "\n"
        "- Thema 2.1 (2 UE)\n"
        "- Thema 2.2 (1 UE)\n"
        "- Zusammenfassung 3\n"
        "- (kein Text) (1 UE)\n"
        "\n"
        "**Unterrichtseinheiten insgesamt: 9**"
    )
    converter = MarkdownConverter(full_example, output_format="detailed")

    assert converter.convert() == expected
