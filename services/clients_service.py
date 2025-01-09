import sqlite3

def init_clients_db():
    conn = sqlite3.connect("database/clients.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            sector TEXT NOT NULL,
            content_demand INTEGER NOT NULL,
            description TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def get_clients():
    conn = sqlite3.connect("database/clients.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM clients")
    clients = cursor.fetchall()
    conn.close()
    return clients

def add_client(name, sector, content_demand, description):
    conn = sqlite3.connect("database/clients.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO clients (name, sector, content_demand, description)
        VALUES (?, ?, ?, ?)
    """, (name, sector, content_demand, description))
    conn.commit()
    conn.close()

def update_client(client_id, name, sector, content_demand, description):
    conn = sqlite3.connect("database/clients.db")
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE clients
        SET name = ?, sector = ?, content_demand = ?, description = ?
        WHERE id = ?
    """, (name, sector, content_demand, description, client_id))
    conn.commit()
    conn.close()

def delete_client(client_id):
    conn = sqlite3.connect("database/clients.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM clients WHERE id = ?", (client_id,))
    conn.commit()
    conn.close()
