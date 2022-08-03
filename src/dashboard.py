from PyQt5 import uic
from dataBase import database

class Dash:

    def __init__(self, AppWindow):
        #Chamando o self da classe que contem a stack
        self._appWindow = AppWindow

        #Carregando a ui da dashboard
        self._window = uic.loadUi("../uis/TelaDash.ui")

        #Carregando os botoes
        self._buttonPerfil = self._window.buttonPerfil
        self._buttonDeposito = self._window.buttonDeposita
        self._buttonTransferir = self._window.buttonTrans
        self._buttonSaca = self._window.buttonSaca
        self._buttonExtrato = self._window.buttonExtrato

        #Carregando os eventos
        self._load_events()


    @property
    def window(self):
        return self._window

    def _load_events(self):
        #Faz a ligacao dos eventos
        self._buttonPerfil.clicked.connect(lambda: self.perfil())
        self._buttonDeposito.clicked.connect(lambda: self.deposito())
        self._buttonTransferir.clicked.connect(lambda: self.transferir())
        self._buttonSaca.clicked.connect(lambda: self.saque())
        self._buttonExtrato.clicked.connect(lambda: self.extrato())

    def _load_info(self, account):
        #Armazena o cliente no self para outras operações
        self._account = account
        self._window.labelUserDash.setText("Olá, " + self._account.titular.nome)
        self._window.labelSaldo.setText("R$ " + str(self._account.saldo))

    def perfil(self):
        self._appWindow.go_to_perfil(self._account)

    def deposito(self):
        self._appWindow.go_to_deposito(self._account)

    def transferir(self):
        self._appWindow.go_to_transfere(self._account)

    def saque(self):
        self._appWindow.go_to_saque(self._account)

    def extrato(self):
        self._appWindow.go_to_extrato(self._account)