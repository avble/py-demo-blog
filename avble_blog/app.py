import http.server as http_srv
from http import HTTPStatus, cookies
from json import load
import socketserver
import re
from urllib.parse import unquote, urlparse, parse_qs
from urllib import parse as url_parse


from jinja2 import Environment
from jinja2.loaders import FileSystemLoader

from . import session
from . import hdl_admin, hdl_login, hdl_blog, hdl_rest

class BlogHandler(http_srv.BaseHTTPRequestHandler):
    
    server_version = "BlogHandler 1.0"
    sess = session.Session()

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

    # handle a GET request
    def request_dispatch(self):
        """
        """
        # paths = re.match(r"(/posts/)(\d+)", self.path)
        paths = re.match(r"(^/\w+)(.*)", self.path)

        # print('trace: headers:', self.headers)
        # print('trace: path:', self.path)
        if paths == None:
            # send invalid request
            self.send_response(HTTPStatus.BAD_REQUEST)
            self.end_headers()
            return
        
        # parsing form if any
        if self.command == 'POST':
            # print(f'TRACE-login-POST header/content-type: {self.headers.get_content_type()} \n')
            if self.headers.get_content_type() == 'application/x-www-form-urlencoded':
                # read body
                con_len = self.headers.get('Content-Length')
                content = self.rfile.read(int(con_len))
                # unquote
                url_unquoted = url_parse.unquote(content.decode())
                self.form = url_parse.parse_qs(url_unquoted)

                # print(f'[DEBUG] form data: {self.form}')

        action = paths.groups()[0]
        action = action.strip('/')
        if action == 'api' and self.command == 'GET':
            # Rest API
            rest = hdl_rest.RestHandler(self)
            rest.hanlder(paths.groups()[1])
        elif action == 'app' and self.command == 'GET':
            # user app
            blg_app = hdl_blog.BlogApp(self)
            blg_app.handler()
        elif action == 'admin': # and self.command == 'GET':
            # admin page
            adm = hdl_admin.AdminUI(self)
            adm.handler()
            # self.admin_handler()
        elif action == 'login':
            # accept both GET and POST command
            # login page
            lgin = hdl_login.LoginHandler(self)
            lgin.handler()
        else:
            self.send_page_not_found()

    def do_GET(self):
        self.request_dispatch()
        pass

    # handle a POST request
    def do_POST(self):
        self.request_dispatch()


def run_forever(port = 8080):
    Handler = BlogHandler
    with socketserver.TCPServer(("", port), Handler) as httpd:
        print("serving at port", port)
        httpd.serve_forever()