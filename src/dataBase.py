import mysql.connector

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
        self._cursor.execute("SELECT CPF FROM users WHERE users.CPF = %s", (CPF,))
        return list(self._cursor)

    #Função que adiciona um registro ao banco de dados.
    def register(self, CPF, name, last_name, email, password):
        status = self.search(CPF)

        if len(status) == 0:

            self._cursor.execute("INSERT INTO bank.users (CPF, Name, Last_name, email, Password) VALUES (%s, %s, %s, %s, %s);", (CPF, name, last_name, email, password))
            self._cursor.execute("INSERT INTO bank.accounts (users_CPF, saldo) VALUES (%s, %s);", (CPF, 0.0))
            self._conection.commit()
            return True

        else:
            return False


db = Database()