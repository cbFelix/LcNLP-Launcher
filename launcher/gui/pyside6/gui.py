import sys
from PySide6.QtCore import QThread, Signal, Qt
from PySide6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QWidget, QLineEdit, QTextEdit, QPushButton,
                               QLabel, QComboBox, QSpinBox, QDoubleSpinBox, QHBoxLayout, QGridLayout, QSizePolicy)
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

class ChatWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("LcNLP-Launcher")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("background-color: #1e1e1e; color: #ffffff;")
        self.init_ui()

        self.generator = AdvancedTextGenerator(model_name='gpt2', device_id='cpu')

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)

        config_layout = QGridLayout()
        config_layout.setContentsMargins(0, 0, 0, 20)

        self.model_selector = QComboBox()
        self.model_selector.addItems(['gpt2', 'gpt2-medium', 'gpt2-large', 'gpt2-xl'])
        self.model_selector.currentTextChanged.connect(self.update_model)
        config_layout.addWidget(QLabel("Model:"), 0, 0)
        config_layout.addWidget(self.model_selector, 0, 1)

        self.device_selector = QComboBox()
        self.device_selector.addItems(DeviceManager()._get_available_devices())
        self.device_selector.currentTextChanged.connect(self.update_device)
        config_layout.addWidget(QLabel("Device:"), 0, 2)
        config_layout.addWidget(self.device_selector, 0, 3)

        self.max_length_spinner = QSpinBox()
        self.max_length_spinner.setRange(1, 1024)
        self.max_length_spinner.setValue(50)
        config_layout.addWidget(QLabel("Max Length:"), 1, 0)
        config_layout.addWidget(self.max_length_spinner, 1, 1)

        self.temperature_spinner = QDoubleSpinBox()
        self.temperature_spinner.setRange(0.1, 2.0)
        self.temperature_spinner.setValue(1.0)
        self.temperature_spinner.setSingleStep(0.1)
        config_layout.addWidget(QLabel("Temperature:"), 1, 2)
        config_layout.addWidget(self.temperature_spinner, 1, 3)

        self.top_k_spinner = QSpinBox()
        self.top_k_spinner.setRange(0, 100)
        self.top_k_spinner.setValue(50)
        config_layout.addWidget(QLabel("Top-k:"), 2, 0)
        config_layout.addWidget(self.top_k_spinner, 2, 1)

        self.top_p_spinner = QDoubleSpinBox()
        self.top_p_spinner.setRange(0.0, 1.0)
        self.top_p_spinner.setValue(0.95)
        self.top_p_spinner.setSingleStep(0.05)
        config_layout.addWidget(QLabel("Top-p:"), 2, 2)
        config_layout.addWidget(self.top_p_spinner, 2, 3)

        self.repetition_penalty_spinner = QDoubleSpinBox()
        self.repetition_penalty_spinner.setRange(1.0, 2.0)
        self.repetition_penalty_spinner.setValue(1.0)
        self.repetition_penalty_spinner.setSingleStep(0.1)
        config_layout.addWidget(QLabel("Repetition Penalty:"), 3, 0)
        config_layout.addWidget(self.repetition_penalty_spinner, 3, 1)

        for i in range(config_layout.count()):
            item = config_layout.itemAt(i).widget()
            if isinstance(item, QLabel):
                item.setStyleSheet("color: #ffffff;")
            elif isinstance(item, QComboBox) or isinstance(item, QSpinBox) or isinstance(item, QDoubleSpinBox):
                item.setStyleSheet("background-color: #3e3e3e; color: #ffffff; border: none;")

        # Поле для отображения сообщений
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        self.chat_display.setStyleSheet("background-color: #2e2e2e; color: #ffffff;")
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

        main_layout.addLayout(config_layout)
        main_layout.addWidget(self.chat_display)
        main_layout.addWidget(self.input_field)
        main_layout.addWidget(send_button)

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
                max_length=self.max_length_spinner.value(),
                temperature=self.temperature_spinner.value(),
                top_k=self.top_k_spinner.value(),
                top_p=self.top_p_spinner.value(),
                repetition_penalty=self.repetition_penalty_spinner.value()
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
