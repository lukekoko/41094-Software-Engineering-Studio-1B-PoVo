from tornado import Server
import TemplateAPI
from random import randint
import json
import db
import sqlite3
import mailPoVo
import datetime
import uuid
import base64

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
    ads = db.getAds(dbConn)
    if response.get_secure_cookie('user_id'):
        response.redirect('/dashboard')
    else:
        response.write(TemplateAPI.render(
            'homepage.html', response, {"title": "Homepage", "ads": ads}))


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
    print register
    if register == 1:
        print "registration succesful"
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
    print "logging in"
    email = response.get_field("email")
    password = response.get_field("password")
    matches = db.checkPassword(dbConn, email, password)
    # Charity
    if matches:
        print "login sucessful"
        response.set_secure_cookie('user_id', str(matches[0]))
        response.set_secure_cookie('user_type', str(matches[1]))
        response.set_secure_cookie('name', str(matches[2]))
        response.set_secure_cookie('active', str(matches[3]))
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
    active = response.get_secure_cookie('active')
    print active
    ads = db.getAds(dbConn)
    name = response.get_secure_cookie('name')
    usertype = response.get_secure_cookie('user_type')
    name = response.get_secure_cookie('name')
    response.write(TemplateAPI.render(
        'dashboard.html', response, {"title": "Dashboard", "usertype": usertype, "ads": ads, "active": active, "name": name}))

@loginCheck
def advertisement(response):
    ads = db.getAds(dbConn)
    response.write(TemplateAPI.render("advertisement.html",
                                      response, {"title": "Advertisement", "ads": ads}))


@loginCheck
def advertisementPost(response):
    print "Creating ads"
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
        print "ad succesfully created"
        response.redirect("/advertisement")
    else:
        print "failed to create ad"
        response.redirect("/advertisement?fail=1")


def advertisementDelete(response):
    # print response.get_field('id')
    result = db.deleteAds(dbConn, response.get_field('id'))
    if result:
        response.redirect("/advertisement")
    else:
        response.redirect("/advertisement?fail=1")

@loginCheck
def booking(response):
    response.write(TemplateAPI.render("booking.html", response, {"title": "Booking"}))
    
@loginCheck
def bookingPost(response):
    booking = {}
    booking["title"] = response.get_field("title")
    booking["desc"] = response.get_field("desc")
    booking["datetime"] = response.get_field("datetime")
    booking["charityuserid"] = 1
    booking["donoruserid"] = 1
    booking["active"] = 1
    booking["location"] = response.get_field("location")
    print booking
    print "attempting to create booking"
    result = db.createBooking(dbConn, booking)
    if result:
        print "booking successfully created"
        response.redirect("/dashboard")
    else:
        print "Failed to create booking"
        response.redirect("/booking")

def confirmation(response):
    print "does this work"
    email = base64.b64decode(response.get_field('acc', ''))
    response.clear_cookie('active')
    response.set_secure_cookie('active', str(db.confirmUser(dbConn, email)))
    print db.confirmUser(dbConn, email)
    print response.get_secure_cookie('active')
    response.redirect("/")

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
    server.register('/test', test)
    server.register('/advertisement', advertisement,
                    get=advertisement, post=advertisementPost)
    server.register('/advertisement/delete', advertisementDelete)
    server.register('/resetpassword', resetPassword,
                    get=resetPassword, post=resetPasswordPost)
    server.register('/booking', booking, get=booking, post=bookingPost)
    server.register('/confirmation', confirmation)
    server.run(setup)


if __name__ == "__main__":
    main()
