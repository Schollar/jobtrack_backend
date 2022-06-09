import mariadb as db
import dbcreds as dbcreds
import hashlib
import traceback

# Connect function that starts a DB connection and creates a cursor


def db_connect():
    conn = None
    cursor = None
    try:
        conn = db.connect(user=dbcreds.user, password=dbcreds.password,
                          host=dbcreds.host, port=dbcreds.port, database=dbcreds.database)
        cursor = conn.cursor()
    except db.OperationalError:
        print('Something is wrong with the DB')
    except:
        print('Something went wrong connecting to the DB')
    return conn, cursor

# Disconnect function that takes in the conn and cursor and attempts to close both


def db_disconnect(conn, cursor):
    try:
        cursor.close()
    except:
        print('Error closing cursor')
    try:
        conn.close()
    except:
        print('Error closing connection')

# Function that will take in the user input password, and either a username, email or logintoken to get the salt for said user.


def get_password(password, email=None, username=None, logintoken=None):
    if(password == ''):
        db_disconnect(conn, cursor)
        return False
    salt = None
    pass_hash = None
    conn, cursor = db_connect()
    try:
        # Check to see which of the three arguments does not equal None. They all run a select statement to get the salt for the user, based on either logintoken, email or username
        if(logintoken != None):
            cursor.execute(
                "SELECT salt FROM users inner join user_session on user_session.userId = users.id WHERE logintoken = ?", [
                    logintoken])
        elif(email != None):
            cursor.execute("SELECT salt FROM users  WHERE email = ?", [email])
        elif(username != None):
            cursor.execute(
                "SELECT salt FROM users  WHERE username = ?", [username])
        # After one of the three if statements above has ran, we select the salt, append it to the password and then get the hashed password.
        salt = cursor.fetchone()

        password = salt[0] + password
        pass_hash = hashlib.sha512(password.encode()).hexdigest()
    except db.OperationalError:
        traceback.print_exc()
        print('Something went wrong with the db!')
    except db.ProgrammingError:
        traceback.print_exc()
        print('Error running DB query')
    except:
        traceback.print_exc()
        print("Something unexpected went wrong")
    # Disconnect and return hashed+salted password
    db_disconnect(conn, cursor)
    if(salt == None):
        return False
    else:
        return pass_hash

# Function that will get a userId from the logintoken passed to it.


def get_userId(logintoken):
    conn, cursor = db_connect()
    userId = None
    try:
        # Select statement to get userId based off logintoken.
        cursor.execute(
            "SELECT users.id FROM user inner join user_session on users.id = user_session.userId WHERE logintoken = ?", [logintoken])
        # Save Id to variable, but since it defaults to a list, we then save the variable equal to the list index item 0. Disconnect and return userId
        userId = cursor.fetchone()
        userId = userId[0]
    except db.OperationalError:
        traceback.print_exc()
        print('Something went  wrong with the db!')
    except db.ProgrammingError:
        traceback.print_exc()
        print('Error running DB query')
    except:
        traceback.print_exc()
        print("Something unexpected went wrong")
    db_disconnect(conn, cursor)
    if(userId != None):
        return userId
    else:
        return False


def validate_login_token(logintoken):
    conn, cursor = db_connect()
    try:
        # Select statement to get userId based off logintoken.
        cursor.execute(
            "SELECT logintoken FROM user_session WHERE logintoken = ?", [logintoken])
        token = cursor.fetchone()
    except db.OperationalError:
        traceback.print_exc()
        print('Something went  wrong with the db!')
    except db.ProgrammingError:
        traceback.print_exc()
        print('Error running DB query')
    except:
        traceback.print_exc()
        print("Something unexpected went wrong")
    db_disconnect(conn, cursor)
    if(token != None):
        return True
    else:
        return False
