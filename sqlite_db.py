import sqlite3


def sql_check(user_id):
    # SQL lite DATABASE:
    # create db & table and connect
    connect = sqlite3.connect("db/users.db")
    cursor = connect.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY,
            phone TEXT,
            first_name TEXT,
            last_name TEXT
            )""")
    connect.commit()
    print(user_id)

    # check user id in fields
    new_user_id = user_id
    cursor.execute(f"SELECT id FROM users WHERE id = {new_user_id}")
    id_check = cursor.fetchone()
    print("checking user id in db")
    print(id_check)
    if id_check is None:
        result = False
        return result
    else:
        result = True
        return result


def add_user(message):
    print(message)
    connect = sqlite3.connect("db/users.db")
    cursor = connect.cursor()
    cursor.execute("INSERT INTO users VALUES(?, ?, ?, ?)", (message.contact.user_id, message.contact.phone_number,
                                                            message.contact.first_name, message.contact.last_name))
    connect.commit()
    res = message.contact.phone_number
    return res
