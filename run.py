import sys
import sys
from os.path import dirname
import avble_blog.app as avb_app

sys.path.append(dirname(__file__) + '/avble_blog')

avb_app.run_forever(8082)
