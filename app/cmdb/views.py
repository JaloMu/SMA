from flask import render_template, request
from . import cmdb
from app.utils import req_m
from os.path import dirname
from flask_login import login_required, current_user


team = dirname(__file__).split("/")[-1]


@cmdb.route('/listserver.html', methods=["GET", "POST"])
@login_required
def listserver():
    if (req_m(request) == 1):
        print(request.get_json())
        return render_template('cmdb/listserver.html', team=team, username=current_user.username)
    if (req_m(request) == 0):
        return render_template('cmdb/listserver.html', team=team, username=current_user.username)
    else:
        return render_template("cmdb/listserver.html", team=team, username=current_user.username)


@cmdb.route('/addServer.html', methods=["GET", "POST"])
@login_required
def addserver():
    if (req_m(request) == 1):
        print(request.get_json())
        return render_template('cmdb/addServer.html', team=team, username=current_user.username)
    if (req_m(request) == 0):
        return render_template('cmdb/addServer.html', team=team, username=current_user.username)
    else:
        return render_template("cmdb/addServer.html", team=team, username=current_user.username)


@cmdb.route('/listservice.html', methods=["GET", "POST"])
@login_required
def listservice():
    if (req_m(request) == 1):
        print(request.get_json())
        return render_template('cmdb/listservice.html', team=team, username=current_user.username)
    if (req_m(request) == 0):
        return render_template('cmdb/listservice.html', team=team, username=current_user.username)
    else:
        return render_template("cmdb/listservice.html", team=team, username=current_user.username)
