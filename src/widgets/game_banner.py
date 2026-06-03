from PyQt6.QtWidgets import QLabel
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt


class GameBanner(QLabel):
    def __init__(self):
        super().__init__()

        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def load_image(self, path):
        pixmap = QPixmap(path)

        if pixmap.isNull():
            self.setText("No Artwork")
            return

        self.setPixmap(
            pixmap.scaled(
                500,
                300,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
        )
