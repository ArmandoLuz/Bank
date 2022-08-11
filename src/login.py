from PyQt5 import uic
from dataBase import db

class Login:
    def __init__(self, appWindow):
        
        #Carregando o self da classe que contem a stack
        self._appWindow = appWindow
        #Carregando a ui da dashboard
        self._window = uic.loadUi("../uis/TelaLogin.ui")

        #Chamando os lineEdits da tela de login
        self._cpf = self._window.inputCPFLogin
        self._senha = self._window.inputSenhaLogin

        #Chamando os botoes da tela de login
        self._login_btn = self._window.buttonLogin
        self._recovery = self._window.buttonEsqSenha
        self._register = self._window.buttonNoClient

        #Carregando os eventos
        self._load_events()

    @property
    def window(self):
        #Retorna a janela atual
        return self._window
    
    def _load_events(self):
        #Faz a ligacao dos eventos
        self._login_btn.clicked.connect(lambda: self.login())
        self._recovery.clicked.connect(lambda: self.recovery_password())
        self._register.clicked.connect(lambda: self.register_user())

    def login(self):
        #Coletando as informações do usuário
        cpf = self._cpf.text()
        senha = self._senha.text()

        #Verificando a senha e entrando na dashboard
        status = 1
        user = db.search(cpf)

        if len(user) != 0:
            if senha == user[0][-1]:
                self._window.inputCPFLogin.setText("")
                self._window.inputSenhaLogin.setText("")
                status = 0
                self._appWindow.go_to_dash(cpf)

        #Seta o label de status
        if status == 0:
            self._window.labelLoginStatus.setText("")
        else:
            self._window.labelLoginStatus.setText("CPF ou senha incorretos!")
        

    def recovery_password(self):
        #Reseta os campos
        self._window.labelLoginStatus.setText("")
        self._senha.setText("")
        self._cpf.setText("")
        #Chama a tela de recuperacao da senha.
        self._appWindow.go_to(1)

    def register_user(self):
        #Reseta os campos
        self._window.labelLoginStatus.setText("")
        self._senha.setText("")
        self._cpf.setText("")
        
        #Faz o cadastro de usuário
        self._appWindow.go_to(2)
