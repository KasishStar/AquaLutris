from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QComboBox,
    QPushButton,
    QMessageBox
)

from src.database.storage import Storage


class SettingsWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("⚙ AquaLutris Settings")
        self.resize(400, 250)

        self.settings = Storage.load_settings()

        layout = QVBoxLayout(self)

        title = QLabel("⚙ AquaLutris Settings")
        layout.addWidget(title)

        layout.addWidget(
            QLabel("Default Runner")
        )

        self.runner = QComboBox()

        self.runner.addItems([
            "native",
            "wine"
        ])

        self.runner.setCurrentText(
            self.settings.get(
                "default_runner",
                "native"
            )
        )

        layout.addWidget(self.runner)

        self.save_button = QPushButton(
            "Save Settings"
        )

        layout.addWidget(
            self.save_button
        )

        self.save_button.clicked.connect(
            self.save_settings
        )

    def save_settings(self):
        self.settings["default_runner"] = (
            self.runner.currentText()
        )

        Storage.save_settings(
            self.settings
        )

        QMessageBox.information(
            self,
            "Saved",
            "Settings saved successfully."
        )
