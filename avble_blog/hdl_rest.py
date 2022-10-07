
class RestHandler:
    def __inti__(self, blog_app):
        self.app = blog_app

    # Api handler
    def hanlder(self, post_id):
        """
        This endpoint is used to process an GET /post endpoind
        """
        msg = "content of : " + post_id
        self.app.send_response(200)
        self.app.send_header("Content-Length", len(msg.encode()))
        self.app.end_headers()

        self.app.wfile.write(msg.encode())