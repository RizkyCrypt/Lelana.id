from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import config

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'

def create_app(config_name):
    """
    Fungsi factory untuk aplikasi (Application Factory).
    - Membuat dan mengkonfigurasi aplikasi Flask.
    - Menginisialisasi ekstensi.
    - Mendaftarkan blueprint.
    """
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)
    login_manager.init_app(app)

    from . import models

    @login_manager.user_loader
    def load_user(user_id):
        from .models.user import User
        return User.query.get(int(user_id))

    from .routes.main_routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .routes.auth_routes import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from .routes.wisata_routes import wisata as wisata_blueprint
    app.register_blueprint(wisata_blueprint)

    from .routes.event_routes import event as event_blueprint
    app.register_blueprint(event_blueprint)

    return app