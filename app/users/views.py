from flask import render_template, request, Response, redirect, url_for, current_app
from . import users
from .. import db
from app.utils import req_m, create_uuid, test_print
from os.path import dirname
from flask_login import login_required, current_user
from ..models.users import Users, UserGroups, Role, Teams, Sections


team = dirname(__file__).split("/")[-1]
actives = 'active'
#####################################################################################################################################################
#                                                                                                                                                   #
#                                                                                                                                                   #
#                                                   '''Users views'''                                                                               #
#                                                                                                                                                   #
#                                                                                                                                                   #
#####################################################################################################################################################


@users.route('/user_profile', methods=["GET"])
@login_required
def user_profile():
    '''
    个人信息展示
    '''
    return render_template("suser/profile.html")
#####################################################################################################################################################


@users.route('/add', methods=["GET", "POST"])
@login_required
def add():
    '''
    添加用户
    '''
    group_all = UserGroups.query.all()
    role_all = Role.query.all()
    section_all = Sections.query.all()
    teams_all = Teams.query.all()
    user_total = len(Users.query.all())
    user_active = len(Users.query.filter_by(is_active=True).all())
    err = ""
    msg = ""
    if (req_m(request) == 1):
        u = Users.query.filter_by(username=request.form.get("username", type=str)).all()
        user = Users()
        if not u:
            for k, v in request.form.items():
                if v != "":
                    setattr(user, k, v)
            user.create_user = current_user.username
            user.updata_user = current_user.username
            user.uuid = create_uuid(user.username)
            db.session.add(user)
            db.session.commit()
            msg = "{} 添加成功".format(request.form.get('username', type=str))
            err = None
        else:
            msg = None
            err = "{} 用户存在!!!".format(request.form.get("username", type=str))
    return render_template("suser/user_add.html",
                           group_all=group_all,
                           role_all=role_all,
                           section_all=section_all,
                           teams_all=teams_all,
                           user_active=user_active,
                           user_total=user_total,
                           error=err,
                           msg=msg)
#####################################################################################################################################################


@users.route('/del', methods=["GET", "POST"])
@login_required
def delete():
    '''
    删除用户
    '''
    if (req_m(request) == 1):
        ids = request.form.get("id", type=str, default=None)
        if ids is None:
            response = Response('用户不存在')
            return response
        idl = ids.split(',')
    if (req_m(request) == 0):
        ids = request.args.get("id", type=str, default=None)
        if ids is None:
            response = Response('用户不存在')
            return response
        idl = ids.split(',')
    try:
        for id in idl:
            user = Users.query.filter_by(id=id).first()
            if (user.role.name != "Super"):
                db.session.delete(user)
            db.session.commit()
    except:
        response = Response('删除失败')
        return response
    response = Response('删除成功')
    return response
#####################################################################################################################################################


@users.route('/list', methods=["GET"])
@login_required
def list():
    '''
    用户列表展示
    '''
    page = request.args.get('page', 1, type=int)
    if ('gid' in request.args.keys()):
        userList = Users.query.order_by(Users.id).\
                filter(Users.group_id == request.args.get("gid", default=0)).\
                paginate(page,
                         per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
                         error_out=True)
    if ('sid' in request.args.keys()):
        userList = Users.query.order_by(Users.id).\
                filter(Users.section_id == request.args.get("sid", default=0)).\
                paginate(page,
                         per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
                         error_out=True)
    if ('tid' in request.args.keys()):
        userList = Users.query.order_by(Users.id).\
                filter(Users.team_id == request.args.get("tid", default=0)).\
                paginate(page,
                         per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
                         error_out=True)
    else:
        if current_user.role_id == 3:
            userList = Users.query.order_by(Users.id).paginate(page,
                                                               per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
                                                               error_out=True)
        if current_user.role_id == 2:
            userList = Users.query.\
                order_by(Users.id).\
                filter(Users.role_id <= current_user.role_id).\
                paginate(page,
                         per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
                         error_out=True)
    return render_template("suser/user_list.html", userList=userList)
#####################################################################################################################################################


