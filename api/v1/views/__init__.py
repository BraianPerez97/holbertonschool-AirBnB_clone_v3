#!/usr/bin/python3
"""Contains the API blueprint"""
from flask import Blueprint

# Create the blueprint instance
app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

# Import views to be included in the blueprint
from api.v1.views.index import *
from api.v1.views.cities import *
from api.v1.views.states import *
from api.v1.views.amenities import *
