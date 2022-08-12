from PySide6.QtWidgets import (
    QPushButton,
    QDialog,
    QFormLayout,
    QLineEdit,
    QDialogButtonBox,
    QVBoxLayout,
    QLabel,
    QCheckBox
)
from PySide6.QtCore import QSize, Qt
from PySide6 import QtGui

class AccountButton(QPushButton):

    def __init__(self, name, login, password):
        super(AccountButton, self).__init__()
        self.setText(name)
        self.login = login
        self.password = password
        self.setFixedSize(QSize(355, 40))
        self.setCursor(QtGui.QCursor(Qt.PointingHandCursor))

    def __repr__(self):
        return f'{self.login}_{self.password}'


class OptionsButtonBase(QPushButton):

    def setup(self, text):
        self.setText(text)
        self.setFixedSize(QSize(205, 50))
        self.setCursor(QtGui.QCursor(Qt.PointingHandCursor))

class AddAccountButton(OptionsButtonBase):

    def __init__(self):
        super(AddAccountButton, self).__init__()
        self.setup('Add account')


class DeleteAccountButton(OptionsButtonBase):

    def __init__(self):
        super(DeleteAccountButton, self).__init__()
        self.setup('Delete account')


class RefreshButton(OptionsButtonBase):

    def __init__(self):
        super(RefreshButton, self).__init__()
        self.setup('Refresh')


class ConfigureButton(OptionsButtonBase):

    def __init__(self):
        super(ConfigureButton, self).__init__()
        self.setup('Configure')


class GithubButton(OptionsButtonBase):
    def __init__(self):
        super(GithubButton, self).__init__()
        self.setup('Source code')

class AddAccountModal(QDialog):

    def __init__(self, parent):
        super(AddAccountModal, self).__init__(parent)
        self.manager = parent.manager
        self.setModal(True)
        self.setWindowTitle("Add Account")

        # fields we want to get from form
        self.name = QLineEdit()
        self.login = QLineEdit()
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)

        self.message = QLabel('')

        self.setUpForm()
    
    def setUpForm(self):
        formLayout = QFormLayout()
        formLayout.addRow("Name:", self.name)
        formLayout.addRow("Login:", self.login)
        formLayout.addRow("Password:", self.password)
        formLayout.addRow(self.message)

        buttons = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.save)
        buttons.rejected.connect(self.cancel)

        formLayout.addRow(buttons)

        self.setLayout(formLayout)

    def save(self):
        name = self.name.text()
        login = self.login.text()
        password = self.password.text()

        if name != '' and login != '' and password != '':
            self.manager.save_account(name, login, password)
            self.close()
        else:
            self.message.setText('All fields are required!')

    def cancel(self):
        self.close()


class DeleteAccountModal(QDialog):
    def __init__(self, parent):
        super(DeleteAccountModal, self).__init__(parent)
        self.manager = parent.manager
        self.setModal(True)
        self.setWindowTitle("Delete Account")
        self.checkboxes = []

        self.setUpUI()
    
    def setUpUI(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 40)
        for name in self.manager.data.keys():
            box = QCheckBox(name, self)
            self.checkboxes.append(box)
            layout.addWidget(box)

        buttons = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.save)
        buttons.rejected.connect(self.cancel)

        layout.addWidget(buttons)

        self.setLayout(layout)

    def save(self):
        to_be_deleted = []

        for box in self.checkboxes:
            if box.isChecked():
                to_be_deleted.append(box.text())
        
        self.manager.delete_accounts(to_be_deleted)
        self.close()

    def cancel(self):
        self.close()
