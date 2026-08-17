from pathlib import Path

from textual.screen import Screen

from kiss_editor.commands import SearchProvider


class FakeApp:
    def __init__(self, folder):
        self.folder = folder

    def action_help(self):
        pass

    def action_edit_config(self):
        pass

    def edit_file(self, path):
        pass


class FakeScreen(Screen):
    app = None


def make_provider(folder):
    FakeScreen.app = FakeApp(Path(folder))
    return SearchProvider(FakeScreen())


def test_read_all_files_recursive_skips_hidden(sample_dir):
    provider = make_provider(sample_dir)
    names = sorted(p.name for p in provider.read_all_files())
    assert names == ["deep.md", "hello.py", "notes.txt"]


def test_read_all_files_empty_dir(tmp_path):
    provider = make_provider(tmp_path)
    assert provider.read_all_files() == []


async def test_discover_yields_help_and_config(sample_dir):
    provider = make_provider(sample_dir)
    hits = [hit async for hit in provider.discover()]
    assert [h.display for h in hits] == ["Help", "Edit config"]


async def test_search_finds_file_and_builtins(sample_dir):
    provider = make_provider(sample_dir)
    hits = [h async for h in provider.search("hello")]
    assert len(hits) == 1
    assert "hello.py" in hits[0].match_display.plain
    assert hits[0].help == "Open file in KISS"


async def test_search_matches_help(sample_dir):
    provider = make_provider(sample_dir)
    displays = [h.match_display.plain async for h in provider.search("help")]
    assert any("Help" in d for d in displays)


async def test_search_matches_edit_config(sample_dir):
    provider = make_provider(sample_dir)
    displays = [h.match_display.plain async for h in provider.search("config")]
    assert any("Edit config" in d for d in displays)


async def test_search_returns_nothing_for_miss(sample_dir):
    provider = make_provider(sample_dir)
    hits = [h async for h in provider.search("zzz-no-match-zzz")]
    assert hits == []
