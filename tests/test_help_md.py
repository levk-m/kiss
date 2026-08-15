from kiss_editor.data.help_md import HELP


def test_help_is_nonempty_string():
    assert isinstance(HELP, str)
    assert HELP.strip()


def test_help_contains_expected_sections():
    for section in (
        "## Command Palette",
        "## Configuration",
        "### Available application themes",
        "### Available editor themes",
        "## Keybindings",
    ):
        assert section in HELP
