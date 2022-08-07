#Imports
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QStackedLayout

from login import Login
from recovery import Recovery
from register import Register
from dashboard import Dash
from perfil import Perfil
from deposito import Deposito
from transfere import Transfere
from sacar import Saque 
from extrato import Extrato
#APP

class AppWindow(QMainWindow):
    def __init__(self):
        super(AppWindow, self).__init__()
        self._stack = QStackedLayout()

        #Instanciando as telas
        self._login = Login(self)
        self._recovery = Recovery(self)
        self._register = Register(self)
        self._dash = Dash(self)
        self._perfil = Perfil(self)
        self._deposito = Deposito(self)
        self._transfere = Transfere(self)
        self._saque = Saque(self)
        self._extrato = Extrato(self)
        
        #Adicionando as telas na stack
        self._stack.addWidget(self._login.window)
        self._stack.addWidget(self._recovery.window)
        self._stack.addWidget(self._register.window)
        self._stack.addWidget(self._dash.window)
        self._stack.addWidget(self._perfil.window)
        self._stack.addWidget(self._deposito.window)
        self._stack.addWidget(self._transfere.window)
        self._stack.addWidget(self._saque.window)
        self._stack.addWidget(self._extrato.window)

    def go_to(self, id):
        self._stack.setCurrentIndex(id)

    def go_to_dash(self, account):
        self._dash._load_info(account)
        self.go_to(3)
    
    def go_to_perfil(self, client):
        self._perfil._load_info(client)
        self.go_to(4)
    
    def go_to_deposito(self, account):
        self._deposito._load_info(account)
        self.go_to(5)
    
    def go_to_transfere(self, account):
        self._transfere._load_info(account)
        self.go_to(6)

    def go_to_saque(self, account):
        self._saque._load_info(account)
        self.go_to(7)

    def go_to_extrato(self, account):
        self._extrato._load_info(account)
        self.go_to(8)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = AppWindow()
    sys.exit(app.exec_())
        
