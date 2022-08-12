import mysql.connector

class Database:

    def __init__(self):
        #Estabelecendo uma conexão com o database previamente criado.
        self._conection = mysql.connector.connect(host='localhost', 
                                                    user='root', 
                                                    password='******', 
                                                    auth_plugin = 'mysql_native_password', 
                                                    database='bank')
        self._cursor = self._conection.cursor()

        #Criando todas as tabelas e relações do database
        self._cursor.execute("""CREATE TABLE IF NOT EXISTS users(
                                    CPF VARCHAR(11) PRIMARY KEY NOT NULL,
                                    Name VARCHAR(25) NOT NULL, Last_name VARCHAR(35) NOT NULL, 
                                    email VARCHAR(35) NOT NULL, Password VARCHAR(45) NOT NULL
                                    )
                                ENGINE = InnoDB;""")

        self._cursor.execute("""CREATE TABLE IF NOT EXISTS accounts(
                                    id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
                                    users_CPF VARCHAR(11) NOT NULL, 
                                    saldo FLOAT UNSIGNED NOT NULL,
                                    UNIQUE INDEX id_UNIQUE (id ASC) VISIBLE,
                                    INDEX fk_accounts_users_idx (users_CPF ASC) VISIBLE,
                                    CONSTRAINT fk_account_users FOREIGN KEY (users_CPF) REFERENCES bank.users (CPF)
                                    ON DELETE NO ACTION
                                    ON UPDATE NO ACTION
                                )
                                ENGINE = InnoDB
                                AUTO_INCREMENT = 10000;""")
        
        self._cursor.execute("""CREATE TABLE IF NOT EXISTS historic(
                                    id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
                                    accounts_id INT UNSIGNED NOT NULL,
                                    info VARCHAR(100) NOT NULL,
                                    UNIQUE INDEX id_UNIQUE (id ASC) VISIBLE,
                                    INDEX fk_historic_accounts_idx (accounts_id ASC) VISIBLE,
                                    CONSTRAINT fk_historic_accounts FOREIGN KEY (accounts_id) REFERENCES bank.accounts (id)
                                    ON DELETE NO ACTION
                                    ON UPDATE NO ACTION
                                )
                                ENGINE = InnoDB;""")
        
        self._conection.commit()
    
    #Função que busca registros existentes através de um CPF.
    def search(self, CPF):
        self._cursor.execute("SELECT * FROM users WHERE users.CPF = %s", (CPF,))
        return list(self._cursor)

    #Função que busca contas através do CPF.
    def search_account(self, cpf):
        self._cursor.execute("SELECT id, saldo FROM bank.users, bank.accounts WHERE users.CPF = %s AND accounts.users_CPF = users.CPF", (cpf,))
        return list(self._cursor)

    #Função que busca o saldo de uma conta através do seu número.
    def get_saldo(self, num):
        self._cursor.execute("SELECT saldo FROM bank.accounts WHERE accounts.id = %s", (num,))
        return list(self._cursor)

    #Função que adiciona um registro ao banco de dados.
    def register(self, CPF, name, last_name, email, password):
        #Busca o registro
        status = self.search(CPF)
        
        #Verifica se o registro não existe.
        if len(status) == 0:
            #Insere um novo registro
            self._cursor.execute("INSERT INTO bank.users (CPF, Name, Last_name, email, Password) VALUES (%s, %s, %s, %s, %s);", (CPF, name, last_name, email, password))
            self._cursor.execute("INSERT INTO bank.accounts (users_CPF, saldo) VALUES (%s, %s);", (CPF, 0.0))
            self._conection.commit()
            return True

        else:
            return False

    #Função de transferência de saldo.
    def trasnfer(self, cpf, num, value):

        #Pessquisando uma conta através do CPF
        account = self.search_account(cpf)
        #Coletando o saldo de uma conta atrés do seu número
        saldo_destino = self.get_saldo(num)

        #Verificando se há saldo suficiente e se a conta de destino existe
        if account[0][1] > value and len(saldo_destino) != 0:

            #Depositando o valor na conta de destino
            self._cursor.execute("UPDATE bank.accounts SET saldo = %s WHERE accounts.id = %s", (saldo_destino[0][-1] + value, num))
            
            #Subtraindo valor da conta de origem
            self._cursor.execute("UPDATE bank.accounts SET saldo = %s WHERE accounts.users_CPF = %s", (account[0][-1] - value, cpf))
            
            #Adicionando registro ao histórico da conta de origem
            info = "Transferência de R$ {} para a conta {}".format(value, num)
            self._cursor.execute("INSERT INTO bank.historic (accounts_id, info) VALUES (%s, %s)", (account[0][0], info))

            #Adicionando registro ao histórico da conta de destino
            info = "Depósito de R$ {} da conta {}".format(value, account[0][0])
            self._cursor.execute("INSERT INTO bank.historic (accounts_id, info) VALUES (%s, %s)", (num, info)) 

            self._conection.commit()
            return "Transferência realizada com sucesso!"

        else:
            return "Saldo insuficiente ou conta inexistente."

    #Função de depósito
    def deposit(self, cpf, value):
        #Pesquisa uma conta pelo CPF
        account = self.search_account(cpf)

        #Realiza o depósito
        self._cursor.execute("UPDATE bank.accounts SET saldo = %s WHERE accounts.users_CPF = %s", (account[0][-1] + value, cpf))

        #Adiciona um registro ao histórico
        info = "Depósito de R$ {}".format(value)
        self._cursor.execute("INSERT INTO bank.historic (accounts_id, info) VALUES (%s, %s)", (account[0][0], info))

        self._conection.commit()
        return "Depósito realizado com sucesso!"

    def withdraw(self, cpf, value):
        #Pesquisa uma conta pelo CPF
        account = self.search_account(cpf)
        
        #Verifica se há saldo disponível
        if account[0][-1] >= value:
            #Realizando o saque
            self._cursor.execute("UPDATE bank.accounts SET saldo = %s WHERE accounts.users_CPF = %s", (account[0][-1] - value, cpf))

            #Adicionando um registro
            info = "Saque de R$ {}".format(value)
            self._cursor.execute("INSERT INTO bank.historic (accounts_id, info) VALUES (%s, %s)", (account[0][0], info))

            self._conection.commit()

            return "Saque realizado com sucesso!"
        else:
            return "Saldo insuficiente!"

    #Retorna o histórico de uma conta
    def extract(self, cpf):
        self._cursor.execute("SELECT bank.historic.id, info FROM bank.historic, bank.users, bank.accounts WHERE users.CPF = %s AND accounts.users_CPF = users.CPF AND historic.accounts_id = accounts.id", (cpf,))
        return list(self._cursor)

db = Database()
