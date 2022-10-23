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
            self.app.send_response(HTTPStatus.TEMPORARY_REDIRECT)
            self.app.send_header('Location', '/login')
            self.app.end_headers()

        cookie_ =cookies.SimpleCookie()
        cookie_.load(req_cookie)

        if self.app.sess.is_existed(cookie_['session'].value) is False:
            # check if it is stored
            self.app.send_response(HTTPStatus.TEMPORARY_REDIRECT)
            self.app.send_header('Location', '/login')
            self.app.end_headers()
            return

        page = dict_par.get('page', ['posts'])[0]
        if page == 'user':
            return self.admin_users()
        elif page == 'posts':
            # check if search
            action = dict_par.get('action', [""])[0]
            if action == "search":
                # Reading (Searching)
                search_txt = dict_par.get('search', [""])[0]
                return self.posts_search(search_txt)
            elif action == "delete":
                id = dict_par.get('id', [-1])[0]
                return self.posts_delete(id)
            elif action == "read_a_post":
                id = dict_par.get('id', [-1])[0]
                self.post_read(id)
            else:
                # Reading (all with pagination)
                pagination = dict_par.get('pagination', [0])[0]
                return self.posts_read(pagination=int(pagination))
        elif page == 'post':
            if self.app.command == "POST":
                # update post
                id = self.app.form.get('id', [-1])[0]
                title = self.app.form.get('title', ['title-default'])[0]
                content = self.app.form.get('content', ['content-default'])[0]
                # title = self.app.form['title']

                self.post_update(id, title, content)
        else:
            return self.app.send_page_not_found()

    def admin_users(self) -> str:
        tpl = self.app.env_admin.get_template('users.html')
        users = []
        for id in range(1, 10):
            users.append(('id-' + str(id), 'username_' + str(id)))

        msg = tpl.render(users=users)
        self.app.send_msg(msg)

    def post_read(self, id:int)->str:
        '''
        '''
        tpl = self.app.env_admin.get_template('post.html')
        
        row = db.post_read(id)
        post = None
        if row != None:
            # len(row)
            post = {'id': row[0], 'title': row[1], 'title_long': row[2], 'content': row[3], 'created_date': row[4]}

        msg = tpl.render(post=post)
        self.app.send_msg(msg)

    def post_update(self, id:int, title:str, content:str):
        # Redirection to posts_read
        db.post_update(id, title, content)

        # Render page again
        self.post_read(id)

    def posts_read(self, pagination:int = 0) -> str:
        '''
        '''
        tpl = self.app.env_admin.get_template('posts.html')
        
        posts = []
        limit_low = pagination*10
        rows = db.posts_read(limit_low=limit_low)
        posts = [{'id': row[0], 'title': row[1], 'title_long': row[2], 'created_date': row[4]} for row in rows]

        pag = {}
        pag['cur_num'] = pagination

        msg = tpl.render(posts=posts, pagination=pag)
        self.app.send_msg(msg)

    def posts_search(self, text:str):
        '''
        '''
        tpl = self.app.env_admin.get_template('posts.html')
        rows = db.posts_search(text)
        posts = [{'id': row[0], 'title': row[1], 'title_long': row[2], 'created_date': row[3]} for row in rows]

        pag = {}
        pag['cur_num'] = 0

        msg = tpl.render(posts=posts, pagination=pag)
        self.app.send_msg(msg)

    def posts_delete(self, id:int):
        '''
        '''
        db.posts_delete(id)
        self.posts_read()