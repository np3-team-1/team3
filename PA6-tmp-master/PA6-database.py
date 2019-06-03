import sqlite3
def create_table():
    conn = sqlite3.connect("temperature.db")
    cur = conn.cursor()
    cur.execute('''create table tmp(DATE, TMP)
    ''')
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_table()
