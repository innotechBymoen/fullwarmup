import mariadb
import dbcreds


def connect():
    conn = None
    cursor = None
    try:
        conn = mariadb.connect(user=dbcreds.user, password=dbcreds.password,
                               host=dbcreds.host, port=dbcreds.port, database=dbcreds.database)
        cursor = conn.cursor()
    except:
        print("sorry, something is wrong with the DB connection")
    return conn, cursor


def disconnect(conn, cursor):
    try:
        cursor.close()
    except:
        print("sorry, there was an issue closing the cursor")

    try:
        conn.close()
    except:
        print("sorry, there was an issue closing the connection")


def insert_post(username, content):
    success = False
    id = None
    conn, cursor = connect()
    try:
        cursor.execute("INSERT INTO blog_post(username, content) VALUES(?,?)", [
                       username, content, ])
        conn.commit()
        if(cursor.rowcount == 1):
            success = True
            id = cursor.lastrowid
    except mariadb.ProgrammingError:
        print("There is an error with the SQL")
    except mariadb.OperationalError:
        print("There is an issue with the DB")
    except:
        print("Something went wrong")
    disconnect(conn, cursor)
    return success, id


def get_all_posts():
    success = False
    posts = []
    conn, cursor = connect()
    try:
        cursor.execute(
            "SELECT id, content, username, created_at FROM blog_post")
        posts = cursor.fetchall()
        success = True
    except mariadb.ProgrammingError:
        print("There is an error with the SQL")
    except mariadb.OperationalError:
        print("There is an issue with the DB")
    except:
        print("Something went wrong")
    disconnect(conn, cursor)
    return success, posts
