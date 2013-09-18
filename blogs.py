import os, urllib, cgi

from google.appengine.api import users
from google.appengine.ext import ndb
import settings as SETTINGS

import jinja2
import webapp2

JINJA_ENVIRONMENT = jinja2.Environment(
            loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
            extensions=['jinja2.ext.autoescape'])

# Models
class Blogs(ndb.Model):
    author = ndb.UserProperty()
    title = ndb.StringProperty()
    text = ndb.TextProperty(indexed=False)
    post_date = ndb.DateTimeProperty(auto_now_add=True)

def blog_key():
    """Constructs a Datastore key for a Guestbook entity with guestbook_name."""
    return ndb.Key('Ouroborothon', 'Blog')

# Views
class BlogList(webapp2.RequestHandler):

    def get(self):
        context = {'title':'Title','message':'hello world'}
        context.update({'site_title':SETTINGS.BLOG_NAME})
        blogs_query = Blogs.query(
                ancestor=blog_key()).order(-Blogs.post_date)
        blogs = blogs_query.fetch(10)
        context.update({'blogs':blogs})

        template = JINJA_ENVIRONMENT.get_template('templates/blogs/blogs_list.html')
        self.response.write(template.render(context))

class BlogEditor(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if not user:
            self.redirect(users.create_login_url(self.request.uri))
            return 
        if user.nickname() != SETTINGS.BLOG_OWNER:
            self.redirect(users.create_logout_url('/'))
            return 
        
        context = {'title':'Title','message':'hello world'}
        context = {'use_mce':True}
        if user:
            context.update({'site_title':user.nickname()})
        template = JINJA_ENVIRONMENT.get_template('templates/blogs/editor.html')
        self.response.write(template.render(context))

    def post(self):
        user = users.get_current_user()
        if not user:
            self.redirect(users.create_login_url(self.request.uri))
            return 
        if user.nickname() != SETTINGS.BLOG_OWNER:
            self.redirect(users.create_logout_url('/'))
            return 

        title = cgi.escape(self.request.get('title'))
        text = self.request.get('text')
        author = users.get_current_user()

        blog = Blogs(parent=blog_key())
        blog.title = title
        blog.text = text
        blog.author = author

        blog.put()

        self.redirect('/')

application = webapp2.WSGIApplication([
    ('/editor', BlogEditor),
    ('/', BlogList),
], debug=True)

editor = webapp2.WSGIApplication([
    ('/editor', BlogEditor),
], debug=True)
