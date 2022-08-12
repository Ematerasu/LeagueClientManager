import sys

from PySide6.QtWidgets import QApplication

from GUI.main_window import GUIManager


if __name__ == '__main__':

    app = QApplication(sys.argv)
    gui = GUIManager()
    gui.show()
    with open('GUI\\stylesheets.qss', 'r') as f:
        style = f.read()
        app.setStyleSheet(style)
    sys.exit(app.exec())
