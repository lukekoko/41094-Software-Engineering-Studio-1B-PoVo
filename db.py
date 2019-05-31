import sqlite3
import bcrypt


def setup():
	conn = sqlite3.connect('./db/povo.db')
	print("setup")
	conn.execute("DROP TABLE IF EXISTS user;")
    conn.execute("DROP TABLE IF EXISTS advertisements")
    conn.execute("DROP TABLE IF EXISTS booking")
    # conn.execute("DROP TABLE IF EXISTS ads_history")
    # conn.execute("DROP TABLE IF EXISTS booking_history")

    conn.execute("""
		CREATE TABLE IF NOT EXISTS user
		(
			id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
			name TEXT NOT NULL,
			email TEXT unique,
			city TEXT,
			postcode TEXT,
			password TEXT NOT NULL,
			type INT NOT NULL,
			conf_status INT NOT NULL
		);
	""")

    conn.execute("""
		CREATE TABLE IF NOT EXISTS advertisements
		(
			id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
			title TEXT NOT NULL,
			description TEXT,
			active INT,
			user_id INT,
			FOREIGN KEY (user_id) REFERENCES user(id)
		);
	""")

    conn.execute("""
		CREATE TABLE IF NOT EXISTS bookings
		(
			id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
			title TEXT NOT NULL,
			description TEXT,
			user_id INT,
			active INT,
			Location TEXT,
			FOREIGN KEY (user_id) REFERENCES user(id)
		)
	""")

    password = bcrypt.hashpw('1234', bcrypt.gensalt())
    conn.execute(
        "INSERT INTO user (name, email, password, type, conf_status) VALUES ('test', 'test@gmail.com', ?, 1, 0)", (password,))


def registerUser(conn, user):
    password = user['password']
    user['password'] = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())
    try:
        conn.execute(
            "INSERT INTO user (name, email, password, type, conf_status) VALUES (:name, :email, :password, :usertype, 0)", user)
        conn.commit()
        return 1
    except sqlite3.IntegrityError:
        return 2
    except Exception:
        return 3


def checkPassword(conn, email, password):
    try:
        hashPW = conn.execute(
            "SELECT password FROM user WHERE email=?", (email,)).fetchone()
        if bcrypt.checkpw(password.encode('utf8'), hashPW[0].encode('utf8')):
            usertype = conn.execute(
                "SELECT id, type FROM user WHERE email=?", (email,)).fetchone()
            return usertype
        else:
            return False
    except:
        return False
