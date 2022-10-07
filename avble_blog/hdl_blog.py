from . import db

class BlogApp:

    def __init__(self, blog_app):
        self.app = blog_app

    # user UI
    def handler(self):
        # /app
        posts = []

        rows = db.post_read()
        posts = [{'title': row[0], 'content': row[1]} for row in rows]

        tpl = self.app.env.get_template('index.html')
        msg = tpl.render(posts=posts)

        self.app.send_msg(msg)