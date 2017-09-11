from flask import render_template, request
from . import main
from os.path import dirname
from flask_login import login_required


team = dirname(__file__).split("/")[-1]


@main.route("/index.html", methods=["GET", "POST"])
@main.route("/", methods=["GET", "POST"])
@login_required
def index():
    return render_template('smain/index.html')


@main.route("/skin_config/", methods=["GET", "POST"])
def skin_config():
    return render_template("skin_config.html")
