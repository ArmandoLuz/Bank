from PyQt5 import uic
from conta import Cliente
from dataBase import db

class Register:
    def __init__(self, AppWindow):
        #Carregando o self da classe que contem a stack
        self._appWindow = AppWindow

        #Carregando a ui da dashboard
        self._window = uic.loadUi("../uis/TelaCadastro.ui")

        #Carregando os LineEdits
        self._nome = self._window.inputNomeCad
        self._sobrenome = self._window.inputSobreCad
        self._cpf = self._window.inputCpfCad
        self._email = self._window.inputEmailCad
        self._senha = self._window.inputSenhaCad

        #carregando os botoes
        self._buttonCad = self._window.buttonCad
        self._buttonBack = self._window.buttonBackCad

        self._load_events()

    @property
    def window(self):
        #Retorna a janela atual
        return self._window

    def _load_events(self):
        #Faz a ligacao dos eventos
        self._buttonCad.clicked.connect(lambda: self.register())
        self._buttonBack.clicked.connect(lambda: self.back())

    def register(self):
        #Coletando as informacoes
        nome = self._nome.text()
        sobrenome = self._sobrenome.text()
        cpf = self._cpf.text()
        email = self._email.text()
        senha = self._senha.text()

        #Inserindo no banco de dados
        status = db.register(cpf, nome, sobrenome, email, senha)

        #Verificando o status da operação.
        if status == True:
            self._window.labelAvisoCad.setText("Cadastro realizado com sucesso!")
            self._nome.setText("")
            self._sobrenome.setText("")
            self._cpf.setText("")
            self._email.setText("")
            self._senha.setText("")
        else:
            self._window.labelAvisoCad.setText("Usuário já existe!")
            self._nome.setText("")
            self._sobrenome.setText("")
            self._cpf.setText("")
            self._email.setText("")
            self._senha.setText("")
    #Voltando para a tela de login
    def back(self):
        #reseta os campos 
        self._window.labelAvisoCad.setText("")
        self._nome.setText("")
        self._sobrenome.setText("")
        self._cpf.setText("")
        self._email.setText("")
        self._senha.setText("")

        #Volta para a tela de login
        self._appWindow.go_to(0)
            


        