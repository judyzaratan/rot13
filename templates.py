import os

import jinja2
import webapp2


template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                                autoescape = True)
def rot13(string):
    newString = ""
    for letter in string:
        value = ord(letter)
        if ((value <= 77 and value >= 65) or (value <= 109 and value >= 97)):
            newLetter = chr(value + 13)
        elif(value >= 78 and value <= 90):
            newLetter = chr(65 + (90 - value))
        elif(value >= 110 and value <= 122):
            newLetter = chr(97 + (122 - value))
        else:
            newLetter = letter
        newString += newLetter
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
        self.render("rot13.html")
    def post(self):
        change = self.request.get('namestring')
        newChange = rot13(change)
        self.render("rot13.html", string = newChange);


app = webapp2.WSGIApplication([('/', MainPage)],
                                debug=True)
