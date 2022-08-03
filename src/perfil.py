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

    def _load_info(self, account):
        #Carregando as informacoes do perfil
        self._window.perfilConta.setText("Conta: " + str(account.numero))
        self._window.emailPerfil.setText("Email: " + account.titular.email)
        self._window.nomePerfil.setText(account.titular.nome + ' ' + account.titular.sobrenome)

    def back(self):
        #Faz o retorno para a dashboard
        self._appWindow.go_to(3)
    
    def exit(self):
        #Faz o retorno para a tela de login
        self._appWindow.go_to(0)