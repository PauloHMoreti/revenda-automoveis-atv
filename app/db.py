import os

import mysql.connector


def get_connection():
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST", "localhost"),
        port=int(os.getenv("MYSQL_PORT", 3306)),
        user=os.getenv("MYSQL_USER", "root"),
        password=os.getenv("MYSQL_PASSWORD", ""),
        database=os.getenv("MYSQL_DATABASE", "oficina"),
    )


def consultar(sql, params=(), um=False):
    """Executa um SELECT e devolve as linhas como dicionários."""
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(sql, params)
        return cursor.fetchone() if um else cursor.fetchall()
    finally:
        conn.close()


def executar(sql, params=()):
    """Executa um INSERT/UPDATE/DELETE, confirma a transação e devolve o id gerado."""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(sql, params)
        conn.commit()
        return cursor.lastrowid
    finally:
        conn.close()
