from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QPushButton, QLineEdit
from PyQt6.QtCore import QProcess


class PkgInstallPage(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        self.setLayout(layout)

        # =========================
        # INPUT FIELD (APP NAME)
        # =========================
        self.input = QLineEdit()
        self.input.setPlaceholderText("Enter app name (e.g. firefox, vscode)")

        # =========================
        # BUTTON
        # =========================
        self.btn = QPushButton("Install")
        self.btn.clicked.connect(self.run_install)

        # =========================
        # CONSOLE OUTPUT
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
    # RUN INSTALL
    # =========================
    def run_install(self):
        app = self.input.text().strip()

        if not app:
            self.console.append("Zyphor: ✖ Missing app name\n")
            return

        self.console.clear()

        self.process.start(
            "bash",
            ["-c", f"pkexec zyphor pkg install {app}"]
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