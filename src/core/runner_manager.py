import subprocess

from src.database.storage import Storage


class RunnerManager:
    @staticmethod
    def launch(game):

        settings = Storage.load_settings()

        runner = game.get(
            "runner",
            settings.get(
                "default_runner",
                "native"
            )
        )

        if runner == "native":
            subprocess.Popen(
                [game["path"]]
            )

        elif runner == "wine":
            subprocess.Popen(
                ["wine", game["path"]]
            )

        else:
            subprocess.Popen(
                [game["path"]]
            )
