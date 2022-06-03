# File Name: data_persistence.py
# Author: Hanze Hu
# File Description: Contains the functions to interact with the database
#
# Date: June 1, 2022

import sqlite3

DATABASE = "data/tags.db"

def db_update_tag(user_name, old_value, value):
    """
    Update value for attribute in sql database

    Args:
        user_name: id of the user
        value: new value for tags
    
    Returns:
        None
    """
    database_path = DATABASE
    conn = sqlite3.connect(database_path)
    curs = conn.cursor()
    curs.execute(f"UPDATE tags SET tag = '{value}' WHERE user_name = '{user_name}' AND tag = '{old_value}'")
    conn.commit()
    curs.close()
    conn.close()
    if curs.rowcount != 1:
        return "Operation Failed"
    return None

def db_fetch_tags(user_name):
    """
    Query value for attribute in sql database

    Args:
        user_name: id of the user
    
    Returns:
        Query result
    """
    database_path = DATABASE
    conn = sqlite3.connect(database_path)
    curs = conn.cursor()
    curs.execute(f"SELECT tag FROM tags WHERE user_name = '{user_name}'")
    output = []
    result = curs.fetchone()
    while result != None:
        output.append(result[0])
        result = curs.fetchone()
    curs.close()
    conn.close()
    return output


def db_insert_tag(user_name, value):
    """
    Insert data to auth database

    Args:
        insert_sql: sql used to insert data
        data_list: a list of data to be inserted
    
    Returns:
        None
    """
    database_path = DATABASE
    conn = sqlite3.connect(database_path)
    curs = conn.cursor()

    curs.execute("INSERT INTO tags (user_name, tag) values (?,?)", (user_name, value))
    conn.commit()
    curs.close()
    conn.close()
    if curs.rowcount != 1:
        return "Operation Failed"
    return None


def db_delete_tag(user_name, value):
    """
    Delete data from auth database

    Args:
        attribute: a attribute used to locate data to delete
        value: value of the attribute
    
    Returns:
        None
    """
    database_path = DATABASE
    conn = sqlite3.connect(database_path)
    curs = conn.cursor()

    curs.execute(f"DELETE FROM tags WHERE user_name = '{user_name}' AND tag = '{value}'")
    conn.commit()
    curs.close()
    conn.close()
    if curs.rowcount != 1:
        return "Operation Failed"
    return None
