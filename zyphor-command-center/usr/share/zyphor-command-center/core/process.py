from PyQt6.QtCore import QProcess

class ProcessManager:
    def __init__(self, callback):
        self.callback = callback
        self.process = QProcess()
        self.process.readyReadStandardOutput.connect(self.read_stdout)
        self.process.readyReadStandardError.connect(self.read_stderr)

    def run(self, command):
        self.process.start("bash", ["-c", command])

    def read_stdout(self):
        data = self.process.readAllStandardOutput().data().decode()
        self.callback(data)

    def read_stderr(self):
        data = self.process.readAllStandardError().data().decode()
        self.callback(data)