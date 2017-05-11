#!/usr/bin/env python
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from testex import create_app

app = create_app("config.py")
from flasgger import Swagger
Swagger(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=4000)
