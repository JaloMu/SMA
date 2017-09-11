from flask import render_template, request, url_for, redirect, flash
from . import auth
from .. import db
from os.path import dirname
from ..models.users import Users
from flask_login import login_user, logout_user, login_required, current_user
from ..utils import req_m
from datetime import datetime


team = dirname(__file__).split("/")[-1]


@auth.route("/login", methods=["GET", "POST"])
def login():
    msg = None
    if current_user.is_authenticated:
        return redirect(request.args.get("next") or url_for('main.index'))
    if (req_m(request) == 1):
        user = Users.query.filter_by(email=request.form.get("email", type=str, default=None)).first()
        if user is not None:
            if user.verify_password(request.form.get("password", type=str, default=None)):
                user.last_login = datetime.now()
                db.session.add(user)
                db.session.commit()
                login_user(user)
                flash('登录成功')
                return redirect(request.args.get("next") or url_for('main.index'))
            else:
                msg = "密码错误"
        else:
            msg = "用户不存在"
    return render_template("sauth/login.html", error=msg)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('auth.login'))
