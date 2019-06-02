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
    ads = db.getAds(dbConn, "%")
    userid = response.get_secure_cookie("user_id")
    if response.get_secure_cookie('user_id'):
        response.redirect('/dashboard')
    else:
        response.write(TemplateAPI.render(
            'homepage.html', response, {"title": "Homepage", "ads": ads, "userid": userid}))


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
        response.redirect('/dashboard')
    else:
        response.redirect('/login?fail=1')


@loginCheck
def resetPassword(response):
    response.write(TemplateAPI.render('resetPassword.html',
                                      response, {'title': 'Reset Password'}))


@loginCheck
def resetPasswordPost(response):
    user = {}
    user['id'] = response.get_secure_cookie('user_id')
    user['password'] = response.get_field("password")
    passwordReset = db.resetUserPassword(dbConn, user)
    # password reset successful go to dashboard
    if passwordReset:
        response.redirect('/dashboard')


@loginCheck
def logout(response):
    response.clear_cookie('user_id')
    response.clear_cookie('user_type')
    response.redirect('/')


@loginCheck
def dashboard(response):
    usertype = response.get_secure_cookie('user_type')
    userid = int(response.get_secure_cookie("user_id"))
    search = response.get_field('charitySearch', '')
    print search
    if search:
        search = "%" + search + "%"
    else:
        search = '%'
    ads = db.getAds(dbConn, search)

    response.write(TemplateAPI.render(
        'dashboard.html', response, {"title": "Dashboard", "usertype": usertype, "ads": ads, "userid": userid}))


@loginCheck
def advertisement(response):
    search = response.get_field('search', '')
    print search
    usertype = response.get_secure_cookie('user_type')
    userid = int(response.get_secure_cookie("user_id"))
    ads = db.getAds(dbConn, '%')
    response.write(TemplateAPI.render("advertisement.html",
                                      response, {"title": "Advertisement", "ads": ads, "userid": userid, "usertype": usertype}))


@loginCheck
def advertisementPost(response):
    print "Creating ads"
    ad = {}
    ad["title"] = response.get_field("title")
    ad["desc"] = response.get_field("desc")
    ad["imgpath"] = []
    img = response.get_files("img")

    for x in img:
        imgpath = "static/img_store/ad_img/" + str(uuid.uuid4().hex) + ".png"
        try:
            with open(imgpath, 'wb') as img:
                img.write(str(x[2]))
            ad["imgpath"].append(imgpath)
        except:
            pass

    ad["datetime"] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
    ad["userid"] = response.get_secure_cookie('user_id')
    ad["active"] = 1
    result = db.createAd(dbConn, ad)
    if result:
        print "ad succesfully created"
        response.redirect("/dashboard")
    else:
        print "failed to create ad"
        response.redirect("/dashboard?fail=1")


@loginCheck
def advertisementDelete(response):
    result = db.deleteAds(dbConn, response.get_field('id'))
    if result:
        response.redirect("/dashboard")
    else:
        response.redirect("/dashboard?fail=1")


@loginCheck
def adView(response):
    adId = response.get_field('id', '')
    ads = db.viewAd(dbConn, adId)
    usertype = response.get_secure_cookie('user_type')
    userid = int(response.get_secure_cookie("user_id"))
    response.write(TemplateAPI.render(
        "advertisementView.html", response, {"title": "test", "ads": ads, "userid": userid, "usertype": usertype}))


@loginCheck
def advertisementEdit(response):
    ad = {}
    ad["id"] = response.get_field('id', '')
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
    db.editAd(dbConn, ad)
    # view = "/advertisement/view?id=%s" % ad["id"]
    response.redirect('/dashboard')


@loginCheck
def booking(response):
    usertype = response.get_secure_cookie('user_type')
    response.write(TemplateAPI.render(
        "booking.html", response, {"title": "Booking", "usertype": usertype}))


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
    print "attempting to create booking"
    result = db.createBooking(dbConn, booking)
    if result:
        print "booking successfully created"
        response.redirect("/dashboard")
    else:
        print "Failed to create booking"
        response.redirect("/booking")


@loginCheck
def manageAccount(response):
    userid = response.get_secure_cookie('user_id')
    fail = response.get_field('fail', '') == '1'
    user = db.getUser(dbConn, userid)
    print user
    response.write(TemplateAPI.render("manageAccount.html",
                                      response, {"title": "Account", "user": user, "fail":  fail}))


@loginCheck
def editAccount(response):
    user = {}
    user['id'] = response.get_secure_cookie('user_id')
    user['name'] = response.get_field("name")
    user['email'] = response.get_field("email")
    user['usertype'] = response.get_field("usertype")
    result = db.editUser(dbConn, user)
    if result:
        response.redirect("/account")
    else:
        response.redirect("/account?fail=1")


@loginCheck
def userAds(response):
    ads = db.getUserAds(dbConn, response.get_secure_cookie('user_id'))
    usertype = response.get_secure_cookie('user_type')
    print ads
    response.write(TemplateAPI.render(
        "userAds.html", response, {"title": "My Ads", "usertype": usertype, "ads": ads}))


@loginCheck
def searchCharities(response):
    usertype = response.get_secure_cookie('user_type')
    sType = 0
    if int(usertype) == 1:
        sType = 2
    elif int(usertype) == 2:
        sType = 1

    if not response.get_field("charitySearch"):
        charities = db.getCharities(dbConn, sType)
        response.write(TemplateAPI.render("searchCharities.html",
                                          response, {"title": "Charities", "charities": charities, "usertype": usertype}))
    else:
        searchQuery = response.get_field("charitySearch")
        filteredCharities = db.getFilteredCharities(dbConn, searchQuery, sType)
        response.write(TemplateAPI.render("filterCharities.html",
                                          response, {"title": "Charities", "filteredCharities": filteredCharities, "usertype": usertype}))


@loginCheck
def test(response):
    response.write(TemplateAPI.render(
        "test.html", response, {"title": "test"}))


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
    server.register('/advertisement/view', adView)
    server.register('/advertisement/edit', advertisementEdit)
    server.register('/resetpassword', resetPassword,
                    get=resetPassword, post=resetPasswordPost)
    server.register('/booking', booking, get=booking, post=bookingPost)
    server.register('/account', manageAccount,
                    get=manageAccount, post=editAccount)
    server.register('/myadvertisements', userAds)
    server.register('/searchCharities', searchCharities)
    server.run(setup)


if __name__ == "__main__":
    main()
