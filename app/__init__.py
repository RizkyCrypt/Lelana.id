from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import config

db = SQLAlchemy()

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

    from .routes.main_routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .routes.auth_routes import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    return app