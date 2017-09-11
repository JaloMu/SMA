from flask import Blueprint

dns = Blueprint('dns', __name__)

from . import views, errors
