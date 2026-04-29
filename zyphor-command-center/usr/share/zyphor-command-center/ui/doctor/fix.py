from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QPushButton
from PyQt6.QtCore import QProcess


class DoctorFixPage(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        self.setLayout(layout)

        # Console output
        self.console = QTextEdit()
        self.console.setReadOnly(True)

        # Button
        self.btn = QPushButton("Run Doctor Fix")
        self.btn.clicked.connect(self.run_fix)

        # Process handler
        self.process = QProcess()
        self.process.readyReadStandardOutput.connect(self.read_output)
        self.process.readyReadStandardError.connect(self.read_output)

        layout.addWidget(self.btn)
        layout.addWidget(self.console)

    def run_fix(self):
        self.console.clear()
        self.process.start("bash", ["-c", "pkexec zyphor doctor fix"])

    def read_output(self):
        data = self.process.readAllStandardOutput().data().decode()
        err = self.process.readAllStandardError().data().decode()

        if data:
            self.console.append(data)
        if err:
            self.console.append(err)