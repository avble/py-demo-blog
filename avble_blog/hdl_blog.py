import markdown
from urllib.parse import urlparse, parse_qs

from . import db

class BlogApp:

    def __init__(self, blog_app):
        self.app = blog_app

    # user UI
    def handler(self):
        # url scheme
        # app: list most recent post
        # app?page=post&&id=12: list the full post

        url_parser_ = urlparse(self.app.path)
        dict_par = parse_qs(url_parser_.query)

        page = dict_par.get('page', ['main'])[0]
        if page == 'main':
            posts = []

            rows = db.posts_read(num_row=6)
            posts = [{'title': row[1], 'title_long': row[2]} for row in rows]

            tpl = self.app.env.get_template('index.html')
            msg = tpl.render(posts=posts)

            self.app.send_msg(msg)
        else:
            id = int(dict_par.get('id', ['0'])[0])
            self.post_view(id)


    def post_view(self, id:int):
        post = db.post_read(id)

        p = {}
        p['content'] = markdown.markdown(post[3])
        p['title'] = post[1]
        p['title_long'] = post[2]


        tpl = self.app.env.get_template('post.html')
        msg = tpl.render(post=p)
        self.app.send_msg(msg)

    def authenticated_usr_handle(self):
        '''
        + Display the posts of user
        '''
        pass