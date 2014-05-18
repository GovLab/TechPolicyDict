from base import *

#--------------------------------------------------------MAIN PAGE------------------------------------------------------------
class MainHandler(BaseHandler):
    @tornado.web.addslash
    #@tornado.web.authenticated
    def get(self):
        try: 
            user = models.User.objects.get(email=self.current_user)
        except:
            user = ''
        self.render(
            "index.html",
            page_title='Heroku Funtimes',
            page_heading='Main Page',
            user=user
        )

class AboutHandler(BaseHandler):
    @tornado.web.addslash
    #@tornado.web.authenticated
    def get(self):
        self.render(
            "about.html",
            page_title='Heroku Funtimes',
            page_heading='About Page',
        )

class LoginHandler(BaseHandler):
    @tornado.web.addslash
    def get(self):
        self.render(
            "login.html", 
            next=self.get_argument("next","/"), 
            message=self.get_argument("error",""),
            page_title="Please Login",
            page_heading="Login to TPD" 
            )

    def post(self):
        email = self.get_argument("email", "")
        password = self.get_argument("password", "").encode('utf-8')
        try: 
            user = models.User.objects.get(email=email)
        except Exception, e:
            logging.info('unsuccessful login')
            error_msg = u"?error=" + tornado.escape.url_escape("User does not exist")
            self.redirect(u"/login" + error_msg)
        if user and user.password and bcrypt.hashpw(password, user.password.encode('utf-8')) == user.password:
            logging.info('successful login for '+email)
            self.set_current_user(email)
            self.redirect("/")
        else: 
            logging.info('unsuccessful login')
            error_msg = u"?error=" + tornado.escape.url_escape("Incorrect Password")
            self.redirect(u"/login" + error_msg)

    def set_current_user(self, user):
        logging.info('setting ' + user)
        if user:
            self.set_secure_cookie("user", tornado.escape.json_encode(user))
        else: 
            self.clear_cookie("user")

class RegisterHandler(LoginHandler):
    @tornado.web.addslash
    def get(self):
        self.render(
            "register.html", 
            next=self.get_argument("next","/"),
            message=self.get_argument("error",""),
            page_title="Register",
            page_heading="Register for TPD"
            )

    def post(self):
        email = self.get_argument("email", "")
        name = self.get_argument("name", "")
        try:
            user = models.User.objects.get(email=email)
        except:
            user = ''
        if user:
            error_msg = u"?error=" + tornado.escape.url_escape("Login name already taken")
            self.redirect(u"/register" + error_msg)
        else: 
            password = self.get_argument("password", "")
            password_confirm = self.get_argument("password_confirm", "")
            if password != password_confirm:
                error_msg = u"?error=" + tornado.escape.url_escape("Passwords do not match.")
                self.redirect(u"/register" + error_msg)
            else:
                hashedPassword = bcrypt.hashpw(password, bcrypt.gensalt(8))
                newUser = models.User(
                    email=email,
                    name=name,
                    password = hashedPassword
                    )
                newUser.save()
                self.set_current_user(email)
                self.redirect("/")

class LogoutHandler(BaseHandler): 
    def get(self):
        self.clear_cookie("user")
        self.redirect(u"/login")

class SubmitHandler(BaseHandler):
    @tornado.web.addslash
    #@tornado.web.authenticated
    def get(self):
        self.render(
            "submit.html",
            page_title='Heroku Funtimes',
            page_heading='Submit Page',
        )

class WordHandler(BaseHandler):
    @tornado.web.addslash
    #@tornado.web.authenticated
    def get(self):
        self.render(
            "word.html",
            page_title='Heroku Funtimes',
            page_heading='Word Page',
        )

class SearchHandler(BaseHandler):
    @tornado.web.addslash
    #@tornado.web.authenticated
    def get(self):
        self.render(
            "search.html",
            page_title='Heroku Funtimes',
            page_heading='Search Page',
        )

























