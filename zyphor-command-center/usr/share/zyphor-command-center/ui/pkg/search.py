from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QTextEdit,
    QPushButton, QLineEdit
)
from PyQt6.QtCore import QProcess


class PkgSearchPage(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        self.setLayout(layout)

        # =========================
        # INPUT FIELD
        # =========================
        self.input = QLineEdit()
        self.input.setPlaceholderText("Search packages (e.g. firefox, snap, editor)")

        # =========================
        # BUTTON
        # =========================
        self.btn = QPushButton("Search")
        self.btn.clicked.connect(self.run_search)

        # =========================
        # OUTPUT
        # =========================
        self.console = QTextEdit()
        self.console.setReadOnly(True)

        # =========================
        # PROCESS
        # =========================
        self.process = QProcess()
        self.process.readyReadStandardOutput.connect(self.read_output)
        self.process.readyReadStandardError.connect(self.read_output)

        layout.addWidget(self.input)
        layout.addWidget(self.btn)
        layout.addWidget(self.console)

    # =========================
    # RUN SEARCH
    # =========================
    def run_search(self):
        keyword = self.input.text().strip()

        if not keyword:
            self.console.append("Zyphor: ✖ Please enter a search keyword\n")
            return

        self.console.clear()
        self.process.start(
            "bash",
            ["-c", f"zyphor pkg search {keyword}"]
        )

    # =========================
    # OUTPUT HANDLER
    # =========================
    def read_output(self):
        data = self.process.readAllStandardOutput().data().decode()
        err = self.process.readAllStandardError().data().decode()

        if data:
            self.console.append(data)
        if err:
            self.console.append(err)