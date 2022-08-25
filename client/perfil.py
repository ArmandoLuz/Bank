from PyQt5 import uic

class Perfil:
    def __init__(self, AppWindow):
        #Chamando o self da classe que contem a stack
        self._appWindow = AppWindow

        #Carregando a ui da dashboard
        self._window = uic.loadUi("../uis/TelaPerfil.ui")

        #Carregando os botoes
        self._buttonBack = self._window.button_back_perfil
        self._buttonExit = self._window.buttonExit

        #Carregando os eventos
        self._load_events()

    @property
    def window(self):
        return self._window
    
    def _load_events(self):
        #Faz a ligacao dos eventos
        self._buttonBack.clicked.connect(lambda: self.back())
        self._buttonExit.clicked.connect(lambda: self.exit())

    def _load_info(self, cpf):
        #Carregando as informacoes do perfil
        #Construindo o comando
        command = '9,{}'.format(cpf)
        #Enviando o comando para o servidor
        self._name = self._appWindow.client.send(command.encode())
        #construindo o comando
        command = '11,{}'.format(cpf)
        #Enviando o comando para o servidor
        self._email = self._appWindow.client.send(command.encode())
        #construindo o comando
        command = '12,{}'.format(cpf)
        #Enviando o comando para o servidor
        self._num = self._appWindow.client.send(command.encode())
        #construindo o comando
        command = '13,{}'.format(cpf)
        #Enviando o comando para o servidor
        self._lastname = self._appWindow.client.send(command.encode())
        #Exibição dos dados no perfil
        self._window.perfilConta.setText("Conta: " + self._num)
        self._window.emailPerfil.setText("Email: " + self._email)
        self._window.nomePerfil.setText(self._name + ' ' + self._lastname)

    def back(self):
        #Faz o retorno para a dashboard
        self._appWindow.go_to(3)
    
    def exit(self):
        #Faz o retorno para a tela de login
        self._appWindow.go_to(0)