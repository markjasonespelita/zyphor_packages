from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QPushButton
from PyQt6.QtCore import QProcess


class DoctorReportPage(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.console = QTextEdit()
        self.console.setReadOnly(True)

        self.btn = QPushButton("Generate System Report")
        self.btn.clicked.connect(self.run_report)

        self.process = QProcess()
        self.process.readyReadStandardOutput.connect(self.read_output)
        self.process.readyReadStandardError.connect(self.read_output)
        self.process.finished.connect(self.load_report_file)

        layout.addWidget(self.btn)
        layout.addWidget(self.console)

    def run_report(self):
        self.console.clear()
        self.process.start("bash", ["-c", "pkexec zyphor doctor report"])

    def read_output(self):
        data = self.process.readAllStandardOutput().data().decode()
        err = self.process.readAllStandardError().data().decode()

        if data:
            self.console.append(data)
        if err:
            self.console.append(err)

    def load_report_file(self):
        # Automatically display saved report
        try:
            with open("/tmp/zyphor_doctor_report.txt", "r") as f:
                content = f.read()

            self.console.append("\n\n--- SYSTEM REPORT ---\n")
            self.console.append(content)

        except Exception as e:
            self.console.append(f"\nFailed to read report file: {e}")