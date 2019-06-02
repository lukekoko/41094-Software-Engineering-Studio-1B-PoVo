import sqlite3
import bcrypt


def setup(conn):
    print("setup")
    conn.execute("DROP TABLE IF EXISTS user;")
    conn.execute("DROP TABLE IF EXISTS advertisements")
    conn.execute("DROP TABLE IF EXISTS advertisement_img")
    conn.execute("DROP TABLE IF EXISTS bookings")
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
            active INT
	 	);
	 """)

    conn.execute("""
		CREATE TABLE IF NOT EXISTS advertisements
		(
			id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
			title TEXT NOT NULL,
			description TEXT,
            datetime TEXT,
			active INT,
			user_id INT NOT NULL,
			FOREIGN KEY (user_id) REFERENCES user(id)
		);
	""")

    conn.execute("""
		CREATE TABLE IF NOT EXISTS advertisement_img
		(
			id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
			path TEXT NOT NULL,
			ad_id INT NOT NULL,
			FOREIGN KEY (ad_id) REFERENCES advertisements(ad_id)
		);
	""")

    conn.execute("""
     	CREATE TABLE IF NOT EXISTS bookings
     	(
     		id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
     		title TEXT NOT NULL,
     		description TEXT,
            datetime TEXT,
     		charity_user_id INT,
            donor_user_id INT,
     		active INT,
     		Location TEXT,
     		FOREIGN KEY (donor_user_id) REFERENCES user(id)
            FOREIGN KEY (charity_user_id) REFERENCES user(id)
     	);
    """)

    # password = bcrypt.hashpw('1234', bcrypt.gensalt())
    # conn.execute(
    #     "INSERT INTO user (name, email, password, type) VALUES ('test', 'test@gmail.com', ?, 1)", (password,))


if __name__ == "__main__":
    dbConn = sqlite3.connect('povo.db')
    setup(dbConn)
