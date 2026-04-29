from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QPushButton
from PyQt6.QtCore import QProcess


class PkgListPage(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        self.setLayout(layout)

        # =========================
        # OUTPUT (TERMINAL STYLE)
        # =========================
        self.console = QTextEdit()
        self.console.setReadOnly(True)

        # =========================
        # BUTTON
        # =========================
        self.btn = QPushButton("Refresh Package List")
        self.btn.clicked.connect(self.run_list)

        # =========================
        # PROCESS
        # =========================
        self.process = QProcess()
        self.process.readyReadStandardOutput.connect(self.read_output)
        self.process.readyReadStandardError.connect(self.read_output)

        layout.addWidget(self.btn)
        layout.addWidget(self.console)

        self.run_list()

    # =========================
    # RUN COMMAND
    # =========================
    def run_list(self):
        self.console.clear()
        self.process.start("bash", ["-c", "zyphor pkg list"])

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