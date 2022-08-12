from PyQt5 import uic
from dataBase import db

class Saque:

    def __init__(self, AppWindow):
        #Chamando o self da classe que contem a stack
        self._appWindow = AppWindow

        #Carregando a ui da tela de saque
        self._window = uic.loadUi("../uis/Saque.ui")

        #Carregando os botoes
        self._back_saque = self._window.button_back_saca
        self._buttonSaque = self._window.buttonSaque

        #Carregando os lineEdits
        self._valor = self._window.inputValorSaque

        #Carregando os eventos
        self._load_events()

    @property
    def window(self):
        #Retorna a janela atual
        return self._window

    def _load_events(self):
        #Faz a ligacao dos eventos
        self._buttonSaque.clicked.connect(lambda: self.saque())
        self._back_saque.clicked.connect(lambda: self.back())

    def _load_info(self, cpf):
        self._cpf = cpf

    def back(self):
        #Reseta os campos
        self._valor.setText("")
        self._window.labelStatusSaque.setText("")
        #Faz o retorno para a dashboard
        self._appWindow._dash._load_info(self._cpf)
        self._appWindow.go_to(3)
    
    def saque(self):
        if self._valor.text() == '' or float(self._valor.text()) <= 0:
            self._window.labelStatusSaque.setText("Digite um valor válido!")

        else:
            status = db.withdraw(self._cpf, float(self._valor.text()))
            self._window.labelStatusSaque.setText(status)
            self._window.inputValorSaque.setText("")