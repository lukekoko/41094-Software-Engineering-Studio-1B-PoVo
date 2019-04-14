import sqlite3
import bcrypt

def setup(conn):
	conn.execute("DROP TABLE IF EXISTS user;")
	conn.execute("DROP TABLE IF EXISTS ads")
	conn.execute("DROP TABLE IF EXISTS ads_history")

	conn.execute("""
		CREATE TABLE IF NOT EXISTS user
		(
			id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL ,
			Username TEXT NOT NULL,
			Name TEXT NOT NULL,
			Email TEXT unique,
			Password TEXT NOT NULL,
			Type INT NOT NULL
		);
	""")

	conn.execute("""
		CREATE TABLE IF NOT EXISTS ads
		(
			id INT PRIMARY KEY NOT NULL,
			title TEXT NOT NULL,
			description TEXT,
			user_id INT,
			FOREIGN KEY (user_id) REFERENCES user(id)
		);
	""")

	password = bcrypt.hashpw('1234', bcrypt.gensalt())
	conn.execute("INSERT INTO user (Username, Name, Email, Password, Type) VALUES ('test', 'test', 'test@gmail.com', ?, 1)", (password,))

def registerUser(conn, user):
	print user['password']
	password = user['password']
	user['password'] = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())
	try:
		conn.execute("INSERT INTO user (Username, Name, Email, Password, Type) VALUES (:username, :name, :email, :password, :usertype)", user)
	except:
		print("error")
		
def checkPassword(conn, username, password):
	hashPW = conn.execute("SELECT Password FROM user WHERE username=?", (username,)).fetchone()
	if bcrypt.checkpw(password.encode('utf8'), hashPW[0].encode('utf8')):
		return True
	else:
		return False