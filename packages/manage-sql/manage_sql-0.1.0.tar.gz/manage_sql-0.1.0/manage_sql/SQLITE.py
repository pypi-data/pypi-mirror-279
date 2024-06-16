import sqlite3 as sq
import hashlib as sh
from pathlib import Path

class SQLITE:

    def __init__(self, nomeBanco: str):
        """
        Inicializa a classe com o nome do banco de dados.
        
        :param nomeBanco: Nome do banco de dados a ser utilizado.
        
        Exemplo de uso:
        ```python
        db = SQLITE('meu_banco)
        ```
        """
        self.nomeBanco = nomeBanco

    def conectarBanco(self):
        """
        Conecta ao banco de dados e cria a pasta 'database' se não existir.

        :return: Um objeto de conexão e cursor do banco de dados.
        
        Exemplo de uso:
        ```python
        db = SQLITE('meu_banco')
        database, cursor = db.conectarBanco()
        ```
        """
        path = Path.cwd() / "database"
        path.mkdir(parents=True, exist_ok=True)
        
        database = sq.connect(f'database/{self.nomeBanco}.db')
        cursor = database.cursor()

        return database, cursor

    def criarTabela(self, nomeTabela: str, Colunas: list, ColunasTipo: list):
        
        """
        Cria uma tabela no banco de dados.

        :param nomeTabela: Nome da tabela a ser criada.
        :param Colunas: Lista com os nomes das colunas.
        :param ColunasTipo: Lista com os tipos das colunas.

        Exemplo de uso:
        ```python
        db = SQLITE('meu_banco')
        db.criarTabela(
            nomeTabela='minha_tabela',
            Colunas=['coluna1', 'coluna2'],
            ColunasTipo=['TEXT', 'INTEGER']
        )
        ```
        """
        
        if type(Colunas) == list and type(ColunasTipo) == list:
            if len(Colunas) == len(ColunasTipo):
                database, cursor = self.conectarBanco()
                ListaColunas = []

                for i in range(len(Colunas)):
                    ListaColunas.append(f'{Colunas[i]} {ColunasTipo[i]}')

                ColunaSQL = ','.join(ListaColunas)

                cursor.execute(f'CREATE TABLE IF NOT EXISTS {nomeTabela} (id INTEGER PRIMARY KEY AUTOINCREMENT,{ColunaSQL})')

                database.commit()
                database.close()
            else:
                print('Impossível criar tabelas: quantidade de colunas e tipos não coincide.')
        else:
            print('Impossível criar tabelas: parâmetros devem ser listas.')

    def inserirDados(self, nomeTabela: str, Colunas: list, dados: list):
        """
        Insere dados em uma tabela do banco de dados.

        :param nomeTabela: Nome da tabela onde os dados serão inseridos.
        :param Colunas: Lista com os nomes das colunas.
        :param dados: Lista com os valores a serem inseridos.
        
        Exemplo de uso:
        ```python
        db = SQLITE('meu_banco')
        db.inserirDados(
            nomeTabela='minha_tabela',
            Colunas=['coluna1', 'coluna2'],
            dados=['valor1', 123]
        )
        ```
        """
        if type(Colunas) == list and type(dados) == list:
            if len(Colunas) == len(dados):
                database, cursor = self.conectarBanco()

                ColunaSQL = ','.join(Colunas)

                Dados = []

                for dado in dados:
                    if type(dado) == str or type(dado) == bool:
                        Dados.append(f"'{dado}'")
                    else:
                        Dados.append(str(dado))

                dadoSQL = ','.join(Dados)

                cursor.execute(f'INSERT INTO {nomeTabela} ({ColunaSQL}) VALUES ({dadoSQL})')

                database.commit()
                database.close()
            else:
                print('Impossível inserir dados: quantidade de colunas e valores não coincide.')
        else:
            print('Impossível inserir dados: parâmetros devem ser listas.')

    def apagarDados(self, nomeTabela: str, conditions: str = ''):
        database, cursor = self.conectarBanco()

        if conditions == '':
            cursor.execute(f'DELETE FROM {nomeTabela}')
        
        else:
            cursor.execute(f'DELETE FROM {nomeTabela} WHERE {conditions}')
        
        database.commit()
        database.close()

    def editarDados(self, nomeTabela: str, Coluna: str, Valor: str, conditions: str = ''):
        database, cursor = self.conectarBanco()

        if conditions == '':
            cursor.execute(f"UPDATE {nomeTabela} SET {Coluna} = '{Valor}'")
        
        else:
            cursor.execute(f"UPDATE {nomeTabela} SET {Coluna} = '{Valor}' WHERE {conditions}")
        
        database.commit()
        database.close()

    def adicionarColuna(self, nomeTabela: str, Coluna: str, ColunaTipo: str):
        database, cursor = self.conectarBanco()

        cursor.execute(f'ALTER TABLE {nomeTabela} ADD COLUMN {Coluna} {ColunaTipo.upper()}')

        database.commit()
        database.close()
    
    def apagarColuna(self, nomeTabela: str, Coluna: str):
        """
        Apaga uma coluna de uma tabela do banco de dados.

        :param nomeTabela: Nome da tabela onde a coluna será apagada.
        :param Coluna: Nome da coluna a ser apagada.
        
        Exemplo de uso:
        ```python
        db = SQLITE('meu_banco')
        db.apagarColuna('minha_tabela', 'coluna2')
        ```
        """
        database, cursor = self.conectarBanco()

        cursor.execute(f'ALTER TABLE {nomeTabela} DROP COLUMN {Coluna}')

        database.commit()
        database.close()

    def apagarTabela(self, nomeTabela: str):
        """
        Apaga uma tabela do banco de dados.

        :param nomeTabela: Nome da tabela a ser apagada.
        
        Exemplo de uso:
        ```python
        db = SQLITE('meu_banco')
        db.apagarTabela('minha_tabela')
        ```
        """
        database, cursor = self.conectarBanco()

        cursor.execute(f'DROP TABLE IF EXISTS {nomeTabela}')

        database.commit()
        database.close()

    def verDados(self, nomeTabela: str, conditions: str = '', colunas: str = '*'):
        """
        Consulta dados de uma tabela do banco de dados.

        :param nomeTabela: Nome da tabela a ser consultada.
        :param conditions: Condições para a consulta (opcional).
        :param colunas: Colunas a serem selecionadas (opcional).
        :return: Dados consultados.
        
        Exemplo de uso:
        ```python
        db = SQLITE('meu_banco')
        dados = db.verDados('minha_tabela')
        print(dados)
        ```
        """
        database, cursor = self.conectarBanco()

        if conditions == '':
            cursor.execute(f'SELECT {colunas} FROM {nomeTabela}')
        else:
            cursor.execute(f'SELECT {colunas} FROM {nomeTabela} WHERE {conditions}')

        dados = cursor.fetchall()

        database.commit()
        database.close()

        return dados

    def verDadosPlus(self, query: str, params: list):
        """
        Consulta dados com base em uma query SQL customizada.

        :param query: Query SQL a ser executada.
        :param params: Parâmetros para a query SQL.
        :return: Dados consultados.
        
        ```python
        db = SQLITE('meu_banco')
        query = "SELECT * FROM minha_tabela WHERE coluna1 = ? AND coluna2 = ?"
        params = ['valor1', 123]
        dados = db.verDadosPlus(query, params)
        print(dados)
        ```
        """
        database, cursor = self.conectarBanco()
        
        cursor.execute(query, params)
        dados = cursor.fetchall()
        
        database.commit()
        database.close()
        
        return dados

    def encryptPass(self, value: str):
        """
        Gera um hash SHA-512 de um valor fornecido.

        :param value: Valor a ser criptografada.
        :return: Valor criptografado em SHA-512.
        
        Exemplo de uso:
        ```python
        db = SQLITE('meu_banco')
        value_hashed = db.encryptPass('minha_senha')
        print(value_hashed)
        ```
        """
        hash = sh.sha512()
        hash.update(value.encode('UTF-8'))
        value_hashed = hash.hexdigest()

        return value_hashed


if __name__ == '__main__':
    # Exemplo de uso da classe SQLITE
    db = SQLITE('users')

    # Criar tabela
    db.criarTabela(
        nomeTabela='users',
        Colunas=['nome', 'username', 'senha'],
        ColunasTipo=['TEXT', 'TEXT', 'TEXT']
    )

    # Inserir dados
    db.inserirDados(
        nomeTabela='users',
        Colunas=['nome', 'username', 'senha'],
        dados=['Alexandre Zunguze', 'azunguze', db.encryptPass('Aa123')]
    )

    # Ver dados
    dados = db.verDados('users')
    print(dados)

    # Apagar tabela
    db.apagarTabela('users')