from conta import Conta, Cliente

#Definicao de contas e clientes
cli1 = Cliente("Armando", "Luz", "123-1")
cli2 = Cliente("Teste", "Teste", "123-2")
c1 = Conta("123-1", cli1, 100, 0)
c2 = Conta("124-2", cli2, 0, 0)

#-----------------------Aula 3-------------------------#
#Atividade 1 / Criacao dos metodos e atributos
c1.deposita(10.0)
c1.saca(5.0)
c1.extrato()

#Atividade 2 / criacao da classe transfere
c1.transfere(c2, 50)
c1.extrato()
c2.extrato()

#Atividade 3 / implementação de histórico
c1.historico.imprime()
#---------------------FIM--------------------------------#

#----------------------Aula 4----------------------------#
#Atividade 1 / implementar modificadores de acesso

#atividade 2 / implementar um contador de contas
print(c1.getTotalContas())
print(c2.getTotalContas())

#Atividade 3 / criar slots na classe
