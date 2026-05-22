import sys
from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow

app = QApplication(sys.argv)

# CARREGAR ESTILO
with open("assets/style.qss", "r", encoding="utf-8") as file:
    app.setStyleSheet(file.read())

window = MainWindow()
window.show()

sys.exit(app.exec())