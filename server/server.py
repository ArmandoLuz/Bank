import socket
from dataBase import db
import threading

class Server:

    def __init__(self):
        #Definindo o host e a porta
        self._host = ''
        self._port = 8001
        #Criando novo socket
        self._serv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #Criando um endereço para o socket
        self._addr = (self._host, self._port)
        #Criando uma estrutura para armazenar as operações
        self._operations = {'1':db.register, '2':db.trasnfer, '3':db.deposit, 
                            '4':db.withdraw, '5':db.extract, '6':db.login, '7':db.search,
                            '8':db.search_account, '9':db.get_name, '10':db.get_saldo_cpf, 
                            '11':db.get_email, '12':db.get_num, '13':db.get_last_name}
        

    def conection(self):
        #Vinculando o socket ao endereço
        self._serv_socket.bind(self._addr)

        #Rodando o socket em modo escuta
        while True:
            #Habilitando o servidor para aceitar conexões
            self._serv_socket.listen(6)
            print("Aguardando conexões...")
            #Aceitando conexões
            self._conection, self._client_address = self._serv_socket.accept()
            #Criando uma nova thread para a conexão
            new_thread = Comunication(self._client_address, self._conection, self._operations)
            new_thread.start()

class Comunication(threading.Thread):
    def __init__(self, client_address, client_socket, operations):
        threading.Thread.__init__(self)
        self._csocket = client_socket
        self._client_address = client_address
        self._operations = operations
        print("Nova conexão iniciada: ", client_address)

    def run(self):
        while True:
           
            try:
                #Recebendo comando
                operation = self._csocket.recv(1024).decode()
                #Particionando o comando
                operation = operation.split(',')
                print(operation)
                #Executando o comando
                return_ = self._operations[operation[0]](operation[1:])
                print(return_)
                #Enviando a resposta
                self._csocket.send(return_.encode())
            
            except:
                print("Conexão encerrada")
                self._csocket.close()
                break 

if __name__=="__main__":
    server = Server()
    server.conection()
