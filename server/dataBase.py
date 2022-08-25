import mysql.connector
import hashlib

class Database:

    def __init__(self):
        #Estabelecendo uma conexão com o database previamente criado.
        self._conection = mysql.connector.connect(host='localhost', 
                                                    user='root', 
                                                    password='75395AlB', 
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
        self._cursor.execute("SELECT * FROM users WHERE users.CPF = %s", (CPF[0],))
        return list(self._cursor)

    #Função que busca contas através do CPF.
    def search_account(self, cpf):
        self._cursor.execute("SELECT id, saldo FROM bank.users, bank.accounts WHERE users.CPF = %s AND accounts.users_CPF = users.CPF", (cpf,))
        return list(self._cursor)

    #Função que busca o saldo de uma conta através do seu número.
    def get_saldo(self, num):
        self._cursor.execute("SELECT users_CPF, saldo FROM bank.accounts WHERE accounts.id = %s", (num,))
        return list(self._cursor)

    #Função que retorna o saldo de uma conta através do cpf.
    def get_saldo_cpf(self, cpf: list):
        self._cursor.execute("SELECT saldo FROM bank.accounts WHERE users_CPF = %s", (cpf[0],))
        return str(list(self._cursor)[0][0])
    
    #Retorna o nome de um usuário através do CPF
    def get_name(self, cpf: list):
        self._cursor.execute("SELECT Name FROM bank.users WHERE CPF = %s", (cpf[0],))
        return list(self._cursor)[0][0]

    #Retorna o ultimo nome do usuário através do CPF
    def get_last_name(self, cpf):
        self._cursor.execute("SELECT Last_name FROM bank.users WHERE CPF = %s", (cpf[0],))
        return list(self._cursor)[0][0]
    
    #Retorna o email de um usuário através do CPF
    def get_email(self, cpf: list):
        self._cursor.execute("SELECT email FROM bank.users WHERE CPF = %s", (cpf[0],))
        return list(self._cursor)[0][0]
    
    #Retorna o número da conta através do CPF
    def get_num(self, cpf: list):
        self._cursor.execute("SELECT id FROM bank.accounts WHERE users_CPF = %s", (cpf[0],))
        return str(list(self._cursor)[0][0])

    #Função que adiciona um registro ao banco de dados.
    def register(self, credentials: list):
        #Armanzenando as informações
        CPF = credentials[0] 
        name = credentials[1]
        last_name = credentials[2]
        email = credentials[3]
        password = credentials[4]

        #Busca o registro
        status = self.search([CPF])
        
        #Verifica se o registro não existe.
        if len(status) == 0:
            #Insere um novo registro
            self._cursor.execute("INSERT INTO bank.users (CPF, Name, Last_name, email, Password) VALUES (%s, %s, %s, %s, MD5(%s));", (CPF, name, last_name, email, password))
            self._cursor.execute("INSERT INTO bank.accounts (users_CPF, saldo) VALUES (%s, %s);", (CPF, 0.0))
            self._conection.commit()
            return "True"

        else:
            return "False"

    #Função de transferência de saldo.
    def trasnfer(self, crendentials: list):
        #Armanzenando as informações
        cpf = crendentials[0]
        num = int(crendentials[1])
        value = float(crendentials[2])

        #Pesquisando uma conta de origem através do CPF
        account = self.search_account(cpf)

        #Coletando o saldo de uma conta de destino atrés do seu número
        saldo_destino = self.get_saldo(num)

        if len(saldo_destino) == 0 or cpf == saldo_destino[0][0]:
            return "Operação não permitida!"

        #Verificando se há saldo suficiente e se a conta de destino existe
        if account[0][1] > value:

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
    def deposit(self, values: list):
        #Armanzenando as informações
        cpf = values[0]
        value = float(values[1])
        #Pesquisa uma conta pelo CPF
        account = self.search_account(cpf)

        #Realiza o depósito
        self._cursor.execute("UPDATE bank.accounts SET saldo = %s WHERE accounts.users_CPF = %s", (account[0][-1] + value, cpf))

        #Adiciona um registro ao histórico
        info = "Depósito de R$ {}".format(value)
        self._cursor.execute("INSERT INTO bank.historic (accounts_id, info) VALUES (%s, %s)", (account[0][0], info))

        self._conection.commit()
        return "Depósito realizado com sucesso!"

    def withdraw(self, values: list):
        #Armanzenando as informações
        cpf = values[0]
        value = float(values[1])

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
        self._cursor.execute("SELECT info FROM bank.historic, bank.users, bank.accounts WHERE users.CPF = %s AND accounts.users_CPF = users.CPF AND historic.accounts_id = accounts.id", (cpf[0],))
        s=''
        for i in self._cursor:
            s += i[0]+','
        return s

    #Realiza o login
    def login(self, credentials):
        #Armanzenando as credenciais
        cpf = credentials[0]
        password = hashlib.md5(credentials[1].encode()).hexdigest()
        #Pesquisando o usuário
        user = db.search([cpf])

        #Realizando o login
        if len(user) != 0:
            if password == user[0][-1]:
                return "True"
            else:
                return "False"
        else:
            return "False"

db = Database()
