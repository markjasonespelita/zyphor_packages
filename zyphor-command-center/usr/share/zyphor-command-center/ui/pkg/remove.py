from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QTextEdit,
    QPushButton, QLineEdit, QMessageBox
)
from PyQt6.QtCore import QProcess


class PkgRemovePage(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        self.setLayout(layout)

        # =========================
        # INPUT
        # =========================
        self.input = QLineEdit()
        self.input.setPlaceholderText("Enter app name to remove")

        # =========================
        # BUTTON
        # =========================
        self.btn = QPushButton("Remove Package")
        self.btn.clicked.connect(self.confirm_remove)

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
    # CONFIRM (GUI REPLACES CLI PROMPT FLOW)
    # =========================
    def confirm_remove(self):
        app = self.input.text().strip()

        if not app:
            self.console.append("Zyphor: ✖ Missing app name\n")
            return

        reply = QMessageBox.question(
            self,
            "Confirm Removal",
            f"Remove '{app}' from system?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            self.run_remove(app)

    # =========================
    # RUN COMMAND (SAFE FOR read -p BLOCKING)
    # =========================
    def run_remove(self, app):
        self.console.clear()

        # IMPORTANT:
        # We simulate terminal input "y" to satisfy read -p if it appears
        cmd = f"printf 'y\\n' | pkexec zyphor pkg remove {app}"

        self.process.start("bash", ["-c", cmd])

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