from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt

class HomePage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.setLayout(layout)

        label = QLabel("Welcome to Zyphor Command Center")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(label)