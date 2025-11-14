from flask import Flask
import sqlite3
import time

def limpar_tela():
    import os
    os.system('cls' if os.name == 'nt' else 'clear')


app = Flask(__name__) # instancia o aplicativo flask

# criar o banco de dados
conn = sqlite3.connect("todo.db")
cursor = conn.cursor() # objeto que executa as queries

# tabela
cursor.execute("""
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    completed BOOLEAN NOT NULL DEFAULT 0,
    created_at INTEGER,          
    updated_at INTEGER)
""")

def create(title, description):
    completed = 0;
    created_at = int(time.time())
    cursor.execute("INSERT INTO tasks (title, description, completed, created_at) VALUES (?, ?, ?, ?)", (title, description, completed, created_at))
    conn.commit()

def read_all():
    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()
    for task in tasks:
        id, title, description, completed, created_at, updated_at = task
        print(f"ID:{id}\t\tTitle:{title}\t\tDescr:{description}\t\tComple:{completed}\t\tCreat:{created_at}\t\tUpd:{updated_at}")
        print("-" * 150)
    

def update(id, newTitle=None, newDescription=None):
    updated_at = int(time.time())
    if newTitle is not None and newDescription is not None:
        cursor.execute("UPDATE tasks SET title = ?, description = ?, updated_at = ? WHERE id = ?", (newTitle, newDescription, updated_at, id))
    elif newTitle is not None:
        cursor.execute("UPDATE tasks SET title = ?, updated_at = ? WHERE id = ?", (newTitle, updated_at, id))
    elif newDescription is not None:
        cursor.execute("UPDATE tasks SET description = ?, updated_at = ? WHERE id = ?", (newDescription, updated_at, id))
    conn.commit()
    
def delete(id):
    cursor.execute("SELECT * FROM tasks WHERE id = ?", (id,))
    task = cursor.fetchone()
    if not task:
        return
    cursor.execute("DELETE FROM tasks where id = ?", (id,))
    conn.commit()




def menu_delete():
    print("===== DELETAR UMA TAREFA =====")
    id = int(input("ID: "))
    cursor.execute("SELECT * FROM tasks WHERE id = ?", (id,))
    row = cursor.fetchone()
    if row != None:
        id, title, description, completed, created_at, updated_at = row
        print("-" * 150)
        print(f"ID:{id}\t\tTitle:{title}\t\tDescr:{description}\t\tComple:{completed}\t\tCreat:{created_at}\t\tUpd:{updated_at}")
        print("-" * 150)
        force = input("Deseja excluir? (y/n)")
        if force == 'y' or force == 'Y':
            delete(id)
        elif force == 'n' or force == 'N':
            return
        else:
            print("Opção Invalida")
            return
    


def menu_create():
    print("===== CRIAR NOVA TAREFA =====")
    title = input("Title: ")
    description = input("Description: ")
    create(title, description)

def menu_update():
    print("===== ATUALIZAR NOVA TAREFA =====")
    id = int(input("ID: "))
    title = input("Title: ")
    description = input("Description: ")

    if title.strip() == "" and description.strip() == "":
        return
    elif title.strip() == "":
        update(id, newDescription=description)
    elif description.strip() == "":
        update(id, newTitle=title)
    else:
        update(id, title, description)

def menu():
    while True:
        print("\n===== MENU DE TAREFAS =====")
        print("1 - Nova tarefa")
        print("2 - Atualizar tarefa")
        print("3 - Ver tarefas")
        print("4 - Deletar tarefa")
        print("0 - Sair")

        opcao = input("Escolha uma opção: ")
        limpar_tela()
        if opcao == "1":
            menu_create()
        elif opcao == "2":
            menu_update()
        elif opcao == "3":
            read_all()
        elif opcao == "4":
            menu_delete()
        elif opcao == "0":
            print("\nSaindo do sistema...")
            break
        else:
            print("\nOpção inválida! Tente novamente.")


menu()
conn.close()