@users.route('/user_edit', methods=["GET", "POST"])
@login_required
def user_edit():
    '''
    编辑用户信息
    '''
    user = Users.query.filter_by(id=request.args.get('id', type=int, default=0)).first()
    roles = Role.query.all()
    groups = UserGroups.query.all()
    if (req_m(request) == 1):
        for k, v in request.form.items():
            if v != "":
                if k == 'reset_password':
                    getattr(user, k)(v)
                setattr(user, k, v)
        user.updata_user = current_user.username
        test_print(user.team_id)
        db.session.add(user)
        db.session.commit()
        return redirect(request.args.get("next") or url_for('users.list'))
    return render_template("suser/user_edit.html", user=user, roles=roles, groups=groups)
#####################################################################################################################################################


@users.route('/user_detail', methods=["GET"])
@login_required
def user_detail():
    '''
    列表中的用户信息展示
    '''
    if (req_m(request) == 0):
        user_info = Users.query.filter_by(id=request.args.get("id", type=int, default=0)).first()
        return render_template("suser/user_detail.html", user_info=user_info)
#####################################################################################################################################################


@users.route('/update', methods=["GET", "POST"])
@login_required
def update():
    '''
    修改用户密码
    '''
    error = ''
    msg = ''
    if (req_m(request) == 1):
        try:
            for k, v in request.form.items():
                if v != '':
                    if k == 'username':
                        setattr(current_user, 'uuid', create_uuid(v))
                    if k == 'reset_password':
                        getattr(current_user, k)(v)
                    setattr(current_user, k, v)
            db.session.add(current_user)
            db.session.commit()
        except:
            error = '修改失败'
        else:
            msg = "修改成功"
        finally:
            return render_template("suser/change_info.html", error=error, msg=msg)
    return render_template("suser/change_info.html", error=error, msg=msg)
#####################################################################################################################################################
#                                                                                                                                                   #
#                                                                                                                                                   #
#                                                   '''Group views'''                                                                               #
#                                                                                                                                                   #
#                                                                                                                                                   #
#####################################################################################################################################################


@users.route('/grouplist', methods=["GET"])
@login_required
def grouplist():
    '''
    用户组列表
    '''
    page = request.args.get('page', 1, type=int)
    group_all = UserGroups.query.order_by(UserGroups.id).paginate(page,
                                                                  per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
                                                                  error_out=True)
    return render_template("suser/usersgroup_list.html",
                           group_all=group_all,
                           page=page)


@users.route('/usergroupsadd', methods=["GET", "POST"])
@login_required
def usergroupsadd():
    '''
    添加用户组
    '''
    msg = None
    err = None
    if (req_m(request) == 1):
        usergroup = UserGroups()
        u = UserGroups.query.filter_by(name=request.form.get("name", default="")).first()
        if not u:
            for k, v in request.form.items():
                if v != '':
                    setattr(usergroup, k, v)
            db.session.add(usergroup)
            db.session.commit()
            msg = "{} 添加成功".format(request.form.get('name', type=str))
            err = None
        else:
            msg = None
            err = "{} 用户组存在!!!".format(request.form.get("name", type=str))
        return render_template("suser/group_add.html", msg=msg, error=err)
    return render_template("suser/group_add.html",  msg=msg, error=err)


@users.route('/groupdel', methods=["GET", "POST"])
@login_required
def groupdel():
    '''
    删除用户
    '''
    if (req_m(request) == 1):
        ids = request.form.get("id", type=str, default=None)
        if ids is None:
            response = Response('用户组不存在')
            return response
        idl = ids.split(',')
    if (req_m(request) == 0):
        ids = request.args.get("id", type=str, default=None)
        if ids is None:
            response = Response('用户组不存在')
            return response
        idl = ids.split(',')
    try:
        for id in idl:
            group = UserGroups.query.filter_by(id=id).first()
            db.session.delete(group)
            db.session.commit()
    except:
        response = Response('删除失败')
        return response
    response = Response('删除成功')
    return response
#####################################################################################################################################################


@users.route('/sectionlist', methods=["GET"])
@login_required
def sectionlist():
    '''
    部门列表
    '''
    page = request.args.get('page', 1, type=int)
    section_all = Sections.query.order_by(Sections.id).paginate(page,
                                                                per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
                                                                error_out=True)
    return render_template("suser/sections.html",
                           section_all=section_all,
                           page=page)


