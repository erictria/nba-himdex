from flask import (
    Flask,
    render_template,
    request,
    jsonify
)
from livereload import Server
import pandas as pd

from blueprints.himdex_blueprint import himdex_blueprint

from services.db_functions import get_all_seasons

app = Flask(__name__, template_folder='app/templates', static_folder='app/static')

app.register_blueprint(himdex_blueprint)

@app.route('/')
def index():
    # return render_template('landing.html')

    seasons = get_all_seasons()
    return render_template(
        'landing.html', 
        title = 'Landing', 
        seasons = seasons
    )

if __name__ == '__main__':
    server = Server(app.wsgi_app)
    server.serve(port=5000, debug=False, restart_delay=0)