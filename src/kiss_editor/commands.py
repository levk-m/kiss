from functools import partial
from typing import TYPE_CHECKING, cast

from textual.command import DiscoveryHit, Hit, Hits, Provider

if TYPE_CHECKING:
    from kiss_editor.app import Kiss


class SearchProvider(Provider):
    @property
    def app(self) -> "Kiss":
        return cast("Kiss", super().app)

    def read_all_files(self):
        result = []
        folders = [self.app.folder]
        while folders:
            folder = folders.pop()
            for file in folder.iterdir():
                if file.name.startswith((".", "_")):
                    # skip
                    continue
                if file.is_dir():
                    folders.append(file)
                else:
                    result.append(file)
        return result

    async def discover(self) -> Hits:
        yield DiscoveryHit(
            display="Help",
            command=partial(self.app.action_help),
            help="Show help page",
        )
        yield DiscoveryHit(
            display="Edit config",
            command=partial(self.app.action_edit_config),
            help="Open KISS config",
        )

    async def search(self, query: str) -> Hits:
        matcher = self.matcher(query)
        for path in self.read_all_files():
            command = str(path)
            score = matcher.match(command)
            if score > 0:
                yield Hit(
                    score=score,
                    match_display=matcher.highlight(command),
                    command=partial(self.app.edit_file, path),
                    help="Open file in KISS",
                )

        if matcher.match("Help") > 0:
            yield Hit(
                score=0.5,
                match_display=matcher.highlight("Help"),
                command=partial(self.app.action_help),
                help="Show help page",
            )
        if matcher.match("Edit config") > 0:
            yield Hit(
                score=0.5,
                match_display=matcher.highlight("Edit config"),
                command=partial(self.app.action_edit_config),
                help="Open KISS config",
            )
