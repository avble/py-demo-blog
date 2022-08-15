import http.server as http_srv
from http import HTTPStatus
import socketserver
import re

from jinja2 import Environment
from jinja2.loaders import FileSystemLoader

from . import db


class BlogHandler(http_srv.BaseHTTPRequestHandler):
    
    server_version = "BlogHandler 1.0"

    def __init__(self, *args, **kwargs):

        # Front-end setup
        self.env = Environment(loader=FileSystemLoader('avble_blog/template'))
        super().__init__(*args, **kwargs)

    # Utility function
    def send_msg(self, msg_body:str = None, status_code:HTTPStatus = HTTPStatus.OK):
        # send the message whose status is 200
        # 
        self.send_response(status_code)
        if msg_body != None:
            self.send_header("Content-Length", len(msg_body.encode()))

        self.end_headers()
        if msg_body != None:
            self.wfile.write(msg_body.encode())

    # webapp user
    def app_index(self):
        # /app
        #
        posts = []
        # posts.append({
        #     "title": "title 01",
        #     "content": "This is the content of title 01."
        # })

        # posts.append({
        #     "title": "title 02",
        #     "content": "This is the content of title 02."
        # })

        # posts.append({
        #     "title": "title 03",
        #     "content": "This is the content of title 03."
        # })

        rows = db.post_read()
        posts = [{'title': row[0], 'content': row[1]} for row in rows]

        tpl = self.env.get_template('index.html')
        msg = tpl.render(posts=posts)

        self.send_msg(msg)


    # webapp admin
    def admin_index(self):
        # /admin
        pass

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
            self.get_posts_handle(paths.groups()[1])
        elif action == 'app':
            self.app_index()
        elif action == 'admin':
            self.admin_index()

    # handle a POST request
    def do_POST(sefl):
        pass


def run_forever(port = 8080):
    Handler = BlogHandler
    with socketserver.TCPServer(("", port), Handler) as httpd:
        print("serving at port", port)
        httpd.serve_forever()