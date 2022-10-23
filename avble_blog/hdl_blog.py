from . import db

class BlogApp:

    def __init__(self, blog_app):
        self.app = blog_app

    # user UI
    def handler(self):
        # /app
        # if the user is logged in
        # otherwise the user is NOT logged in
        posts = []

        rows = db.posts_read(num_row=6)
        posts = [{'title': row[1], 'content': row[2]} for row in rows]

        tpl = self.app.env.get_template('index.html')
        msg = tpl.render(posts=posts)

        self.app.send_msg(msg)


    def authenticated_usr_handle(self):
        '''
        + Display the posts of user
        '''
        pass