#!/usr/bin/python3
"""Server file"""
import os
from flask import Flask, jsonify
from flask_cors import CORS
from models import storage
from api.v1.views import app_views

app = Flask(__name__)

# Get host and port from environment variables, or use default values
app_host = os.getenv('HBNB_API_HOST', '0.0.0.0')
app_port = int(os.getenv('HBNB_API_PORT', '5000'))

# Disable strict slashes in URL routing
app.url_map.strict_slashes = False

# Register the blueprint for API views
app.register_blueprint(app_views)

# Enable CORS for the entire application, allowing requests from the specified host
CORS(app, resources={r"/*": {"origins": app_host}})

# Define a function to close the database connection after each request
@app.teardown_appcontext
def teardown_flask(exception):
    """Flask app/request event listener."""
    storage.close()

# Define a custom error handler for 404 (Not Found) errors
@app.errorhandler(404)
def error_404(error):
    """Handles 404 error code"""
    return jsonify(error='Not found'), 404

# Define a custom error handler for 400 (Bad Request) errors
@app.errorhandler(400)
def error_400(error):
    """Handles 400 error code"""
    msg = 'bad request'
    if isinstance(error, Exception) and hasattr(error, 'description'):
        msg = error.description
    return jsonify(error=msg), 400

# Run the application only when this script is executed directly
if __name__ == '__main__':
    app.run(host=app_host, port=app_port, threaded=True)
