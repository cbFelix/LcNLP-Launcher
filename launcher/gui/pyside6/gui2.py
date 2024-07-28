import sys
from PySide6.QtCore import QThread, Signal, Qt
from PySide6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QWidget, QLineEdit, QTextEdit, QPushButton,
                               QLabel, QComboBox, QSpinBox, QDoubleSpinBox, QHBoxLayout, QGridLayout, QSizePolicy,
                               QDialog, QDialogButtonBox)
from PySide6.QtGui import QFont
from launcher.generators.ai.NLP_Generator import AdvancedTextGenerator
from launcher.utils.devices.device_manager import DeviceManager

class TextGeneratorThread(QThread):
    update_text = Signal(str)

    def __init__(self, prompt, generator, max_length, temperature, top_k, top_p, repetition_penalty):
        super().__init__()
        self.prompt = prompt
        self.generator = generator
        self.max_length = max_length
        self.temperature = temperature
        self.top_k = top_k
        self.top_p = top_p
        self.repetition_penalty = repetition_penalty

    def run(self):
        generated_text = self.generator.generate_text(
            self.prompt,
            max_length=self.max_length,
            temperature=self.temperature,
            top_k=self.top_k,
            top_p=self.top_p,
            repetition_penalty=self.repetition_penalty
        )
        self.update_text.emit(generated_text)

class ConfigDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.setStyleSheet("background-color: #2e2e2e; color: #ffffff;")
        self.setFixedSize(400, 600)

        layout = QVBoxLayout(self)

        self.model_selector = QComboBox()
        self.model_selector.addItems(['gpt2', 'gpt2-medium', 'gpt2-large', 'gpt2-xl', 'EleutherAI/gpt-neo-1.3B',
                                      'EleutherAI/gpt-neo-2.7B', 'EleutherAI/gpt-neo-125M', 'EleutherAI/gpt-j-6B',
                                      'distilgpt2'])
        layout.addWidget(QLabel("Model:"))
        layout.addWidget(self.model_selector)

        self.device_selector = QComboBox()
        self.device_selector.addItems(DeviceManager()._get_available_devices())
        layout.addWidget(QLabel("Device:"))
        layout.addWidget(self.device_selector)

        self.max_length_spinner = QSpinBox()
        self.max_length_spinner.setRange(1, 4096)
        self.max_length_spinner.setValue(50)
        layout.addWidget(QLabel("Max Length:"))
        layout.addWidget(self.max_length_spinner)

        self.temperature_spinner = QDoubleSpinBox()
        self.temperature_spinner.setRange(0.1, 2.0)
        self.temperature_spinner.setValue(1.0)
        self.temperature_spinner.setSingleStep(0.1)
        layout.addWidget(QLabel("Temperature:"))
        layout.addWidget(self.temperature_spinner)

        self.top_k_spinner = QSpinBox()
        self.top_k_spinner.setRange(0, 100)
        self.top_k_spinner.setValue(50)
        layout.addWidget(QLabel("Top-k:"))
        layout.addWidget(self.top_k_spinner)

        self.top_p_spinner = QDoubleSpinBox()
        self.top_p_spinner.setRange(0.0, 1.0)
        self.top_p_spinner.setValue(0.95)
        self.top_p_spinner.setSingleStep(0.05)
        layout.addWidget(QLabel("Top-p:"))
        layout.addWidget(self.top_p_spinner)

        self.repetition_penalty_spinner = QDoubleSpinBox()
        self.repetition_penalty_spinner.setRange(1.0, 2.0)
        self.repetition_penalty_spinner.setValue(1.0)
        self.repetition_penalty_spinner.setSingleStep(0.1)
        layout.addWidget(QLabel("Repetition Penalty:"))
        layout.addWidget(self.repetition_penalty_spinner)

        for i in range(layout.count()):
            item = layout.itemAt(i).widget()
            if isinstance(item, QLabel):
                item.setStyleSheet("color: #ffffff;")
            elif isinstance(item, QComboBox) or isinstance(item, QSpinBox) or isinstance(item, QDoubleSpinBox):
                item.setStyleSheet("background-color: #3e3e3e; color: #ffffff; border: none;")

        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        layout.addWidget(self.buttons)

class ChatWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("LcNLP-Launcher")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("background-color: #1e1e1e; color: #ffffff;")
        self.init_ui()

        self.generator = AdvancedTextGenerator(model_name='gpt2', device_id='cpu')
        self.max_length = 50
        self.temperature = 1.0
        self.top_k = 50
        self.top_p = 0.95
        self.repetition_penalty = 1.0

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)

        # Кнопка для открытия настроек
        settings_button = QPushButton("Settings")
        settings_button.setStyleSheet("""
            QPushButton {
                background-color: #4e4e4e; 
                color: #ffffff; 
                padding: 10px;
                border: none;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #5e5e5e;
            }
            QPushButton:pressed {
                background-color: #3e3e3e;
            }
        """)
        settings_button.clicked.connect(self.open_settings)
        main_layout.addWidget(settings_button, alignment=Qt.AlignRight)

        # Поле для отображения сообщений
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        self.chat_display.setStyleSheet("background-color: #2e2e2e; color: #ffffff; height: 270px;")
        self.chat_display.setFont(QFont("Arial", 12))

        # Поле для ввода текста
        self.input_field = QLineEdit()
        self.input_field.setStyleSheet("background-color: #3e3e3e; color: #ffffff; padding: 10px;")
        self.input_field.setPlaceholderText("Type your message here...")
        self.input_field.setFont(QFont("Arial", 12))
        self.input_field.returnPressed.connect(self.send_message)

        # Кнопка отправки
        send_button = QPushButton("Send")
        send_button.setStyleSheet("""
            QPushButton {
                background-color: #4e4e4e; 
                color: #ffffff; 
                padding: 10px;
                border: none;
                font-size: 14px;
                height: 30px;
            }
            QPushButton:hover {
                background-color: #5e5e5e;
            }
            QPushButton:pressed {
                background-color: #3e3e3e;
            }
        """)
        send_button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        send_button.clicked.connect(self.send_message)

        main_layout.addWidget(self.chat_display)
        main_layout.addWidget(self.input_field)
        main_layout.addWidget(send_button)

    def open_settings(self):
        dialog = ConfigDialog(self)
        if dialog.exec():
            self.update_model(dialog.model_selector.currentText())
            self.update_device(dialog.device_selector.currentText())
            self.max_length = dialog.max_length_spinner.value()
            self.temperature = dialog.temperature_spinner.value()
            self.top_k = dialog.top_k_spinner.value()
            self.top_p = dialog.top_p_spinner.value()
            self.repetition_penalty = dialog.repetition_penalty_spinner.value()

    def update_model(self, model_name):
        self.generator.load_model(model_name)

    def update_device(self, device_id):
        self.generator.set_device(device_id)
        self.generator.model.to(self.generator.device)

    def send_message(self):
        user_text = self.input_field.text()
        if user_text:
            self.chat_display.append(f"<b>You:</b> {user_text}")
            self.input_field.clear()

            self.thread = TextGeneratorThread(
                user_text,
                self.generator,
                max_length=self.max_length,
                temperature=self.temperature,
                top_k=self.top_k,
                top_p=self.top_p,
                repetition_penalty=self.repetition_penalty
            )
            self.thread.update_text.connect(self.display_generated_text)
            self.thread.start()

    def display_generated_text(self, generated_text):
        self.chat_display.append(f"<b>AI:</b> {generated_text}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ChatWindow()
    window.show()
    sys.exit(app.exec())
