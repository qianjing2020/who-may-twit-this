"""
The first file that runs when running the flask app package
"""

from .flask_app import create_app

APP = create_app()