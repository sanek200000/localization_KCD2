from nicegui import ui


class AudioPlaylist:
    def __init__(self) -> None:
        self._players: list[ui.audio] = list()

    def add(self, player: ui.audio):
        self._players.append(player)

    def start(self):
        if self._players:
            self._play(0)

    def _play(self, index: int):
        if index >= len(self._players):
            return

        player = self._players[index]

        player.run_method("pause")
        player.run_method("load")
        player.run_method("play")

        player.on("ended.once", lambda _, i=index + 1: self._play(i))
