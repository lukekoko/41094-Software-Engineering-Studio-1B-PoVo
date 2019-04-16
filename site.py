from tornado import Server
import TemplateAPI
from random import randint
import json
import db
import sqlite3

dbConn = sqlite3.connect('./db/povo.db')

usertype = ''

def dummy():
    print "Started"
    db.setup(dbConn)    

def homePage(response):
    response.write(TemplateAPI.render('homepage.html', response, {}))

def login(response):
    response.write(TemplateAPI.render('login.html', response, {}))

def loginPost(response):
    email = response.get_field("email")
    password = response.get_field("password")
    matches = db.checkPassword(dbConn, email, password)
    usertype = matches
    print(usertype)
    if matches:
        profile(response)
    else:
        login(response)

def profile(response):
    response.write(TemplateAPI.render('profile.html', response, {}))    

def register(response):
    response.write(TemplateAPI.render('register.html', response, {}))

def registerPost(response):
    user = {}
    user['name'] = response.get_field("name")
    user['email'] = response.get_field("email")
    user['password'] = response.get_field("password1")
    user['usertype'] = response.get_field("usertype")
    registered = db.registerUser(dbConn, user)
    if registered:
        homePage(response)
    else:
        register(response)
        
def randPage(response):
    response.write("Today's Random number is: " + str(ranGen()))

def ranGen():
    return randint(0, 10)

server = Server('localhost', 80)
server.register("/", homePage)
server.register("/rand", randPage)
server.register('/login', login)
server.register('/login/post', loginPost)
server.register('/register', register)
server.register('/register/post', registerPost)

server.run(dummy)