@users.route('/sectionadd', methods=["GET", "POST"])
@login_required
def sectionadd():
    '''
    添加部门
    '''
    msg = None
    err = None
    if (req_m(request) == 1):
        sec = Sections()
        s = Sections.query.filter_by(name=request.form.get("name", default="")).first()
        if not s:
            for k, v in request.form.items():
                if v != '':
                    setattr(sec, k, v)
            db.session.add(sec)
            db.session.commit()
            msg = "{} 添加成功".format(request.form.get('name', type=str))
            err = None
        else:
            msg = None
            err = "{} 部门存在!!!".format(request.form.get("name", type=str))
        return render_template("suser/group_add.html", msg=msg, error=err)
    return render_template("suser/group_add.html",  msg=msg, error=err)


@users.route('/section_edit', methods=["GET", "POST"])
@login_required
def section_edit():
    '''
    编辑项目信息
    '''
    sec = Sections.query.filter_by(id=request.args.get("id", default=0)).first()
    test_print(request.args)
    if (req_m(request) == 1):
        test_print(request.form)
        for k, v in request.form.items():
            if v != '':
                setattr(sec, k, v)
        db.session.add(sec)
        db.session.commit()
        return redirect(request.args.get("next") or url_for('users.sectionlist'))
    return render_template("suser/sections_edit.html", sec=sec)
#####################################################################################################################################################


@users.route('/teamslist', methods=["GET"])
@login_required
def teamslist():
    '''
    项目列表
    '''
    page = request.args.get('page', 1, type=int)
    if ('tid' in request.args.keys()):
        teams_all = Teams.query.order_by(Teams.id).\
            filter(Teams.sections_id == request.args.get("tid", default=0)).\
            paginate(page,
                     per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
                     error_out=True)
    else:
        teams_all = Teams.query.order_by(Teams.id).paginate(page,
                                                            per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
                                                            error_out=True)
    return render_template("suser/teams.html",
                           teams_all=teams_all,
                           page=page)


@users.route('/teamsadd', methods=["GET", "POST"])
@login_required
def teamsadd():
    '''
    添加项目
    '''
    flage = True
    team = Teams()
    sec_all = Sections.query.all()
    msg = None
    err = None
    if (req_m(request) == 1):
        t = Teams.query.filter_by(name=request.form.get("name", default="")).first()
        if not t:
            for k, v in request.form.items():
                if v != '':
                    setattr(team, k, v)
            db.session.add(team)
            db.session.commit()
            msg = "{} 项目添加成功".format(request.form.get('name', type=str))
            err = None
        else:
            msg = None
            err = "{} 项目存在!!!".format(request.form.get("name", type=str))
        return render_template("suser/group_add.html", flage=flage, sec_all=sec_all, msg=msg, error=err)
    return render_template("suser/group_add.html",  msg=msg, error=err, flage=flage, sec_all=sec_all)


@users.route('/team_edit', methods=["GET", "POST"])
@login_required
def team_edit():
    '''
    编辑项目信息
    '''
    team = Teams.query.filter_by(id=request.args.get("id", default=0)).first()
    section_all = Sections.query.all()
    test_print(request.args)
    if (req_m(request) == 1):
        for k, v in request.form.items():
            if v != '':
                setattr(team, k, v)
        db.session.add(team)
        db.session.commit()
        return redirect(request.args.get("next") or url_for('users.teamslist'))
    return render_template("suser/team_edit.html", team=team, section_all=section_all)


@users.route('/teamdel', methods=["GET", "POST"])
@login_required
def teamdel():
    '''
    删除项目
    '''
    if (req_m(request) == 1):
        ids = request.form.get("id", type=str, default=None)
        if ids is None:
            response = Response('项目不存在')
            return response
        idl = ids.split(',')
    if (req_m(request) == 0):
        ids = request.args.get("id", type=str, default=None)
        if ids is None:
            response = Response('项目不存在')
            return response
        idl = ids.split(',')
    try:
        for id in idl:
            team = Teams.query.filter_by(id=id).first()
            user = Users.query.filter_by(team_id=team.id).first()
            if user is not None:
                user.team_id = None
                db.session.add(user)
            db.session.delete(team)
            db.session.commit()
    except:
        response = Response('删除失败')
        return response
    response = Response('删除成功')
    return response
