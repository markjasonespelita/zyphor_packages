from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QPushButton
from PyQt6.QtCore import QProcess


class DoctorScanPage(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        self.setLayout(layout)

        # Console output
        self.console = QTextEdit()
        self.console.setReadOnly(True)

        # Button
        self.btn = QPushButton("Run System Scan")
        self.btn.clicked.connect(self.run_scan)

        # Process handler
        self.process = QProcess()
        self.process.readyReadStandardOutput.connect(self.read_output)
        self.process.readyReadStandardError.connect(self.read_output)

        layout.addWidget(self.btn)
        layout.addWidget(self.console)

    def run_scan(self):
        self.console.clear()
        self.process.start("bash", ["-c", "zyphor doctor scan"])

    def read_output(self):
        data = self.process.readAllStandardOutput().data().decode()
        err = self.process.readAllStandardError().data().decode()

        if data:
            self.console.append(data)
        if err:
            self.console.append(err)