from flask import (
    Flask,
    request,
    jsonify
)
import pandas as pd
from blueprints.himdex_blueprint import himdex_blueprint

app = Flask(__name__)

app.register_blueprint(himdex_blueprint)

if __name__ == '__main__':
    app.run('localhost', load_dotenv = True)