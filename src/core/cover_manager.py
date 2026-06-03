import os


class CoverManager:
    @staticmethod
    def get_cover_path(game_name):
        return f"covers/{game_name}.png"

    @staticmethod
    def ensure_cover_folder():
        os.makedirs("covers", exist_ok=True)
