from flask import (
    Flask,
    render_template,
    request,
    json as flask_json,
    jsonify
)
from livereload import Server
import os
import pandas as pd

from blueprints.himdex_blueprint import himdex_blueprint

from services.gbq_functions import get_all_seasons

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

@app.route('/bootstrap')
def bootstrap():
    return render_template('index.html')

@app.route('/api/get_season_players', methods = ['POST'])
def get_season_players():
    filename = os.path.join(app.static_folder, 'data', 'season_players.json')

    with open(filename) as test_file:
        season_players = flask_json.load(test_file)

        return jsonify(season_players), 200
        
if __name__ == '__main__':
    server = Server(app.wsgi_app)
    server.serve(port=5000, debug=False, restart_delay=0)