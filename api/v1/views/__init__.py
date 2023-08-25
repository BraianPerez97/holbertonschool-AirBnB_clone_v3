from flask import Blueprint

# Create a Blueprint instance for the views
app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")

# Import the views
from api.v1.views.index import *
