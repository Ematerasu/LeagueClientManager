import sys
import os
import re
import win32api

from PySide6.QtWidgets import QApplication

from GUI.main_window import GUIManager
from config import CONFIGS

def find_dir(root_folder, rex):
    for root,dirs,files in os.walk(root_folder):
        for d in dirs:
            result = rex.search(d)
            if result:
                return os.path.join(root, d)
    return False

def find_in_all_drives(file_name):
    #create a regular expression for the file
    rex = re.compile(file_name)
    for drive in win32api.GetLogicalDriveStrings().split('\000')[:-1]:
        x = find_dir( drive, rex )
        if x:
            return x

if __name__ == '__main__':

    # if folder for json's doesn't exist -> create it
    if not os.path.exists(os.path.relpath('config')):
        os.mkdir('config')
    if not os.path.isfile(CONFIGS):
        with open(CONFIGS, 'w') as f:
            path = find_in_all_drives('Riot Games')
            f.write(path+'\\')
    with open(CONFIGS, 'r') as f:
        path = f.read()
        RIOT_GAMES_PATH = path
    app = QApplication(sys.argv)
    gui = GUIManager()
    gui.show()
    with open('GUI\\stylesheets.qss', 'r') as f:
        style = f.read()
        app.setStyleSheet(style)
    sys.exit(app.exec())
