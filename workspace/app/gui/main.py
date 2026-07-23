import sys
from pathlib import Path

from nicegui import ui


sys.path.append(str(Path(__file__).parent.parent.parent))

from app.gui.pages.subs.editor import SubsEditorPage
from app.gui.pages.subs.table import subs_table_page
from app.gui.pages.home import home_page
from app.gui.pages.oggs import oggs_page
from app.gui.pages.tts import tts_page
from app.gui.pages.settings import settings_page


@ui.page("/")
def index():
    home_page()


@ui.page("/subs")
def subtitles():
    subs_table_page()


@ui.page("/subs/{sub_id:int}")
def sub_editor(sub_id: int):
    SubsEditorPage(sub_id).render_page


@ui.page("/oggs")
def oggs():
    oggs_page()


@ui.page("/tts")
def tts():
    tts_page()


@ui.page("/settings")
def settings():
    settings_page()


ui.run(
    title="KCD2 localization",
    favicon="🎙️",
    reload=True,
    dark=True,
)
