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
    
    def _load_info(self, cpf):
        self._cpf = cpf

    def back(self):
        #Faz o retorno para a dashboard
        self._valor.setText("")
        self._window.labelStatusDep.setText("")

        self._appWindow._dash._load_info(self._cpf)
        self._appWindow.go_to(3)
    
    def deposita(self):
        if self._valor.text() == '' or float(self._valor.text()) <= 0:
            self._window.labelStatusDep.setText("Digite um valor válido!")
            return 0
        else:
            #Construindo o comando
            command = "3,{},{}".format(self._cpf, self._valor.text())
            status = self._appWindow.client.send(command.encode())
            self._window.labelStatusDep.setText(status)
            self._window.inpValDep.setText("")