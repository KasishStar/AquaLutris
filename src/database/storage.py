import json
import os

GAMES_FILE = "data/games.json"
SETTINGS_FILE = "data/settings.json"


class Storage:
    @staticmethod
    def initialize():
        os.makedirs("data", exist_ok=True)

        if not os.path.exists(GAMES_FILE):
            with open(GAMES_FILE, "w") as f:
                json.dump([], f)

        if not os.path.exists(SETTINGS_FILE):
            with open(SETTINGS_FILE, "w") as f:
                json.dump(
                    {
                        "default_runner": "native",
                        "theme": "aqua"
                    },
                    f,
                    indent=4
                )

    @staticmethod
    def load_games():
        Storage.initialize()

        with open(GAMES_FILE, "r") as f:
            return json.load(f)

    @staticmethod
    def save_games(games):
        with open(GAMES_FILE, "w") as f:
            json.dump(
                games,
                f,
                indent=4
            )

    @staticmethod
    def load_settings():
        Storage.initialize()

        with open(SETTINGS_FILE, "r") as f:
            return json.load(f)

    @staticmethod
    def save_settings(settings):
        with open(SETTINGS_FILE, "w") as f:
            json.dump(
                settings,
                f,
                indent=4
            )
