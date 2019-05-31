from tornado import Server
import TemplateAPI
from random import randint
import json
import db
import sqlite3
import mailPoVo
import base64

db.setup()
dbConn = sqlite3.connect('./db/povo.db')
usertype = ''
host = "localhost"
port = 80


def setup():
    print "Server listening on http://{host}:{port}".format(
        host=host, port=port)
    


def loginCheck(fn):
    def result(response, *args, **kwargs):
        if response.get_secure_cookie('user_id') is not None:
            return fn(response, *args, **kwargs)
        else:
            response.redirect('/login')
    return result


def homePage(response):
    response.write(TemplateAPI.render(	
        'homepage.html', response, {"title": "Homepage"}))


def register(response):
    if response.get_secure_cookie('user_id'):
        response.redirect('/dashboard')
    else:
        fail = response.get_field('fail')
        response.write(TemplateAPI.render('register.html', response, {
                       "title": "Register", "fail": fail}))


def registerPost(response):
    user = {}
    user['conf_status'] = 0
    user['name'] = response.get_field("name")
    user['email'] = response.get_field("email")
    user['password'] = response.get_field("password1")
    user['usertype'] = response.get_field("usertype")
    register = db.registerUser(dbConn, user)
    # register successful go to homepage/login
    if register == 1:
        mailPoVo.sendConfirmationEmail(user['email'], user['name'], user['usertype'])
        response.redirect('/login')
    # register failed go back to register
    elif register == 2:
        response.redirect('/register?fail=userExist')
    else:
        response.redirect('/register?fail=error')


def login(response):
    # checks if user is already logged in
    if response.get_secure_cookie('user_id'):
        response.redirect('/dashboard')
    else:
        login_failed = response.get_field('fail', '') == '1'
        response.write(TemplateAPI.render(
            'login.html', response, {'login_failed': login_failed, "title": "Login"}))


def loginPost(response):
    email = response.get_field("email")
    password = response.get_field("password")
    matches = db.checkPassword(dbConn, email, password)
    # Charity
    if matches:
        response.set_secure_cookie('user_id', str(matches[0]))
        response.set_secure_cookie('user_type', str(matches[1]))
        response.redirect('/dashboard')
    else:
        response.redirect('/login?fail=1')

def confirmation(response):
	response.write(TemplateAPI.render(
        'dashboard.html', response, {"title": "confirmation"}))
	email = base64.b64decode(response.get_field('acc', ''))
	print email

@loginCheck
def logout(response):
    response.clear_cookie('user_id')
    response.clear_cookie('user_type')
    response.redirect('/login')


@loginCheck
def dashboard(response):
    usertype = response.get_secure_cookie('user_type')
    print usertype
    response.write(TemplateAPI.render(
        'dashboard.html', response, {"title": "Dashboard", "usertype": usertype}))

@loginCheck
def advertisement(response):
    items = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11']
    response.write(TemplateAPI.render("advertisement.html",
                                      response, {"title": "Advertisement", "items": items}))


def main():
    server = Server(host, port)
    server.register("/", homePage)
    server.register('/login', login, get=login, post=loginPost)
    server.register('/register', register, get=register, post=registerPost)
    server.register('/logout', logout)
    server.register('/dashboard', dashboard)
    server.register('/advertisement', advertisement)
    server.register('/confirmation', confirmation)

    server.run(setup)


if __name__ == "__main__":
    main()
