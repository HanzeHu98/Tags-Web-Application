# File Name: init_database.py
# Author: Hanze Hu
# File Description: Contains the functions to initialize a sqlite3 database
# for the tagging system
#
# Date: June 1, 2022

import sqlite3
from uuid import uuid4
import auth

def init_tags_database():
    database_path = "data/tags.db"
    conn = sqlite3.connect(database_path)
    curs = conn.cursor()

    curs.execute("DROP TABLE IF EXISTS tags")
    curs.execute("CREATE TABLE IF NOT EXISTS tags (user_name VARCHAR(50), tag VARCHAR(50))")
    init_data = (
        ("James", "games"),
        ("Hanze Hu", "music"),
        ("Hanze Hu", "soccer"),
        ("Hanze Hu", "cooking"),
        ("Hanze Hu", "travelling"),
        ("Jayden", "NFTs"),
    )
    sql = "INSERT INTO tags (user_name, tag) values (?,?)"
    for data in init_data:
        curs.execute(sql, (data[0], data[1]))

    conn.commit()
    curs.close()
    conn.close()

def init_auth_database():
    database_path = "data/database.db"
    conn = sqlite3.connect(database_path)
    curs = conn.cursor()

    curs.execute("DROP TABLE IF EXISTS auth")
    curs.execute("CREATE TABLE IF NOT EXISTS auth (user_id VARCHAR(50) PRIMARY KEY, salt BLOB, hashed BLOB, token VARCHAR(100))")
    init_data = (
        ("Hanze Hu", uuid4(), "", "password1"),
        ("James", uuid4(), "", "password2"),
        ("Jayden", uuid4(), "", "password3"),
        ("Clara", uuid4(), "", "password4"),
    )
    sql = "INSERT INTO auth (user_id, salt, hashed, token) values (?,?,?,?)"
    for data in init_data:
        salt, hashed = auth.hash_password(data[3])
        curs.execute(sql, (data[0], salt, hashed, data[2]))

    conn.commit()
    curs.close()
    conn.close()

if __name__ == "__main__":
    init_tags_database()
    init_auth_database()