from urllib.parse import unquote, urlparse, parse_qs
from http import HTTPStatus, cookies

from . import db

class AdminUI:
    def __init__(self, app_blog):
        self.app = app_blog
        pass

    # admin UI
    def handler(self) -> str:
        # /admin?page=post
        # in case the page is ommited.
        url_parser_ = urlparse(self.app.path)
        dict_par = parse_qs(url_parser_.query)

        req_cookie = self.app.headers.get('cookie', None)
        if req_cookie == None:
            # redirect 
            # check if it is stored
            # self.send
            self.app.send_response(HTTPStatus.PERMANENT_REDIRECT)
            self.app.send_header('Location', '/login')
            self.app.end_headers()

        cookie_ =cookies.SimpleCookie()
        cookie_.load(req_cookie)
        if self.app.sess.is_existed(cookie_['session'].value) is False:
            # check if it is stored
            self.app.send_response(HTTPStatus.PERMANENT_REDIRECT)
            self.app.send_header('Location', '/login')
            self.app.end_headers()
            return

        page = dict_par.get('page', ['users'])[0]
        if page == 'users':
            return self.admin_users()
        elif page == 'posts':
            return self.admin_posts()
        else:
            return self.app.send_page_not_found()

    def admin_users(self) -> str:
        tpl = self.app.env_admin.get_template('users.html')
        users = []
        for id in range(1, 10):
            users.append(('id-' + str(id), 'username_' + str(id)))

        msg = tpl.render(users=users)
        self.app.send_msg(msg)


    def admin_posts(self) -> str:
        tpl = self.app.env_admin.get_template('posts.html')
        
        posts = []
        rows = db.post_read()
        posts = [{'title': row[0], 'content': row[1]} for row in rows]

        msg = tpl.render(posts=posts)
        self.app.send_msg(msg)