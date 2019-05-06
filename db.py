import sqlite3
import bcrypt
import os


def registerUser(conn, user):
    password = user['password']
    user['password'] = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())
    try:
        conn.execute(
            "INSERT INTO user (name, email, password, type) VALUES (:name, :email, :password, :usertype)", user)
        conn.commit()
        return 1
    except sqlite3.IntegrityError:
        return 2
    except Exception:
        return 3


def resetUserPassword(conn, user):
    try:
        password = user['password']
        user['password'] = bcrypt.hashpw(
            password.encode('utf8'), bcrypt.gensalt())
        conn.execute(
            "UPDATE user set password = :password WHERE email= :email", user)
        return True
    except:
        return False


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


def createAd(conn, ad):
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO advertisements (title, description, datetime, active, user_id) VALUES (:title, :desc, :datetime, :active, :userid)", ad)
        for x in ad["imgpath"]:
            conn.execute(
                "INSERT INTO advertisement_img (path, ad_id) VALUES (?, ?)", (x, cursor.lastrowid))
        conn.commit()
        return True
    except:
        return False


def getAds(conn):
    ads = []
    cursor = conn.execute(
        "SELECT id, title, description, datetime, user_id FROM advertisements")
    for row in cursor:
        ad = {}
        ad["id"] = row[0]
        ad["title"] = row[1]
        ad["desc"] = row[2]
        ad["datetime"] = row[3]
        ad["user_id"] = row[4]
        try:
            imgpath = conn.execute(
                "SELECT path FROM advertisement_img WHERE ad_id=?", (row[0],))
            ad["img_path"] = imgpath.fetchone()[0]
        except:
            ad["img_path"] = ""
        # print ad
        ads.append(ad)
    return ads


def deleteAds(conn, id):
    try:
        conn.execute(
            "DELETE FROM advertisements WHERE id=?", (id,)
        )
        cursor = conn.execute(
            "SELECT path FROM advertisement_img WHERE ad_id=?", (id,))
        for x in cursor:
            os.remove(x[0])
        conn.execute(
            "DELETE FROM advertisement_img WHERE ad_id=?", (id,)
        )
        conn.commit()
        return True
    except:
        return False
