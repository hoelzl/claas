from tempfile import TemporaryDirectory

from claas.__main__ import main_generate_outputs


def test_main_function():
    with TemporaryDirectory() as temp_dir:
        main_generate_outputs("tests/full_example.xml", ["markdown"], temp_dir)
        with open(f"{temp_dir}/full_example.md") as f:
            content = f.read()
        assert content == (
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
            "### abschnitt 2\n"
            "\n"
            "- Thema 2 Inhalt (5 UE)"
        )
