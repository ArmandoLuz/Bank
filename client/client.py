import socket

class Client:

    def __init__(self):
        #Definindo o host e a porta
        self._host = 'localhost'
        self._port = 8000
        #Criando novo socket
        self._client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #Criando um endereço para o socket
        self._addr = (self._host, self._port)
    
    def communication(self):
        #Conectando ao servidor
        self._client_socket.connect(self._addr)

    def send(self, command):
        #Enviando um comando ao servidor
        self._client_socket.send(command)
        #Recebendo a resposta do servidor
        return self._client_socket.recv(1024).decode()

    @property
    def return_(self):
        return self._return_
