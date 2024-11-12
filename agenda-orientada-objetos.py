import sqlite3
from datetime import datetime

class Contato:
    def __init__(self, id, nome, telefone):
        self.id = id
        self.nome = nome
        self.telefone = telefone

    def __str__(self):
        return f"ID: {self.id}, Nome: {self.nome}, Telefone: {self.telefone}"

class Compromisso:
    def __init__(self, id, descricao, data, contato=None):
        self.id = id
        self.descricao = descricao
        self.data = data
        self.contato = contato

    def __str__(self):
        contato_nome = self.contato.nome if self.contato else "N/A"
        return f"ID: {self.id}, Descrição: {self.descricao}, Data: {self.data}, Contato: {contato_nome}"

class BancoDeDados:
    def __init__(self, nome_arquivo):
        self.conn = sqlite3.connect(nome_arquivo)
        self.criar_tabelas()

    def criar_tabelas(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS contatos (
                id INTEGER PRIMARY KEY,
                nome TEXT NOT NULL,
                telefone TEXT NOT NULL
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS compromissos (
                id INTEGER PRIMARY KEY,
                descricao TEXT NOT NULL,
                data TEXT NOT NULL,
                contato_id INTEGER,
                FOREIGN KEY (contato_id) REFERENCES contatos (id)
            )
        ''')
        self.conn.commit()

    def adicionar_contato(self, nome, telefone):
        cursor = self.conn.cursor()
        cursor.execute('INSERT INTO contatos (nome, telefone) VALUES (?, ?)', (nome, telefone))
        self.conn.commit()
        return cursor.lastrowid

    def adicionar_compromisso(self, descricao, data, contato_id=None):
        cursor = self.conn.cursor()
        cursor.execute('INSERT INTO compromissos (descricao, data, contato_id) VALUES (?, ?, ?)',
                       (descricao, data, contato_id))
        self.conn.commit()
        return cursor.lastrowid

    def listar_contatos(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM contatos')
        return [Contato(id, nome, telefone) for id, nome, telefone in cursor.fetchall()]

    def listar_compromissos(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT c.id, c.descricao, c.data, co.id, co.nome, co.telefone
            FROM compromissos c
            LEFT JOIN contatos co ON c.contato_id = co.id
        ''')
        compromissos = []
        for row in cursor.fetchall():
            contato = Contato(row[3], row[4], row[5]) if row[3] else None
            compromissos.append(Compromisso(row[0], row[1], row[2], contato))
        return compromissos

class Agenda:
    def __init__(self):
        self.db = BancoDeDados('agenda.db')

    def adicionar_contato(self, nome, telefone):
        return self.db.adicionar_contato(nome, telefone)

    def adicionar_compromisso(self, descricao, data, contato_id=None):
        return self.db.adicionar_compromisso(descricao, data, contato_id)

    def listar_contatos(self):
        return self.db.listar_contatos()

    def listar_compromissos(self):
        return self.db.listar_compromissos()

class Interface:
    def __init__(self):
        self.agenda = Agenda()

    def exibir_menu(self):
        print("\n1. Adicionar Contato")
        print("2. Adicionar Compromisso")
        print("3. Listar Contatos")
        print("4. Listar Compromissos")
        print("5. Sair")

    def adicionar_contato(self):
        nome = input("Nome do contato: ")
        telefone = input("Telefone do contato: ")
        id_contato = self.agenda.adicionar_contato(nome, telefone)
        print(f"Contato adicionado com ID: {id_contato}")

    def adicionar_compromisso(self):
        descricao = input("Descrição do compromisso: ")
        data = input("Data do compromisso (YYYY-MM-DD HH:MM): ")
        contato_id = input("ID do contato (opcional): ")
        id_compromisso = self.agenda.adicionar_compromisso(descricao, data, int(contato_id) if contato_id else None)
        print(f"Compromisso adicionado com ID: {id_compromisso}")

    def listar_contatos(self):
        contatos = self.agenda.listar_contatos()
        for contato in contatos:
            print(contato)

    def listar_compromissos(self):
        compromissos = self.agenda.listar_compromissos()
        for compromisso in compromissos:
            print(compromisso)

    def executar(self):
        while True:
            self.exibir_menu()
            opcao = input("Escolha uma opção: ")

            if opcao == '1':
                self.adicionar_contato()
            elif opcao == '2':
                self.adicionar_compromisso()
            elif opcao == '3':
                self.listar_contatos()
            elif opcao == '4':
                self.listar_compromissos()
            elif opcao == '5':
                print("Encerrando o programa...")
                break
            else:
                print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    interface = Interface()
    interface.executar()
