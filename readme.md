# Introduction
To write a web application, there are various web framework out there. 
They are included but not all, Django, Flask, FastAPI, etc. The Python itself also 
provides a build-in library for developing web application, it is Internet
Protocols and Support library.

Beside the obvious benefits of using the above web framework, there are also disadvantages.
They are included but not all
+ These frameworks implement a bunch of the features and many of them are trivial to the target 
web-application. Consequently, their code-base is quite big that would cause difficulty
in maintaining the application.
+ Each framework has their own limitation as well as its issues. Resolve these limitations and its issue
requires a much time and highly skilled set.

This small project intends to use the library provided by Python to demonstrate
writing a BLOG web-application from front-end to API back-end.

## For Rest API:
+ Use python built-in library, Internet Protocols and Support library.

## For database:
+ The python has specified the database interface at PEP 249. Each instance
database such as PostgresSQL, MySQL, sqlite3, etc have its own implementation.
For this demonstration of *blog* web-application, the sqlite3 is selected.

## For Front-end:
### Template engineer
+ At the time of writing, python does not have the built-in library for template rendering.
Fortunately, Jinja2 library is one candidate for redering the template.

### others
html, css, etc. 

Talk is always cheaper than the actual works.

# Implementaion
## Rest API
Handle getting a post (code snippet)
``` python
    def handler(self):
        # /app
        posts = []

        rows = db.post_read()
        posts = [{'title': row[0], 'content': row[1]} for row in rows]

        tpl = self.app.env.get_template('index.html')
        msg = tpl.render(posts=posts)

        self.app.send_msg(msg)
```

## database
1. Initialization
Create a database if it is not created.
In case it is development environment, add test data (code snippet)
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
