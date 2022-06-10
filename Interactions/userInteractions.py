import mariadb as db
import dbhandler as dbh
import traceback
import userLogin as ul

# Function to create a new user. Requires username and email, and hashed password plus salt to be stored.


def post_user(email, username, pass_hash, salt):
    user = []
    conn, cursor = dbh.db_connect()
    try:
        # Inserting a new user into the DB
        cursor.execute(
            "INSERT INTO users (email, username, password, salt) VALUES (?, ?, ?, ?)", [email, username, pass_hash, salt])
        conn.commit()
        # After creating the user in the DB, we pass in information to the user login endpoint to also log the user in, creating a login token.
        user = ul.post_login(email, None, pass_hash)
        # Saving the login token to a variable
        login_token = user[1]['loginToken']
        # Run a select statement to get data on the newly created user, save it to a variable and then change to an object, with the logintoken aswell. before disconnecting and returning the data
        cursor.execute(
            "SELECT users.id, email, username FROM users WHERE username = ?", [username])
        user = cursor.fetchone()
        user = {
            'userId': user[0],
            'email': user[1],
            'username': user[2],
            'loginToken': login_token
        }
    except db.OperationalError:
        traceback.print_exc()
        print('Something went  wrong with the db!')
    except db.ProgrammingError:
        traceback.print_exc()
        print('Error running DB query')
    except:
        traceback.print_exc()
        print("Something unexpected went wrong")
    dbh.db_disconnect(conn, cursor)
    # If user is empty, something went wrong. If not return the user.
    if(user == []):
        return False, None
    else:
        return True, user
