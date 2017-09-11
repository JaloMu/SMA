from flask import render_template, request, jsonify
from . import saltstack
from app.utils import req_m
from os.path import dirname
from flask_login import login_required, current_user


team = dirname(__file__).split("/")[-1]


@saltstack.route('/deploy.html', methods=["GET", "POST"])
@login_required
def deploy():
    if (req_m(request) == 1):
        print(request.get_json())
        return render_template('saltstack/deploy.html', team=team, username=current_user.username)
    if (req_m(request) == 0):
        return render_template('saltstack/deploy.html', team=team, username=current_user.username)
    else:
        return render_template("saltstack/deploy.html", team=team, username=current_user.username)


@saltstack.route('/publish.html', methods=["GET", "POST"])
@login_required
def publish():
    if (req_m(request) == 1):
        print(request.get_json())
        return render_template('saltstack/publish.html', team=team, username=current_user.username)
    if (req_m(request) == 0):
        return render_template('saltstack/publish.html', team=team, username=current_user.username)
    else:
        return render_template("saltstack/publish.html", team=team, username=current_user.username)
