from flask import Blueprint

srpm = Blueprint('srpm', __name__)

from . import views, errors
