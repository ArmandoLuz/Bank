from PyQt5 import uic

class Recovery:
    def __init__(self, appWindow):
        
        #Carregando o self da classe que contem a stack
        self._appWindow = appWindow
        #Carregando a ui da dashboard
        self._window = uic.loadUi("../uis/TelaRecuperacao.ui")

        #Carregando os LineEdits
        self._inputEmail = self._window.inputEmailRec

        #Carregando os botoes
        self._buttonRec = self._window.buttonRec
        self._buttonBack = self._window.buttonBackRec

        #Carregando os eventos
        self._load_events()

    @property
    def window(self):
        #Retorna a janela atual
        return self._window

    def _load_events(self):
        #Faz a ligacao dos eventos
        self._buttonRec.clicked.connect(lambda: self.recovery())
        self._buttonBack.clicked.connect(lambda: self.back())

    def recovery(self):
        #Faz a recuperação de senha

        #Seta o label de status
        self._window.labelConfirEmail.setText("Email de recuperação enviado!")
        self._inputEmail.setText("")

    def back(self):
        #Faz o retorno para a tela de login
        self._window.labelConfirEmail.setText("")
        self._appWindow.go_to(0)