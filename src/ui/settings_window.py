from PyQt6.QtWidgets import QWidget,QVBoxLayout,QLabel,QComboBox,QPushButton

class SettingsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('AquaLutris Settings')

        layout = QVBoxLayout(self)

        layout.addWidget(QLabel('⚙ AquaLutris Settings'))

        self.runner = QComboBox()
        self.runner.addItems(['native', 'wine', 'gptk'])

        layout.addWidget(QLabel('Default Runner'))
        layout.addWidget(self.runner)

        layout.addWidget(QPushButton('Save'))
