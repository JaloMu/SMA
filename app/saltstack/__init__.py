from flask import Blueprint


saltstack = Blueprint('saltstack', __name__)

from . import views, errors
