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

        page = dict_par.get('page', ['post'])[0]
        if page == 'user':
            return self.admin_users()
        elif page == 'post':
            # check if search
            search_txt = dict_par.get('search', [""])[0]
            if search_txt != "":
                return self.post_search(search_txt)
            else:
            # Pagination
                pagination = dict_par.get('pagination', [0])[0]

                return self.post_read(pagination=int(pagination))
        else:
            return self.app.send_page_not_found()

    def admin_users(self) -> str:
        tpl = self.app.env_admin.get_template('users.html')
        users = []
        for id in range(1, 10):
            users.append(('id-' + str(id), 'username_' + str(id)))

        msg = tpl.render(users=users)
        self.app.send_msg(msg)


    def post_read(self, pagination:int = 0) -> str:
        '''

        '''
        tpl = self.app.env_admin.get_template('posts.html')
        
        posts = []
        limit_low = pagination*10
        rows = db.post_read(limit_low=limit_low)
        posts = [{'id': row[0], 'title': row[1], 'content': row[2], 'created_date': row[3]} for row in rows]

        pag = {}
        pag['cur_num'] = pagination

        msg = tpl.render(posts=posts, pagination=pag)
        self.app.send_msg(msg)

    def post_search(self, text:str):
        '''
        '''
        tpl = self.app.env_admin.get_template('posts.html')
        rows = db.post_search(text)
        posts = [{'id': row[0], 'title': row[1], 'content': row[2], 'created_date': row[3]} for row in rows]

        pag = {}
        pag['cur_num'] = 0

        msg = tpl.render(posts=posts, pagination=pag)
        self.app.send_msg(msg)
