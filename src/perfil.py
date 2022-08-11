from PyQt5 import uic
from dataBase import db

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
        self._user = db.search(cpf)
        self._account = db.search_account(cpf)
        self._window.perfilConta.setText("Conta: " + str(self._account[0][0]))
        self._window.emailPerfil.setText("Email: " + self._user[0][3])
        self._window.nomePerfil.setText(self._user[0][1] + ' ' + self._user[0][2])

    def back(self):
        #Faz o retorno para a dashboard
        self._appWindow.go_to(3)
    
    def exit(self):
        #Faz o retorno para a tela de login
        self._appWindow.go_to(0)