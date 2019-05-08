from tornado import Server
import TemplateAPI
from random import randint
import json
import db
import sqlite3
import mailPoVo
import datetime
import uuid

dbConn = sqlite3.connect('./db/povo.db')
usertype = ''
host = "localhost"
port = 80


def setup():
    print "Server listening on http://{host}:{port}".format(
        host=host, port=port)
    # db.setup(dbConn)


def loginCheck(fn):
    def result(response, *args, **kwargs):
        if response.get_secure_cookie('user_id') is not None:
            return fn(response, *args, **kwargs)
        else:
            response.redirect('/login')
    return result


def homePage(response):
    if response.get_secure_cookie('user_id'):
        response.redirect('/dashboard')
    else:
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
    user['name'] = response.get_field("name")
    user['email'] = response.get_field("email")
    user['password'] = response.get_field("password1")
    user['usertype'] = response.get_field("usertype")
    register = db.registerUser(dbConn, user)
    # register successful go to homepage/login
    if register == 1:
        mailPoVo.sendConfirmationEmail(user['email'])
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
        response.set_secure_cookie('name', str(matches[2]))
        response.redirect('/dashboard')
    else:
        response.redirect('/login?fail=1')


@loginCheck
def resetPassword(response):
    response.write(TemplateAPI.render('manageUser.html',
                                      response, {'title': 'Reset Password'}))


@loginCheck
def resetPasswordPost(response):
    user = {}
    user['email'] = response.get_field("email")
    user['password'] = response.get_field("password")
    passwordReset = db.resetUserPassword(dbConn, user)
    # password reset successful go to dashboard
    if passwordReset:
        response.redirect('/dashboard')


@loginCheck
def logout(response):
    response.clear_cookie('user_id')
    response.clear_cookie('user_type')
    response.redirect('/login')


@loginCheck
def dashboard(response):
    usertype = response.get_secure_cookie('user_type')
    name = response.get_secure_cookie('name')
    response.write(TemplateAPI.render(
        'dashboard.html', response, {"title": "Dashboard", "usertype": usertype}))


@loginCheck
def advertisement(response):
    ads = db.getAds(dbConn)
    # print ads
    response.write(TemplateAPI.render("advertisement.html",
                                      response, {"title": "Advertisement", "ads": ads}))


@loginCheck
def advertisementPost(response):
    ad = {}
    ad["title"] = response.get_field("title")
    ad["desc"] = response.get_field("desc")
    ad["imgpath"] = []

    for x in response.get_files("img"):
        imgpath = "static/img_store/ad_img/" + str(uuid.uuid4().hex) + ".png"
        try:
            with open(imgpath, 'wb') as img:
                img.write(str(x[2]))
            ad["imgpath"].append(imgpath)
        except:
            pass
                    
    ad["datetime"] = datetime.datetime.now().isoformat()
    ad["userid"] = response.get_secure_cookie('user_id')
    ad["active"] = 1
    result = db.createAd(dbConn, ad)
    if result:
        response.redirect("/advertisement")
    else:
        response.redirect("/advertisement?fail=1")


def advertisementDelete(response):
    # print response.get_field('id')
    result = db.deleteAds(dbConn, response.get_field('id'))
    if result:
        response.redirect("/advertisement")
    else:
        response.redirect("/advertisement?fail=1")

@loginCheck
def test(response):
    response.write(TemplateAPI.render("test.html", response, {"title": "test"}))

def main():
    server = Server(host, port)
    server.register("/", homePage)
    server.register('/login', login, get=login, post=loginPost)
    server.register('/register', register, get=register, post=registerPost)
    server.register('/logout', logout)
    server.register('/dashboard', dashboard)
    server.register('/advertisement', advertisement)
    server.register('/test', test)
    server.register('/advertisement', advertisement,
                    get=advertisement, post=advertisementPost)
    server.register('/advertisement/delete', advertisementDelete)
    server.register('/resetpassword', resetPassword,
                    get=resetPassword, post=resetPasswordPost)
    server.run(setup)


if __name__ == "__main__":
    main()
