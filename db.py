import sqlite3
import bcrypt

def setup(conn):
	print("setup")
	conn.execute("DROP TABLE IF EXISTS user;")
	conn.execute("DROP TABLE IF EXISTS ads")
	# conn.execute("DROP TABLE IF EXISTS ads_history")
	conn.execute("DROP TABLE IF EXISTS booking")
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
			type INT NOT NULL
		);
	""")

	conn.execute("""
		CREATE TABLE IF NOT EXISTS ads
		(
			id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
			title TEXT NOT NULL,
			description TEXT,
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
			Location TEXT,
			FOREIGN KEY (user_id) REFERENCES user(id)
		)
	""")

	# password = bcrypt.hashpw('1234', bcrypt.gensalt())
	# conn.execute("INSERT INTO user (name, email, password, type) VALUES ('test', 'test@gmail.com', ?, 1)", (password,))

def registerUser(conn, user):
	password = user['password']
	user['password'] = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())
	try:
		conn.execute("INSERT INTO user (name, email, password, type) VALUES (:name, :email, :password, :usertype)", user)
		return True
	except:
		return False
		
def checkPassword(conn, email, password):
	try:
		hashPW = conn.execute("SELECT password FROM user WHERE email=?", (email,)).fetchone()
		if bcrypt.checkpw(password.encode('utf8'), hashPW[0].encode('utf8')):
			usertype = conn.execute("SELECT type FROM user WHERE email=?", (email,)).fetchone()
			return usertype[0]
		else:
			return False
	except: 
		return False