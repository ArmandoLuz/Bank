from PyQt5 import uic
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QWidget

class Extrato:

    def __init__(self, AppWindow):

        #Chamando a classe que contem a stack
        self._appWindow = AppWindow

        #Carregando a ui da tela de extrato
        self._window = uic.loadUi("../uis/TelaExtrato.ui")

        #Carregando os botoes
        self._buttonBackExtra = self._window.buttonBackExtra

        #Carregando os eventos
        self._load_events()

    @property
    def window(self):
        return self._window
    
    def _load_events(self):
        #Faz a ligacao dos eventos
        self._buttonBackExtra.clicked.connect(lambda: self.back())
    
    def _load_info(self, account):
        self._account = account
        self._load_data(self._account)

    def _load_data(self, account):
        extrato = account.historico.historico()
        self._vbox = QVBoxLayout()
        self._widget = QWidget()
        for t in extrato:
            label = QLabel(text=t)
            label.setStyleSheet("color: rgb(122, 82, 208);")
            self._vbox.addWidget(label)
        
        self._widget.setLayout(self._vbox)


        self._window.scrollArea.setWidget(self._widget)
    def back(self):
        #Faz o retorno para a dashboard
        self._appWindow.go_to(3)