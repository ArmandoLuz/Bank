from PyQt5 import uic

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

    def _load_info(self, cpf):
        #Construindo o comando
        command = "9,{}".format(cpf)
        #Enviando o comando para o servidor
        self._name = self._appWindow.client.send(command.encode())
        #Construindo o comando
        command = "10,{}".format(cpf)
        #Enviando o comando para o servidor
        self._saldo = self._appWindow.client.send(command.encode())
        self._cpf = cpf
        #Exibindo as informações do usuário
        self._window.labelUserDash.setText("Olá, " + self._name)
        self._window.labelSaldo.setText("R$ " + str(self._saldo))

    def perfil(self):
        self._appWindow.go_to_perfil(self._cpf)

    def deposito(self):
        self._appWindow.go_to_deposito(self._cpf)

    def transferir(self):
        self._appWindow.go_to_transfere(self._cpf)

    def saque(self):
        self._appWindow.go_to_saque(self._cpf)

    def extrato(self):
        self._appWindow.go_to_extrato(self._cpf)