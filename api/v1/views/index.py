#!/usr/bin/python3
"""Index Script"""
from api.v1.views import app_views
from flask import jsonify

# Create a route for /status
@app_views.route('/status', methods=['GET'])
def status():
    return jsonify(status="OK")
