from functools import partial

from textual.command import Provider, Hits, Hit
from pathlib import Path


class SearchProvider(Provider):
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

        if matcher.match("help") > 0:
            yield Hit(
                score=0.5,
                match_display=matcher.highlight("help"),
                command=partial(self.app.action_help),
                help="Show help page",
            )
