import sqlite3

def init_cronogramas_db():
    conn = sqlite3.connect("database/cronogramas.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cronogramas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_id INTEGER NOT NULL,
            client_name TEXT NOT NULL,
            content TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def add_cronograma(client_id, client_name, content):
    conn = sqlite3.connect("database/cronogramas.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO cronogramas (client_id, client_name, content)
        VALUES (?, ?, ?)
    """, (client_id, client_name, content))
    conn.commit()
    conn.close()

def get_cronogramas():
    conn = sqlite3.connect("database/cronogramas.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cronogramas")
    cronogramas = cursor.fetchall()
    conn.close()
    return cronogramas

def delete_cronograma(cronograma_id):
    conn = sqlite3.connect("database/cronogramas.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM cronogramas WHERE id = ?", (cronograma_id,))
    conn.commit()
    conn.close()
