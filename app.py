from flask import Flask
import sqlite3
import time

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
    conn.close()

def update(id, newTitle=None, newDescription=None):
    updated_at = int(time.time())
    if newTitle is not None and newDescription is not None:
        cursor.execute("UPDATE tasks SET title = ?, description = ?, updated_at = ? WHERE id = ?", (newTitle, newDescription, updated_at, id))
    elif newTitle is not None:
        cursor.execute("UPDATE tasks SET title = ?, updated_at = ? WHERE id = ?", (newTitle, updated_at, id))
    elif newDescription is not None:
        cursor.execute("UPDATE tasks SET description = ?, updated_at = ? WHERE id = ?", (newDescription, updated_at, id))
    conn.commit()
    conn.close



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

#if __name__ == '__main__': # inicializa o app
#    app.run(debug=True)

menu_update()
read_all()
