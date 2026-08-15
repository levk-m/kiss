from textual.widgets import Label

from kiss_editor.screens import StartScreen


async def test_start_screen_shows_ascii_art(app):
    the_app, pilot = app
    await the_app.push_screen(StartScreen())
    await pilot.pause()
    assert isinstance(the_app.screen, StartScreen)
    screen = the_app.screen
    label = screen.query_one(Label)
    content = str(label.content)
    assert "__ __" in content
    assert "/_/ |_/" in content
