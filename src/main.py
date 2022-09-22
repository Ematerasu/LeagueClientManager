import os
import sys

from PySide6.QtWidgets import QApplication

from GUI.main_window import GUIManager

if __name__ == '__main__':

    # if folder for json's doesn't exist -> create it
    if not os.path.exists(os.path.relpath('config')):
        os.mkdir('config')

    app = QApplication(sys.argv)
    gui = GUIManager()
    gui.show()
    with open('GUI\\stylesheets.qss', 'r') as f:
        style = f.read()
        app.setStyleSheet(style)
    sys.exit(app.exec())
