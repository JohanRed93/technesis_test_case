import sqlite3
from typing import List, Dict


# Создаем подключение к базе данных
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Создаем таблицу, если она не существует
cursor.execute('''
CREATE TABLE IF NOT EXISTS data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    url TEXT NOT NULL,
    xpath TEXT NOT NULL
)
''')
conn.commit()


def insert_data(data: List[Dict[str, str]]) -> List[Dict[str, str]]:
    """
    Вставляет данные в таблицу и возвращает добавленные строки.
    """
    added_rows = []
    for row in data:
        cursor.execute('''
        INSERT INTO data (title, url, xpath)
        VALUES (?, ?, ?)
        ''', (row['title'], row['url'], row['xpath']))
        conn.commit()
        added_rows.append(row)
    return added_rows


def close_connection():
    """Закрывает соединение с базой данных."""
    conn.close()
