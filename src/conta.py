import datetime

class Conta:

    __slots__ = ['_numero', '_titular', '_saldo', '_limite', '_historico']

    _totalContas = 0

    def __init__(self, numero, cliente, saldo=0.00, limite=1000.0):
        self._numero = numero
        self._titular = cliente
        self._saldo = saldo
        self._limite = limite
        self._historico = Historico()

        Conta._totalContas += 1

    @staticmethod
    def getTotalContas():
        return Conta._totalContas

    def deposita(self, valor):
        if valor <= 0:
            return "Valor invalido!"
        else:
            self._saldo += valor
            self.historico.transacoes.append("Depósito de R$ {}".format(valor))
            return "Depósito realizado com sucesso!"
    
    def saca(self, valor):
        if self._saldo >= valor and valor > 0:
            self._saldo -= valor
            self.historico.transacoes.append("Saque de R$ {}".format(valor))
            return "Saque realizado com sucesso!"
        else:
            return "Saldo insuficiente ou o valor é inválido!"
    
    def extrato(self):
        print("numero: {}\nSaldo: {}".format(self.numero, self._saldo))

    def transfere(self, destino, valor):
        if self._saldo >= valor and valor > 0:
            destino.deposita(valor)
            self._saldo -= valor
            self.historico.transacoes.append("Transferencia de R${} para a conta {}".format(valor, destino.numero))
            destino.historico.transacoes.append("Transferencia de R${} da conta {}".format(valor, self._numero))
            return "Transferencia realizada com sucesso!"
        else:
            return "Saldo insuficiente ou o valor é inválido!"

    @property
    def numero(self):
        return self._numero

    @property
    def titular(self):
        return self._titular
    
    @titular.setter
    def titular(self, titular):
        self._titular = titular

    @property
    def saldo(self):
        return self._saldo

    @property
    def limite(self):
        return self._limite
    
    @limite.setter
    def limite(self, valor):
        self._limite = valor
    
    @property
    def historico(self):
        return self._historico
    
    
class Cliente:
    def __init__(self, nome, sobrenome, cpf, email, senha):
        self._nome = nome
        self._sobrenome = sobrenome
        self._cpf = cpf
        self._email = email
        self._senha = senha

    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, nome):
        self._nome = nome
    
    @property
    def sobrenome(self):
        return self._sobrenome
    
    @sobrenome.setter
    def sobrenome(self, sobrenome):
        self._sobrenome = sobrenome
    
    @property
    def cpf(self):
        return self._cpf

    @cpf.setter
    def cpf(self, cpf):
        self._cpf = cpf

    @property
    def email(self):
        return self._email

    @property
    def senha(self):
        return self._senha


class Historico:
    def __init__(self):
        self.dataAbertura = datetime.datetime.today()
        self.transacoes = []

    def historico(self):
        return self.transacoes