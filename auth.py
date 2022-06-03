# File Name: auth.py
# Author: Hanze Hu
# File Description: Contains the functions to interact with the user
# authentication database
#
# Date: June 1, 2022

import sqlite3, os, hashlib, secrets, string

DATABASE = "data/database.db"

def authenticate(user_id, password):
    """
    Check if the user_id and password match and are correct

    Args:
        user_id: id of the user
        password: password for the id
    
    Returns:
        True if user_id and password match and are correct;
        False otherwise
    """
    salt, hashed = get_credential(user_id)
    if not hashed:
        return False
    _, hashed_to_verify = hash_password(password, salt)
    return hashed_to_verify == hashed


def generate_token(user_id):
    """
    Generate a token for the user with user_id

    Args:
        user_id: id of the user
    
    Returns:
        A random string for future api access
    """
    string_lib = string.ascii_letters + string.digits + user_id
    token = ''.join(secrets.choice(string_lib) for _ in range(64))
    sql_do_update(user_id, "token", token)
    return token


def get_token(user_id):
    """
    Get the token of user with user_id

    Args:
        user_id: id of the user
    
    Returns:
        Token of the user
    """
    result = sql_do_select(user_id, "token")
    return result[0] if result else None


def logout(user_id):
    """
    Logout the user with user_id; this will empty token of the user

    Args:
        user_id: id of the user
    
    Returns:
        None
    """
    sql_do_update(user_id, "token", "")


def get_role(user_id):
    """
    Get the role of user with user_id

    Args:
        user_id: id of the user
    
    Returns:
        Role of the user
    """
    result = sql_do_select(user_id, "role")
    return result[0] if result else None

def add_user_to_auth_database(user_id, password, role):
    """
    Register a new user to auth database

    Args:
        user_id: id of the user
        password: password for the id
        role: role of the user
    
    Returns:
        True if successfully added the user;
        False otherwise (user_id exist)
    """
    if user_exists(user_id):
        return False
    salt, hashed = hash_password(password)
    insert_sql = "INSERT INTO auth (user_id, role, salt, hashed, token) values (?,?,?,?,?)"
    sql_do_insert(insert_sql, [(user_id, role, salt, hashed, "")])
    return True

def permitted(customer_id, user_id):
    role = get_role(user_id)
    if role == "FM":
        return True
    return user_id == customer_id

def user_exists(user_id):
    """
    Check whether a user_id exists

    Args:
        user_id: id of the user
    
    Returns:
        True if user_id exists;
        False otherwise
    """
    result = sql_do_select(user_id, "user_id")
    return result is not None

#----------------------------------- HELPERS --------------------------------#

def get_credential(user_id):
    """
    Get the salt and hashed password of user with user_id

    Args:
        user_id: id of the user
    
    Returns:
        Salt and hashed password of the user
    """
    result = sql_do_select(user_id, "salt, hashed")
    return result if result else (None, None)


def hash_password(password, salt=None):
    """
    Generate a hashed password (and salt if it is absent)

    Args:
        password: password to hash
        salt: salt used to hash the password
    
    Returns:
        Salt and hashed password
    """
    if salt is None:
        salt = os.urandom(32)
    hashed = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode('utf-8'),
        salt,
        100000
    )
    return salt, hashed


#----------------------------------- PERSIST LAYER --------------------------------#

def sql_do_update(user_id, attribute, value):
    """
    Update value for attribute in sql database

    Args:
        user_id: id of the user
        attribute: attribute to update
        value: new value
    
    Returns:
        None
    """
    conn = sqlite3.connect(DATABASE)
    curs = conn.cursor()
    curs.execute(f"UPDATE auth SET {attribute} = '{value}' WHERE user_id = '{user_id}'")
    conn.commit()
    curs.close()
    conn.close()

def sql_do_select(user_id, attribute):
    """
    Query value for attribute in sql database

    Args:
        user_id: id of the user
        attribute: attribute to query
    
    Returns:
        Query result
    """
    conn = sqlite3.connect(DATABASE)
    curs = conn.cursor()
    curs.execute(f"SELECT {attribute} FROM auth WHERE user_id = '{user_id}'")
    result = curs.fetchone()
    curs.close()
    conn.close()
    return result


def sql_do_insert(insert_sql, data_list):
    """
    Insert data to auth database

    Args:
        insert_sql: sql used to insert data
        data_list: a list of data to be inserted
    
    Returns:
        None
    """
    conn = sqlite3.connect(DATABASE)
    curs = conn.cursor()

    for data in data_list:
        curs.execute(insert_sql, data)

    conn.commit()
    curs.close()
    conn.close()


def sql_do_delete(attribute, value):
    """
    Delete data from auth database

    Args:
        attribute: a attribute used to locate data to delete
        value: value of the attribute
    
    Returns:
        None
    """
    conn = sqlite3.connect(DATABASE)
    curs = conn.cursor()

    curs.execute(f"DELETE FROM auth WHERE {attribute} = '{value}'")

    conn.commit()
    curs.close()
    conn.close()