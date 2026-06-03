import subprocess


class RunnerManager:
    @staticmethod
    def launch(game):

        runner = game.get("runner", "native")

        if runner == "native":
            subprocess.Popen([game["path"]])

        elif runner == "wine":
            subprocess.Popen(
                ["wine", game["path"]]
            )

        else:
            subprocess.Popen([game["path"]])
