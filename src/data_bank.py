import random
from conta import Conta


class Data_bank:

    __slots__ = ["_lista_contas"]

    def __init__(self):
        self._lista_contas = {}

    #Faz o cadastro do usuário
    def cadastra(self, cliente):

        existe = self.busca(cliente.cpf)

        if existe == False:
            return False
        else:
            self._lista_contas[existe] = Conta(existe,cliente)
            return True

    #Verifica se o usuário existe e gera um número de conta caso não exista
    def busca(self, cpf):
        if len(self._lista_contas.keys()) > 0:
            for num in self._lista_contas.keys():
                
                if self._lista_contas[num].titular.cpf == cpf:
                    return False
                else:
                    while True:
                        numero = random.randint(100000000, 999999999)
                        if numero not in self._lista_contas.keys():
                            return numero
        else:
            numero = random.randint(100000000, 999999999)
            return numero

    #Busca um usuário pelo numero                    
    def busca_user(self, num):
        if num in self._lista_contas.keys():
            return self._lista_contas[num]
        else:
            return None

    @property
    def lista_contas(self):
        return self._lista_contas