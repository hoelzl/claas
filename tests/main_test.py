from tempfile import TemporaryDirectory

from claas.__main__ import main_generate_outputs


def test_main_function_summary():
    with TemporaryDirectory() as temp_dir:
        main_generate_outputs(
            "tests/full_example.xml",
            ["markdown"],
            temp_dir,
            skip_time=True,
            kinds=["summary"],
        )
        with open(f"{temp_dir}/full_example_summary.md") as f:
            content = f.read()
        assert content == (
            "# Kurs Titel\n"
            "\n"
            "## Modul 1 Titel\n"
            "\n"
            "Modul 1 Beschreibung\n"
            "\n"
            "- Zusammenfassung 1\n"
            "\n"
            "### Abschnitt 1\n"
            "\n"
            "### Woche 1: Wocheninhalt 1\n"
            "\n"
            "- Zusammenfassung 2\n"
            "- Zusammenfassung 3\n"
            "- Zusammenfassung 4"
        )


def test_main_function_detailed():
    with TemporaryDirectory() as temp_dir:
        main_generate_outputs(
            "tests/full_example.xml",
            ["markdown"],
            temp_dir,
            skip_time=False,
            kinds=["detailed"],
        )
        with open(f"{temp_dir}/full_example_detailed.md") as f:
            content = f.read()
        assert content == (
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
