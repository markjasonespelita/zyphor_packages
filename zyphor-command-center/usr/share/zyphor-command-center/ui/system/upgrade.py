from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QTextEdit
from core.process import ProcessManager

class UpgradePage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.console = QTextEdit()
        self.console.setReadOnly(True)

        self.process = ProcessManager(self.console.append)

        btn = QPushButton("Run System Upgrade")
        btn.clicked.connect(self.run)

        layout.addWidget(btn)
        layout.addWidget(self.console)

    def run(self):
        self.console.clear()
        self.process.run("pkexec zyphor system upgrade")