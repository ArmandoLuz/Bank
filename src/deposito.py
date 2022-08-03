from PyQt5 import uic

class Deposito:

    def __init__(self, AppWindow):

        #Chamando o self da classe que contem a stack
        self._appWindow = AppWindow

        #Carregando a ui da tela de deposito
        self._window = uic.loadUi("../uis/TelaDeposito.ui")

        #Carregando os botoes
        self._buttonDep = self._window.buttonDep
        self._buttonBackDep = self._window.buttonBackDep

        #Carregando os lineEdits
        self._valor = self._window.inpValDep

        #Carregando os eventos
        self._load_events()

    @property
    def window(self):
        return self._window

    def _load_events(self):
        #Faz a ligacao dos eventos
        self._buttonDep.clicked.connect(lambda: self.deposita())
        self._buttonBackDep.clicked.connect(lambda: self.back())
    
    def _load_info(self, account):
        self._account = account

    def back(self):
        #Faz o retorno para a dashboard
        self._valor.setText("")
        self._window.labelStatusDep.setText("")

        self._appWindow._dash._load_info(self._account)
        self._appWindow.go_to(3)
    
    def deposita(self):
        if self._valor.text() == '':
            self._window.labelStatusDep.setText("Digite um valor!")
            return 0
        else:
            status = self._account.deposita(float(self._valor.text()))
            self._window.labelStatusDep.setText(status)
            self._window.inpValDep.setText("")