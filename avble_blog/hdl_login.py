import uuid
from urllib.parse import unquote, urlparse, parse_qs
from urllib import parse as url_parse
from http import HTTPStatus, cookies

class LoginHandler():

    def __init__(self, app_blog):
        self.app = app_blog

    def handler(self):
        # called by both POST and GET method
        # GET: render the login form
        # POST form: 
        # 

        if self.app.command == 'GET':
            print("Trace-login-GET")
            tpl = self.app.env.get_template('login.html')
            msg = tpl.render()
            self.app.send_msg(msg)
            return
        elif self.app.command == 'POST':
            print('TRACE-login-POST')
            if self.app.headers.get_content_type() == 'application/x-www-form-urlencoded':
                # read body
                # con_len = self.app.headers.get('Content-Length')
                # content = self.app.rfile.read(int(con_len))
                # # unquote
                # url_unquoted = url_parse.unquote(content.decode())
                # self.app.form = url_parse.parse_qs(url_unquoted)

                # 
                usr = self.app.form['username'][0]
                if usr == 'admin':
                    # Redirect to admin page
                    self.app.send_response(HTTPStatus.TEMPORARY_REDIRECT)
                    self.app.send_header('Location', '/admin')
                    session_id = str(uuid.uuid4())
                    self.app.sess.add(session_id)

                    # step 2: send cookie to the header
                    self.app.send_header('set-cookie', f'session={session_id}')
                    self.app.end_headers()
                else: 
                    tpl = self.app.env.get_template('login.html')
                    msg = tpl.render()
                    self.app.send_msg(msg)