import sys
from PySide6.QtCore import QThread, Signal, Qt
from PySide6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QWidget, QLineEdit, QTextEdit, QPushButton,
                               QLabel, QComboBox, QSpinBox, QDoubleSpinBox, QHBoxLayout, QDialog,
                               QDialogButtonBox, QCheckBox)
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
    def __init__(self, parent=None, current_settings=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.setStyleSheet("background-color: #2e2e2e; color: #ffffff;")
        self.setFixedSize(400, 650)

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
        layout.addWidget(QLabel("Max Length:"))
        layout.addWidget(self.max_length_spinner)

        self.temperature_spinner = QDoubleSpinBox()
        self.temperature_spinner.setRange(0.1, 2.0)
        self.temperature_spinner.setSingleStep(0.1)
        layout.addWidget(QLabel("Temperature:"))
        layout.addWidget(self.temperature_spinner)

        self.top_k_spinner = QSpinBox()
        self.top_k_spinner.setRange(0, 100)
        layout.addWidget(QLabel("Top-k:"))
        layout.addWidget(self.top_k_spinner)

        self.top_p_spinner = QDoubleSpinBox()
        self.top_p_spinner.setRange(0.0, 1.0)
        self.top_p_spinner.setSingleStep(0.05)
        layout.addWidget(QLabel("Top-p:"))
        layout.addWidget(self.top_p_spinner)

        self.repetition_penalty_spinner = QDoubleSpinBox()
        self.repetition_penalty_spinner.setRange(1.0, 2.0)
        self.repetition_penalty_spinner.setSingleStep(0.1)
        layout.addWidget(QLabel("Repetition Penalty:"))
        layout.addWidget(self.repetition_penalty_spinner)

        # Add Half Model Accuracy checkbox
        self.half_model_accuracy_checkbox = QCheckBox("Half Model Accuracy")
        layout.addWidget(self.half_model_accuracy_checkbox)

        self.load_settings(current_settings)

        for i in range(layout.count()):
            item = layout.itemAt(i).widget()
            if isinstance(item, QLabel):
                item.setStyleSheet("color: #ffffff;")
            elif isinstance(item, QComboBox) or isinstance(item, QSpinBox) or isinstance(item, QDoubleSpinBox) or isinstance(item, QCheckBox):
                item.setStyleSheet("background-color: #3e3e3e; color: #ffffff; border: none;")

        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        layout.addWidget(self.buttons)

    def load_settings(self, settings):
        if settings:
            self.model_selector.setCurrentText(settings['model'])
            self.device_selector.setCurrentText(settings['device'])
            self.max_length_spinner.setValue(settings['max_length'])
            self.temperature_spinner.setValue(settings['temperature'])
            self.top_k_spinner.setValue(settings['top_k'])
            self.top_p_spinner.setValue(settings['top_p'])
            self.repetition_penalty_spinner.setValue(settings['repetition_penalty'])
            self.half_model_accuracy_checkbox.setChecked(settings.get('half_model_accuracy', False))

    def get_settings(self):
        return {
            'model': self.model_selector.currentText(),
            'device': self.device_selector.currentText(),
            'max_length': self.max_length_spinner.value(),
            'temperature': self.temperature_spinner.value(),
            'top_k': self.top_k_spinner.value(),
            'top_p': self.top_p_spinner.value(),
            'repetition_penalty': self.repetition_penalty_spinner.value(),
            'half_model_accuracy': self.half_model_accuracy_checkbox.isChecked()
        }


class ChatWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Initialize settings and generator before calling init_ui
        self.settings = {
            'model': 'gpt2',
            'device': 'cpu',
            'max_length': 50,
            'temperature': 1.0,
            'top_k': 50,
            'top_p': 0.95,
            'repetition_penalty': 1.0,
            'half_model_accuracy': False
        }
        self.generator = AdvancedTextGenerator(model_name=self.settings['model'],
                                               device_id=self.settings['device'],
                                               half_model_accuracy=self.settings['half_model_accuracy'])

        self.setWindowTitle("LcNLP-Launcher")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("background-color: #1e1e1e; color: #ffffff;")
        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)

        # Верхняя панель с названием модели и кнопкой настроек
        header_layout = QHBoxLayout()
        self.model_name_label = QLabel(f"Model: {self.settings['model']}  |  Device: {self.settings['device']}  |  Half Model Accuracy: {self.settings['half_model_accuracy']}")
        self.model_name_label.setStyleSheet("background-color: transparent; color: #ffffff; padding: 10px; border-radius: 10px;")
        header_layout.addWidget(self.model_name_label)

        settings_button = QPushButton("⚙")
        settings_button.setStyleSheet("""
            QPushButton {
                background-color: #3e3e3e; 
                color: #ffffff; 
                padding: 10px;
                border-radius: 10px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #4e4e4e;
            }
            QPushButton:pressed {
                background-color: #2e2e2e;
            }
        """)
        settings_button.setFixedSize(40, 40)
        settings_button.clicked.connect(self.open_settings)
        header_layout.addWidget(settings_button, alignment=Qt.AlignRight)

        main_layout.addLayout(header_layout)

        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        self.chat_display.setStyleSheet("background-color: #2e2e2e; color: #ffffff; border: none;")
        self.chat_display.setFont(QFont("Arial", 12))

        clear_chat_button = QPushButton("Clear")
        clear_chat_button.setStyleSheet("""
            QPushButton {
                background-color: #3e3e3e; 
                color: #ffffff; 
                padding: 10px;
                border-radius: 10px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #4e4e4e;
            }
            QPushButton:pressed {
                background-color: #2e2e2e;
            }
        """)
        clear_chat_button.setFixedSize(40, 40)
        clear_chat_button.clicked.connect(self.clear_chat)

        input_layout = QHBoxLayout()
        self.input_field = QLineEdit()
        self.input_field.setStyleSheet("background-color: #3e3e3e; color: #ffffff; padding: 10px; border-radius: 10px;")
        self.input_field.setPlaceholderText("Type your message here...")
        self.input_field.setFont(QFont("Arial", 12))
        self.input_field.returnPressed.connect(self.send_message)

        clear_chat_button = QPushButton("🧺")
        clear_chat_button.setStyleSheet("""
                    QPushButton {
                        background-color: #3e3e3e; 
                        color: #ffffff; 
                        padding: 10px;
                        border-radius: 10px;
                        font-size: 14px;
                    }
                    QPushButton:hover {
                        background-color: #4e4e4e;
                    }
                    QPushButton:pressed {
                        background-color: #2e2e2e;
                    }
                """)
        clear_chat_button.setFixedSize(40, 40)
        clear_chat_button.clicked.connect(self.clear_chat)

        send_button = QPushButton("➡")
        send_button.setStyleSheet("""
            QPushButton {
                background-color: #3e3e3e; 
                color: #ffffff; 
                padding: 10px;
                border-radius: 10px;
                font-size: 14px;
            }
            QPushButton:hover {
                            background-color: #4e4e4e;
            }
            QPushButton:pressed {
                background-color: #2e2e2e;
            }
        """)
        send_button.setFixedSize(40, 40)
        send_button.clicked.connect(self.send_message)

        input_layout.addWidget(clear_chat_button, alignment=Qt.AlignLeft)
        input_layout.addWidget(self.input_field)
        input_layout.addWidget(send_button, alignment=Qt.AlignRight)

        main_layout.addWidget(self.chat_display)
        main_layout.addLayout(input_layout)

    def open_settings(self):
        dialog = ConfigDialog(self, self.settings)
        if dialog.exec():
            new_settings = dialog.get_settings()
            self.settings.update(new_settings)
            self.update_model(self.settings['model'])
            self.update_device(self.settings['device'])
            self.generator.half_model_accuracy = bool(self.settings['half_model_accuracy'])
            self.update_header()

    def update_model(self, model_name):
        self.generator.load_model(model_name)

    def update_device(self, device_id):
        self.generator.set_device(device_id)
        self.generator.model.to(self.generator.device)

    def update_header(self):
        self.model_name_label.setText(f"Model: {self.settings['model']}  |  Device: {self.settings['device']}  |  Half model accuracy: {self.settings['half_model_accuracy']}")

    def send_message(self):
        user_text = self.input_field.text()
        if user_text:
            self.chat_display.append(f"<b>You:</b> {user_text}")
            self.input_field.clear()

            self.thread = TextGeneratorThread(
                user_text,
                self.generator,
                max_length=self.settings['max_length'],
                temperature=self.settings['temperature'],
                top_k=self.settings['top_k'],
                top_p=self.settings['top_p'],
                repetition_penalty=self.settings['repetition_penalty']
            )
            self.thread.update_text.connect(self.display_generated_text)
            self.thread.start()

    def display_generated_text(self, generated_text):
        self.chat_display.append(f"<b>AI:</b> {generated_text}")

    def clear_chat(self):
        self.chat_display.clear()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ChatWindow()
    window.show()
    sys.exit(app.exec())

