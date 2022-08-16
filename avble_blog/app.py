import http.server as http_srv
from http import HTTPStatus, cookies
from json import load
import socketserver
import re
import uuid
from urllib.parse import urlparse, parse_qs


from jinja2 import Environment
from jinja2.loaders import FileSystemLoader

from . import db


class BlogHandler(http_srv.BaseHTTPRequestHandler):
    
    server_version = "BlogHandler 1.0"

    session = []

    def __init__(self, *args, **kwargs):

        # Front-end setup
        self.env = Environment(loader=FileSystemLoader('avble_blog/template'))
        self.env_admin = Environment(loader=FileSystemLoader('avble_blog/template/admin'))

        super().__init__(*args, **kwargs)

    # Utility function
    def send_msg(self, msg_body:str = None, status_code:HTTPStatus = HTTPStatus.OK):
        # send the message
        # 
        self.send_response(status_code)
        if msg_body != None:
            self.send_header("Content-Length", len(msg_body.encode()))

        self.end_headers()
        if msg_body != None:
            self.wfile.write(msg_body.encode())

    def send_page_not_found(self):
        """
        return page not foud
        """
        self.send_error(HTTPStatus.NOT_FOUND)
        # self.send_msg(None, HTTPStatus.NOT_FOUND)

    def send_page_in_construction(self):
        """
        return page in the construction
        """
        self.send_msg("Page is under construction")


    def login_handler(self):
        # GET: render the login form 
        # POST form:
        # self.send_response(HTTPStatus.PERMANENT_REDIRECT)
        # self.send_header('Location', '/app')
        # session_id = str(uuid.uuid4())
        # BlogHandler.session.append(session_id)

        # # step 2: send cookie to the header
        # self.send_header('set-cookie', f'session={session_id}')
        # self.end_headers()

        if self.command == 'GET':
            tpl = self.env.get_template('login.html')
            msg = tpl.render()
            self.send_msg(msg)
        elif self.command == 'POST':
            # check authentication


            # redirect to admin page
            
            pass




    # user UI
    def user_handler(self):
        # /app
        #
        # get cookied
        req_cookie = self.headers.get('cookie')
        cookie_ =cookies.SimpleCookie()
        cookie_.load(req_cookie)

        if cookie_['session'].value not in BlogHandler.session:
            # check if it is stored
            self.send_response(HTTPStatus.PERMANENT_REDIRECT)
            self.send_header('Location', '/auth')
            self.end_headers()
            return


        # if yes
        posts = []

        rows = db.post_read()
        posts = [{'title': row[0], 'content': row[1]} for row in rows]

        tpl = self.env.get_template('index.html')
        msg = tpl.render(posts=posts)

        self.send_msg(msg)

    # admin UI
    def admin_handler(self) -> str:
        # /admin?page=post
        # in case the page is ommited.
        url_parser_ = urlparse(self.path)
        dict_par = parse_qs(url_parser_.query)

        page = dict_par.get('page', ['users'])[0]
        if page == 'users':
            return self.admin_users()
        elif page == 'posts':
            return self.admin_posts()
        else:
            return self.send_page_not_found()

    def admin_users(self) -> str:
        tpl = self.env_admin.get_template('users.html')
        users = []
        for id in range(1, 10):
            users.append(('id-' + str(id), 'username_' + str(id)))

        msg = tpl.render(users=users)
        self.send_msg(msg)

    def admin_login(self):
        pass

    def admin_posts(self) -> str:
        self.send_page_in_construction()
    
    # Api handler
    def get_posts_handle(self, post_id):
        """
        This endpoint is used to process an GET /post endpoind
        """
        msg = "content of : " + post_id
        self.send_response(200)
        self.send_header("Content-Length", len(msg.encode()))
        self.end_headers()

        self.wfile.write(msg.encode())

    # handle a GET request
    def do_GET(self):
        """
        GET entry point
        """
        # paths = re.match(r"(/posts/)(\d+)", self.path)
        paths = re.match(r"(^/\w+)(.*)", self.path)

        if paths == None:
            # send invalid request
            self.send_response(HTTPStatus.BAD_REQUEST)
            self.end_headers()
        
        action = paths.groups()[0]
        action = action.strip('/')
        print("DEBUG do_GET: ", action)
        if action == 'posts':
            # Rest API
            self.get_posts_handle(paths.groups()[1])
        elif action == 'app':
            # user app
            self.user_handler()
        elif action == 'admin':
            # admin page
            self.admin_handler()
        elif action == 'login':
            # login page
            self.login_handler()
        else:
            self.send_page_not_found()

    # handle a POST request
    def do_POST(sefl):
        pass


def run_forever(port = 8080):
    Handler = BlogHandler
    with socketserver.TCPServer(("", port), Handler) as httpd:
        print("serving at port", port)
        httpd.serve_forever()