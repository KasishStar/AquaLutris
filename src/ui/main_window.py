from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QListWidget,
    QPushButton, QLabel, QFileDialog, QMessageBox,
    QFrame, QLineEdit
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
        self.current_view = "library"

        self.setWindowTitle("🌊 AquaLutris Alpha 0.3")
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

        QLabel#Info {
            color: #cbd5e1;
        }
        """)

        self.build_ui()

    def build_ui(self):
        root = QHBoxLayout(self)

        sidebar_frame = QFrame()
        sidebar_frame.setObjectName("Sidebar")

        sidebar = QVBoxLayout()

        self.logo = QLabel()
        logo = QPixmap("/home/kasish/Documents/Projects/AquaLutrisLogo.png")

        if not logo.isNull():
            self.logo.setPixmap(
                logo.scaled(
                    150, 150,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
            )

        self.logo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.search = QLineEdit()
        self.search.setPlaceholderText("Search Games...")

        self.library_btn = QPushButton("🏠 Library")
        self.favorite_btn = QPushButton("⭐ Favorites")
        self.installed_btn = QPushButton("🎮 Installed")
        self.settings_btn = QPushButton("⚙ Settings")

        self.game_list = QListWidget()

        self.add_button = QPushButton("➕ Add Game")
        self.launch_button = QPushButton("🚀 Launch Game")

        sidebar.addWidget(self.logo)
        sidebar.addWidget(self.search)
        sidebar.addWidget(self.library_btn)
        sidebar.addWidget(self.favorite_btn)
        sidebar.addWidget(self.installed_btn)
        sidebar.addWidget(self.settings_btn)
        sidebar.addWidget(self.game_list)
        sidebar.addWidget(self.add_button)
        sidebar.addWidget(self.launch_button)

        sidebar_frame.setLayout(sidebar)

        self.preview = QWidget()
        preview_layout = QVBoxLayout(self.preview)

        self.banner = GameBanner()

        self.title = QLabel("🌊 AquaLutris")
        self.title.setObjectName("Title")
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.runner = QLabel("Runner: Native")
        self.runner.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.favorite_label = QLabel("Favorite: No")
        self.favorite_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.info = QLabel("Select a game from your library.")
        self.info.setObjectName("Info")
        self.info.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.favorite_toggle = QPushButton("⭐ Toggle Favorite")

        preview_layout.addStretch()
        preview_layout.addWidget(self.banner)
        preview_layout.addWidget(self.title)
        preview_layout.addWidget(self.runner)
        preview_layout.addWidget(self.favorite_label)
        preview_layout.addWidget(self.info)
        preview_layout.addWidget(self.favorite_toggle)
        preview_layout.addStretch()

        root.addWidget(sidebar_frame, 1)
        root.addWidget(self.preview, 3)

        self.refresh_games()

        self.add_button.clicked.connect(self.add_game)
        self.launch_button.clicked.connect(self.launch_game)
        self.favorite_toggle.clicked.connect(self.toggle_favorite)
        self.game_list.currentRowChanged.connect(self.update_preview)

    def refresh_games(self):
        self.game_list.clear()
        self.manager.reload()

        for game in self.manager.games:
            prefix = "⭐ " if game.get("favorite", False) else ""
            self.game_list.addItem(prefix + game["name"])

    def add_game(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select Game")

        if not path:
            return

        name = os.path.basename(path)

        for ext in [".AppImage", ".exe", ".app"]:
            name = name.replace(ext, "")

        self.manager.add_game(name, path)
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

    def update_preview(self, row):
        if row < 0 or row >= len(self.manager.games):
            return

        game = self.manager.games[row]

        self.title.setText(game["name"])
        self.runner.setText(f"Runner: {game.get('runner', 'native')}")
        self.favorite_label.setText(
            f"Favorite: {'Yes' if game.get('favorite', False) else 'No'}"
        )
        self.info.setText(game["path"])

        self.banner.load_image(
            game.get("cover", f"covers/{game['name']}.png")
        )
