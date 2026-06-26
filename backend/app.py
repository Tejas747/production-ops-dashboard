import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from flask import Flask, send_from_directory
from flask_cors import CORS

from routes.infrastructure import infrastructure_bp
from routes.application import application_bp
from routes.database import database_bp
from routes.cache import cache_bp
from routes.messaging import messaging_bp
from routes.external import external_bp
from routes.security import security_bp
from routes.hygiene import hygiene_bp
from routes.cost import cost_bp
from routes.reliability import reliability_bp
from routes.incidents import incidents_bp
from routes.predictive import predictive_bp
from routes.ai_assistant import ai_bp

app = Flask(__name__, static_folder='../frontend', static_url_path='')
CORS(app)

app.register_blueprint(infrastructure_bp)
app.register_blueprint(application_bp)
app.register_blueprint(database_bp)
app.register_blueprint(cache_bp)
app.register_blueprint(messaging_bp)
app.register_blueprint(external_bp)
app.register_blueprint(security_bp)
app.register_blueprint(hygiene_bp)
app.register_blueprint(cost_bp)
app.register_blueprint(reliability_bp)
app.register_blueprint(incidents_bp)
app.register_blueprint(predictive_bp)
app.register_blueprint(ai_bp)

@app.route('/')
def index():
    return send_from_directory('../frontend', 'index.html')

@app.route('/api/health')
def health():
    return {"status": "ok"}

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host='0.0.0.0', port=port)