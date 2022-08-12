import webbrowser

import pyautogui
from PySide6 import QtCore
from PySide6.QtWidgets import (QMainWindow, QHBoxLayout, QWidget, QVBoxLayout)
from PySide6.QtCore import (QSize,)

from Manager.Manager import Manager
from GUI.customs import (
    AccountButton,
    AddAccountButton,
    ConfigureButton,
    DeleteAccountButton,
    RefreshButton,
    GithubButton,
    AddAccountModal,
    DeleteAccountModal
)
from utils import debug

class GUIManager(QMainWindow):

    WIDTH = 600
    HEIGHT = 600

    def __init__(self):
        super(GUIManager, self).__init__()
        self.manager = Manager()

        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinimizeButtonHint)
        self.setWindowTitle("LeagueClientManager")
        screen_size = pyautogui.size()
        self.setGeometry((screen_size[0] - self.WIDTH)//2,
                        (screen_size[1] - self.HEIGHT)//2,
                        self.WIDTH,
                        self.HEIGHT)

        self.setUpUI()

    def setUpUI(self):
        layout = QHBoxLayout()
        self.AccountsWidget = QWidget()
        self.OptionsWidget = QWidget()
        mainWidget = QWidget()

        self.AccountsWidget.setMinimumSize(QSize(375, 510))
        self.AccountsWidget.setLayout(self.setUpAccounts())

        self.OptionsWidget.setLayout(self.setUpOptions())

        layout.addWidget(self.AccountsWidget)
        layout.addWidget(self.OptionsWidget)

        mainWidget.setLayout(layout)
        self.setCentralWidget(mainWidget)

    def setUpAccounts(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 40)
        for name, data in self.manager.data.items():
            acc = AccountButton(name, data['login'], data['password'])
            acc.clicked.connect(self.acc_clicked)
            layout.addWidget(acc)

        layout.addStretch()
        return layout

    def setUpOptions(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(40, 0, 0, 40)
        add_button = AddAccountButton()
        add_button.clicked.connect(self.add_account_modal)
        layout.addWidget(add_button)

        delete_button = DeleteAccountButton()
        delete_button.clicked.connect(self.delete_account_modal)
        layout.addWidget(delete_button)

        refresh_button = RefreshButton()
        refresh_button.clicked.connect(self.refresh)
        layout.addWidget(refresh_button)

        # TODO: add posibility to change language
        # layout.addWidget(ConfigureButton())

        github_link = GithubButton()
        github_link.clicked.connect(self.open_github)
        layout.addWidget(github_link)

        layout.addStretch()
        return layout

    def acc_clicked(self):
        login, password = self.sender().login, self.sender().password
        debug(f'Login: {login} Password: {password}')
        self.manager.run(login, password)

    def closeEvent(self, event):
        self.manager.cleanupProcesses()
        event.accept()

    def add_account_modal(self):
        dialog = AddAccountModal(self)
        dialog.exec_()
        self.refresh()

    def delete_account_modal(self):
        dialog = DeleteAccountModal(self)
        dialog.exec_()
        self.refresh()
    
    def refresh(self):
        self.manager.sort_data()
        self.setUpUI()

    def open_github(self):
        webbrowser.open('https://github.com/Ematerasu/LeagueClientManager')
