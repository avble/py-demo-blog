import http.server as http_srv
from http import HTTPStatus
import socketserver
import re
from urllib import request



class BlogHandler(http_srv.BaseHTTPRequestHandler):
    
    server_version = "BlogHandler 1.0"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


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
        paths = re.match(r"(/posts/)(\d+)", self.path)

        if paths == None:
            # send invalid request
            self.send_response(HTTPStatus.BAD_REQUEST)
            self.end_headers()
        
        self.get_posts_handle(paths.groups()[1])

    # handle a POST request
    def do_POST(sefl):
        pass


PORT = 8080

Handler = BlogHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()