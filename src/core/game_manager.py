from src.database.storage import Storage
from src.core.cover_manager import CoverManager
from src.core.runner_manager import RunnerManager


class GameManager:
    def __init__(self):
        self.games = Storage.load_games()

    def add_game(self, name, path):
        game = {
            "name": name,
            "path": path,
            "favorite": False,
            "runner": "native",
            "cover": CoverManager.get_cover_path(name),
            "description": "",
            "platform": "Linux",
            "version": "Unknown"
        }

        self.games.append(game)
        Storage.save_games(self.games)

    def toggle_favorite(self, index):
        self.games[index]["favorite"] = not self.games[index].get(
            "favorite",
            False
        )

        Storage.save_games(self.games)

    def set_runner(self, index, runner):
        self.games[index]["runner"] = runner
        Storage.save_games(self.games)

    def launch_game(self, index):
        RunnerManager.launch(
            self.games[index]
        )

    def reload(self):
        self.games = Storage.load_games()
