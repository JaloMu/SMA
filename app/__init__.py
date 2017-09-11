from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config
from flask_login import LoginManager
db = SQLAlchemy()

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)
    login_manager.init_app(app)

    # create main views
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # create auth views
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    # create users views
    from .users import users as users_blueprint
    app.register_blueprint(users_blueprint, url_prefix='/users')

    # create cmdb views
    from .cmdb import cmdb as cmdb_blueprint
    app.register_blueprint(cmdb_blueprint, url_prefix='/cmdb')

    # create cmdb views
    from .dns import dns as dns_blueprint
    app.register_blueprint(dns_blueprint, url_prefix='/dns')

    # create cmdb views
    from .saltstack import saltstack as saltstack_blueprint
    app.register_blueprint(saltstack_blueprint, url_prefix='/saltstack')

    # create cmdb views
    from .srpm import srpm as srpm_blueprint
    app.register_blueprint(srpm_blueprint, url_prefix='/srpm')

    return app
