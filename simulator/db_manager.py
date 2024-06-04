# simulator/db_manager.py

import sqlite3
from .cell import Cell

def initialize_database():
    conn = sqlite3.connect('universe.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cells (
            id INTEGER PRIMARY KEY,
            x INTEGER,
            y INTEGER,
            density REAL,
            temperature REAL
        )
    ''')
    conn.commit()
    conn.close()

def save_universe_to_db(conn, cells):
    cursor = conn.cursor()
    for cell in cells.values():
        cursor.execute('''
            INSERT OR REPLACE INTO cells (id, x, y, density, temperature) VALUES (?, ?, ?, ?, ?)
        ''', (None, cell.x, cell.y, cell.density, cell.temperature))
    conn.commit()

def load_universe_from_db(conn):
    cursor = conn.cursor()
    cursor.execute('SELECT x, y, density, temperature FROM cells')
    cells = {}
    for row in cursor.fetchall():
        x, y, density, temperature = row
        cells[(x, y)] = Cell(x, y, density, temperature)
    return cells
