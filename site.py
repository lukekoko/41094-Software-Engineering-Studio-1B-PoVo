from tornado import Server
import TemplateAPI
from random import randint
import json

def dummy():
    print "Started"

def homePage(response):
    response.write(TemplateAPI.render('homepage.html', response, {}))

def randPage(response):
    response.write("Today's Random number is: " + str(ranGen()))

def ranGen():
    return randint(0, 10)


server = Server('0.0.0.0', 80)
server.register("/", homePage)
server.register("/rand", randPage)


server.run(dummy)
