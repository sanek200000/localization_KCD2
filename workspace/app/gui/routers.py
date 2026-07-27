from nicegui import ui

from app.gui.pages.subs.editor import SubsEditorPage
from app.gui.pages.subs.table import SubsTablePage
from app.gui.pages.home import home_page
from app.gui.pages.oggs import OggsPage
from app.gui.pages.tts import TTSpage
from app.gui.pages.settings import settings_page


@ui.page("/")
def index():
    home_page()


@ui.page("/subs")
def subtitles():
    SubsTablePage().render_page


@ui.page("/subs/{sub_id:int}")
def sub_editor(sub_id: int):
    SubsEditorPage(sub_id).render_page


@ui.page("/oggs")
def oggs():
    OggsPage().render_page


@ui.page("/tts")
def tts():
    TTSpage().reder_page


@ui.page("/settings")
def settings():
    settings_page()
