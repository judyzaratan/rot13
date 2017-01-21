import os

import jinja2
import webapp2

import re

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                                autoescape = True)

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASSWORD_RE = re.compile(r"^.{3,20}$")
EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")

def valid_username(username):
    return USER_RE.match(username)
def valid_password(password):
    return PASSWORD_RE.match(password)
def valid_email(email):
    return EMAIL_RE.match(email)


def rot13(string):
    newString = ""
    # for letter in string:
    #     value = ord(letter)
    #     if ((value <= 77 and value >= 65) or (value <= 109 and value >= 97)):
    #         newLetter = chr(value + 13)
    #     elif(value >= 78 and value <= 90):
    #         newLetter = chr(65 + (90 - value))
    #     elif(value >= 110 and value <= 122):
    #         newLetter = chr(97 + (122 - value))
    #     else:
    if string:
        newString = string.encode('rot13')

    return newString

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))



class MainPage(Handler):
    def get(self):
        self.render("base.html")


class SignUpHandler(Handler):
    def get(self):
        self.render("signup.html")
    def post(self):
        #User inputs
        user_name = self.request.get("username")
        user_password = self.request.get("password")
        user_verify = self.request.get("verify")
        user_email = self.request.get("email")
        # Validity check
        name = valid_username(user_name)
        password = valid_password(user_password)
        email = valid_email(user_email)
        error_username = ""
        error_password = ""
        error_email = ""
        error_verify = ""
        
        if not name:
            error_username = "That's not a valid username."
        if not password:
            error_password = "That's not a valid password."
        elif user_password != user_verify:
            error_verify = "Passwords do not match."
        if not email:
            error_email = "That's not a valid email."

        if(name and password and email and (user_password == user_verify)):
            self.redirect("/welcome?username=" + user_name)
        else:
            self.render("signup.html", username = user_name,
                                password = user_password,
                                email = user_email,
                                error_email = error_email,
                                error_password = error_password,
                                error_username = error_username,
                                error_verify = error_verify)

class WelcomeHandler(Handler):
    def get(self):
        username = self.request.get('username')
        if valid_username(username):
            self.render('welcome.html', username = username)
        else:
            self.redirect('/signup')

class Rot13Handler(Handler):
    def get(self):
        self.render("rot13.html")
    def post(self):
        change = self.request.get('text')
        newChange = rot13(change)
        self.render("rot13.html", string = newChange);



app = webapp2.WSGIApplication([('/', MainPage),
                                ('/welcome', WelcomeHandler),
                                ('/signup', SignUpHandler),
                                ('/rot13', Rot13Handler)],
                                debug=True)
