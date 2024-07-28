import sys

from PySide6.QtWidgets import QApplication

from launcher.gui.pyside6.gui2 import ChatWindow

app = QApplication(sys.argv)
window = ChatWindow()
window.show()
sys.exit(app.exec())