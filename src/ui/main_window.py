from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QListWidget,
    QPushButton, QLabel, QFileDialog, QFrame,
    QLineEdit, QComboBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
import os

from src.core.game_manager import GameManager
from src.widgets.game_banner import GameBanner


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.manager = GameManager()

        self.setWindowTitle("🌊 AquaLutris Alpha 0.6")
        self.resize(1500, 850)

        self.setStyleSheet("""
        QWidget {
            background-color: #09111f;
            color: white;
            font-size: 14px;
        }

        QFrame#Sidebar {
            background-color: #111b30;
            border-radius: 20px;
        }

        QListWidget {
            background-color: #16233d;
            border: none;
            border-radius: 14px;
            padding: 8px;
        }

        QLineEdit {
            background-color: #16233d;
            border: none;
            border-radius: 14px;
            padding: 12px;
            color: white;
        }

        QComboBox {
            background-color: #16233d;
            border-radius: 12px;
            padding: 10px;
        }

        QPushButton {
            background-color: #2563eb;
            border: none;
            border-radius: 14px;
            padding: 12px;
            font-weight: bold;
            color: white;
        }

        QPushButton:hover {
            background-color: #3b82f6;
        }

        QLabel#Title {
            font-size: 34px;
            font-weight: bold;
        }
        """)

        self.build_ui()

    def build_ui(self):
        root = QHBoxLayout(self)

        sidebar_frame = QFrame()
        sidebar_frame.setObjectName("Sidebar")

        sidebar = QVBoxLayout()

        self.logo = QLabel()

        logo = QPixmap("assets/logo.png")

        if not logo.isNull():
            self.logo.setPixmap(
                logo.scaled(
                    150,
                    150,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
            )

        self.logo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.search = QLineEdit()
        self.search.setPlaceholderText("Search Games...")

        self.game_list = QListWidget()

        self.add_button = QPushButton("➕ Add Game")
        self.launch_button = QPushButton("🚀 Launch Game")
        self.favorite_button = QPushButton("⭐ Toggle Favorite")

        sidebar.addWidget(self.logo)
        sidebar.addWidget(self.search)
        sidebar.addWidget(self.game_list)
        sidebar.addWidget(self.add_button)
        sidebar.addWidget(self.launch_button)
        sidebar.addWidget(self.favorite_button)

        sidebar_frame.setLayout(sidebar)

        self.preview = QWidget()
        preview_layout = QVBoxLayout(self.preview)

        self.banner = GameBanner()

        self.title = QLabel("🌊 AquaLutris")
        self.title.setObjectName("Title")
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.runner_label = QLabel("Runner")
        self.runner_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.runner_box = QComboBox()
        self.runner_box.addItems([
            "native",
            "wine"
        ])

        self.info = QLabel(
            "Select a game from your library."
        )
        self.info.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        preview_layout.addWidget(self.banner)
        preview_layout.addWidget(self.title)
        preview_layout.addWidget(self.runner_label)
        preview_layout.addWidget(self.runner_box)
        preview_layout.addWidget(self.info)

        root.addWidget(sidebar_frame, 1)
        root.addWidget(self.preview, 3)

        self.refresh_games()

        self.add_button.clicked.connect(self.add_game)
        self.launch_button.clicked.connect(self.launch_game)
        self.favorite_button.clicked.connect(
            self.toggle_favorite
        )

        self.game_list.currentRowChanged.connect(
            self.update_preview
        )

        self.runner_box.currentTextChanged.connect(
            self.save_runner
        )

    def refresh_games(self):
        self.game_list.clear()

        self.manager.reload()

        for game in self.manager.games:
            prefix = ""

            if game.get("favorite", False):
                prefix = "⭐ "

            self.game_list.addItem(
                prefix + game["name"]
            )

    def add_game(self):
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Game"
        )

        if not path:
            return

        name = os.path.basename(path)

        for ext in [
            ".AppImage",
            ".exe",
            ".app"
        ]:
            name = name.replace(ext, "")

        self.manager.add_game(
            name,
            path
        )

        self.refresh_games()

    def launch_game(self):
        row = self.game_list.currentRow()

        if row >= 0:
            self.manager.launch_game(row)

    def toggle_favorite(self):
        row = self.game_list.currentRow()

        if row >= 0:
            self.manager.toggle_favorite(row)
            self.refresh_games()

    def save_runner(self):
        row = self.game_list.currentRow()

        if row < 0:
            return

        self.manager.set_runner(
            row,
            self.runner_box.currentText()
        )

    def update_preview(self, row):
        if row < 0:
            return

        game = self.manager.games[row]

        self.title.setText(
            game["name"]
        )

        self.runner_label.setText(
            f"Runner: {game.get('runner', 'native')}"
        )

        self.runner_box.setCurrentText(
            game.get(
                "runner",
                "native"
            )
        )

        self.info.setText(
            game["path"]
        )

        self.banner.load_image(
            game.get(
                "cover",
                f"covers/{game['name']}.png"
            )
        )
