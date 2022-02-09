import sqlite3
import config_files.config as config


def txt_db_set():
    # main part of txt db for msg sending
    joined_file = open(config.db_path + "joined.txt", "r")
    joined_users = set()
    for line in joined_file:
        joined_users.add(line.strip())
    joined_file.close()
    return joined_users


def txt_db_add(joined_users, user_id):
    if not str(user_id) in joined_users:
        joined_file = open(config.db_path + "joined.txt", 'a')
        joined_file.write(str(user_id) + "\n")
        joined_file.close()
        joined_users.add(user_id)
        return True
    else:
        return False


def open_sticker(sticker_id):
    sti = open(config.sticker_path + f'AnimatedSticker{str(sticker_id)}.tgs', 'rb')
    return sti


def sql_check(user_id):
    # SQL lite DATABASE:
    # create db & table and connect
    connect = sqlite3.connect(config.db_path + "users.db")
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
    connect = sqlite3.connect(config.db_path + "users.db")
    cursor = connect.cursor()
    cursor.execute("INSERT INTO users VALUES(?, ?, ?, ?)", (message.contact.user_id, message.contact.phone_number,
                                                            message.contact.first_name, message.contact.last_name))
    connect.commit()
    res = message.contact.phone_number
    return res
