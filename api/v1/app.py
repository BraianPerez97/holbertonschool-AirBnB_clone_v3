#!/usr/bin/python3
"""Server file"""
import os
from flask import Flask, jsonify

import models
from models import storage
from api.v1.views import app_views


def create_app(config_name):
    app = Flask(__name__)

    app.config.from_object(config_name)

    app.register_blueprint(app_views)

    @app.teardown_appcontext
    def close_db(error):
        storage.close()

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"error": "Not found"}), 404

    return app


app = create_app(os.getenv('APP_CONFIG', 'default'))

if __name__ == "__main__":
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(os.getenv('HBNB_API_PORT', 5000))
    app.run(host=host, port=port, threaded=True)
