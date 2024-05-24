import sqlite3


def connect():
    connection = sqlite3.connect('translation.db')
    cursor = connection.cursor()
    return connection, cursor


def create_users_table():
    sql = """
    DROP TABLE IF EXISTS users;
    CREATE TABLE IF NOT EXISTS users(
         id INTEGER PRIMARY KEY AUTOINCREMENT,
         chat_id BIGINT NOT NULL
    );
    """
    con, cur = connect()
    cur.executescript(sql)
    con.commit()
    con.close()


def create_translations_table():
    sql = """
    DROP TABLE IF EXISTS translations;
    CREATE TABLE IF NOT EXISTS translations(
         id INTEGER PRIMARY KEY AUTOINCREMENT,
         lang_from TEXT,
         lang_to TEXT,
         original TEXT,
         translated TEXT,
         user_id INTEGER REFERENCES users(id)
    );     
    """
    con, cur = connect()
    cur.executescript(sql)
    con.commit()
    con.close()


def get_user(chat_id):
    con, cur = connect()
    sql = "SELECT id FROM users WHERE chat_id = ?;"
    user_id = cur.execute(sql, (chat_id,)).fetchone()
    if user_id is None:
        return False
    return user_id[0]


def insert_user(chat_id):
    user_id = get_user(chat_id)
    con, cur = connect()

    if not user_id:
        sql = "INSERT INTO users(chat_id) VALUES (?)"
        cur.execute(sql, (chat_id,))

        con.commit()

        con.close()

        print('user added')
        return
    print('already exists')


def insert_translation(lang_from, lang_to, original, translated, chat_id):
    user_id = get_user(chat_id)
    con, cur = connect()

    sql = "INSERT INTO translations(lang_from, lang_to, original, translated, user_id) VALUES (?, ?, ?, ?, ?)"
    cur.execute(sql, (lang_from, lang_to, original, translated, user_id,))
    con.commit()
    con.close()
    print('Добавили перивод')

def get_user_translations(chat_id):
    user_id = get_user(chat_id)
    con, cur = connect()
    sql = "SELECT * FROM translations WHERE user_id = ?"
    translations = cur.execute(sql, (user_id,)).fetchall()
    return translations

# create_users_table()
# create_translations_table()