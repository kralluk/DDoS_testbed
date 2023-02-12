from flask import Flask

app = Flask(__name__)

from app import routes, initialize

initialize.before_first_request_funcs(app)
initialize.at_exit_funcs(app)
