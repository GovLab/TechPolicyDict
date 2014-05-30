from base import *

#--------------------------------------------------------MAIN PAGE------------------------------------------------------------
class MainHandler(BaseHandler):
    @tornado.web.addslash
    #@tornado.web.authenticated
    def get(self):
        try: 
            user = models.Users.objects.get(email=self.current_user)
        except:
            user = ''
        defined_words = models.Words.objects(status="defined")
        undefined_words = models.Words.objects(status="undefined")
        self.render(
            "index.html",
            page_title='The Tech-Policy Dictionary',
            page_heading='The Tech-Policy Dictionary',
            user=user,
            defined_words = defined_words,
            undefined_words = undefined_words
        )

class AboutHandler(BaseHandler):
    @tornado.web.addslash
    #@tornado.web.authenticated
    def get(self):
        self.render(
            "about.html",
            page_title='About the TPD',
            page_heading='About The TPD',
            user=self.current_user
        )

class LoginHandler(BaseHandler):
    @tornado.web.addslash
    def get(self):
        self.render(
            "login.html", 
            next=self.get_argument("next","/"), 
            message=self.get_argument("error",""),
            page_title="Please Login",
            page_heading="Login to TPD",
            user=self.current_user 
            )

    def post(self):
        email = self.get_argument("email", "")
        password = self.get_argument("password", "").encode('utf-8')
        try: 
            user = models.Users.objects.get(email=email)
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
            page_heading="Register for TPD",
            user=self.current_user
            )

    def post(self):
        email = self.get_argument("email", "")
        name = self.get_argument("name", "")
        try:
            user = models.Users.objects.get(email=email)
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
                newUser = models.Users(
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
        logging.info(self.current_user)
        self.render(
            "submit.html",
            page_title='Submit a Term or Phrase',
            page_heading='Submit Page',
            user = self.current_user
        )

    def post(self):
        action = self.get_argument("action", None)
        #--------------------------------------REQUEST DEFINITION-------------------------
        if action == "request":
            word_name = self.get_argument("word_name", None).strip()
            prettyName = re.sub(r'([^\s\w])+', '', word_name).replace(" ", "-").title()
            word = models.Words(
                name = word_name,
                prettyName=prettyName,
                status="undefined"
            )
        else:
            #--------------------------------------SUBMIT DEFINITION------------------------- 
            word_name = self.get_argument("word_name", None).strip()
            prettyName = re.sub(r'([^\s\w])+', '', word_name).replace(" ", "-").title()
            d = self.get_argument("definition", None)
            category = self.get_argument("category", None)
            self.get_argument("tags", None)
            tags = [x.strip() for x in self.get_argument("tags", None).split(',')]
            user = models.Users.objects.get(email=self.current_user)
            definition = models.Definitions(
                d = d,
                category = category,
                sub = user,
                voteUp = 0, 
                voteDown = 0
            )
            word = models.Words(
                name = word_name,
                prettyName=prettyName,
                tags = tags,
                sub = user,
                status="defined"
            )
            word.defs.append(definition)
        word.save()
        self.redirect("/")

class WordHandler(BaseHandler):
    @tornado.web.addslash
    #@tornado.web.authenticated
    def get(self):
        word_name = self.get_argument("word", "")
        try:
            word = models.Words.objects.get(name=word_name)
        except Exception, e:
            logging.info("Error looking for word: " + str(e))
            word = None
        if word:
            self.render(
                "word.html",
                page_title='TPD-'+word.name,
                page_heading='Word Page',
                word=word,
                user=self.current_user
            )
        else:
            self.render(
                "404.html",
                error = "Word Not Found",
                word=word_name,
                page_heading = "Word Not Found",
                page_title = "Word Not Found",
                user=self.current_user
            )

    def post(self):
        try:
            user = models.Users.objects.get(email=self.current_user)
        except Exception, e:
            logging.info("Could not get user. Are you logged in? " + str(e))
            self.redirect("/login/")
        action = self.get_argument("action", None)
        prettyName = self.get_argument("word_name", None)
        try: 
            word = models.Words.objects.get(prettyName=prettyName)
        except Exception, e:
            logging.info("Error, could not get "+ str(prettyName) + ": " + str(e))
            self.render(
                "404.html",
                error = "Word Not Found",
                page_heading = "Word Not Found",
                page_title = "Word Not Found"
            )
            #--------------------------------------ADD TAGS-------------------------
        if action == "add-tags":
            tags = [x.strip() for x in self.get_argument("tags", None).split(',')]
            for tag in tags:
                if tag not in word.tags:
                    word.tags.append(tag)
            word.save()
            self.redirect("/word/?word="+tornado.escape.url_escape(word.name))
            #--------------------------------------ADD DEFINITION-------------------------
        if action == "define":
            definition = models.Definitions(
                d = self.get_argument("definition", None),
                category = self.get_argument("category", None),
                sub = models.Users.objects.get(email=self.current_user),
                voteUp = 0,
                voteDown = 0
            )
            word.defs.append(definition)
            word.status = "defined"
            word.save()
            self.redirect("/word/?word="+tornado.escape.url_escape(word.name))
            #--------------------------------------ADD NEW DEFINITION-------------------------
        if action == "define_new":
            tags = [x.strip() for x in self.get_argument("tags", None).split(',')]
            definition = models.Definitions(
                d = self.get_argument("definition", None),
                category = self.get_argument("category", None),
                sub = models.Users.objects.get(email=self.current_user),
                voteUp = 0,
                voteDown = 0
            )
            word.defs.append(definition)
            word.tags = tags
            word.status = "defined"
            word.sub = user
            word.save()
            self.redirect("/word/?word="+tornado.escape.url_escape(word.name))
            #--------------------------------------VOTE-------------------------
        if action == "vote":
            definition = self.get_argument("definition", None)
            up_or_down = self.get_argument("vote", None)
            vote = models.Vote(user = user, vote = up_or_down)
            #how do I get the definition I want? For now loop through all
            for d in word.defs:
                if d.d == definition:
                    if user not in d.voted_by:
                        d.votes.append(vote)
                        if up_or_down =="up":
                            d.voteUp = d.voteUp + 1
                        if up_or_down == "down":
                            d.voteDown = d.voteDown + 1
                        new_vote = d.voteUp - d.voteDown
                    else:
                        d.votes.append(vote)
            word.save()
            self.write({"vote": new_vote})



class SearchHandler(BaseHandler):
    @tornado.web.addslash
    #@tornado.web.authenticated
    def get(self):
        tag = self.get_argument("tag", "")
        query = self.get_argument("query", "")
        if tag:
            try:
                words = models.Words.objects(tags__contains=tag)
            except Exception, e:
                logging.info("Error looking for word: " + str(e))
                words = None
        if query:
            try:
                words = models.Words.objects(name__contains=query)
            except Exception, e:
                logging.info("Error looking for word: " + str(e))
                words = None
        if words:
            self.render(
                "search.html",
                page_title='Search Results',
                page_heading='Search Results',
                words = words,
                tag=tag,
                query=query,
                user=self.current_user
            )
        else:
            self.render(
                "search.html",
                page_title='Search Results',
                page_heading='Search Results',
                words = "",
                tag=tag,
                query=query,
                user=self.current_user
            )

class ValidateHandler(BaseHandler):
    def post(self):
        #check if word exists:
        word_name = self.get_argument("word_name", None)
        prettyName = re.sub(r'([^\s\w])+', '', word_name).replace(" ", "-").title()
        logging.info(prettyName)
        try: 
            w = models.Words.objects.get(prettyName=prettyName)
            logging.info('word exists.')
            self.write('{ "error": "This word/phrase has already been submitted." }')
        except:
            logging.info('word does not exist. Carry on.')
            self.write('true')























