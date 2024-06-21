from tempfile import TemporaryDirectory

from claas.__main__ import main_generate_outputs


def test_main_function():
    with TemporaryDirectory() as temp_dir:
        main_generate_outputs("tests/full_example.xml", ["markdown"], temp_dir)
        with open(f"{temp_dir}/full_example.md") as f:
            content = f.read()
        assert content == (
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
