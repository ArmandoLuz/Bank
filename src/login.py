from PyQt5 import uic
import hashlib
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
        status = False

        #Encriptando a senha
        password = hashlib.md5(senha.encode()).hexdigest()
        
        #Chamando a função de login
        status = db.login(cpf, password)

        #Seta o label de status
        if status == True:
            self._window.labelLoginStatus.setText("")
            self._window.inputCPFLogin.setText("")
            self._window.inputSenhaLogin.setText("")
            self._appWindow.go_to_dash(cpf)
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
