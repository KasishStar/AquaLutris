import json
import os

DATA_FILE = "data/games.json"


class Storage:
    @staticmethod
    def initialize():
        os.makedirs("data", exist_ok=True)

        if not os.path.exists(DATA_FILE):
            with open(DATA_FILE, "w") as f:
                json.dump([], f)

    @staticmethod
    def load_games():
        Storage.initialize()

        with open(DATA_FILE, "r") as f:
            return json.load(f)

    @staticmethod
    def save_games(games):
        with open(DATA_FILE, "w") as f:
            json.dump(games, f, indent=4)
