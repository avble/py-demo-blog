# Introduction
To write a web application, there are various web framework out there. 
They are included but not all, Django, Flask, etc. The Python itself also 
provides a build-in library for developing web application, it is Internet
Protocols and Support library.

This writing intends to use the library provided by Python to demonstrate
writing a restfull Api for blog web-application.

For rest api:
+ Use python built-in library, Internet Protocols and Support library.

For database:
+ The python has specified the database interface at PEP 249. Each instance
database such as PostgresSQL, MySQL, sqlite3, etc have its own implementation.
For this demonstration of blog web-application, the sqlite3 is selected.

For Front-end:
+ At the time of writing, python does not have the built-in library for template rendering.
Fortunately, Jinja2 library is one candidate for redering the template.

Talk is always cheaper than the actual works.

# Implementaion
## Rest API
Handle getting a post
``` python
def get_posts_handle(self, post_id):
    """
    This endpoint is used to process an GET /post endpoind
    """
    msg = "content of : " + post_id
    self.send_response(200)
    self.send_header("Content-Length", len(msg.encode()))
    self.end_headers()

    self.wfile.write(msg.encode())
```

Create a new post
``` python
# TBU 

```


## database
1. Initializatino
Create a database if it is not created.
In case it is development environment, add test data
``` python
def db_init():
    """
    Create a database if it does not exists
    """
    # If the db has not there, create the database
    if not os.path.isfile(DB_NAME):
        print ("Create database ")
        db_execute_schema()

    # check if it is the prod or dev environment
    if 'prod' in g_db:
        if g_db['prod'] == False:
            db_add_test_data()
```

## Front end app
```python

```




The entire source code can be found [here](https://github.com/avble/py-demo-blog)

# Reference
[1] https://docs.python.org/3.9/library/http.server.html, 
