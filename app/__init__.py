from flask import Flask, render_template
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

    from .routes.paket_wisata_routes import paket_wisata as paket_wisata_blueprint
    app.register_blueprint(paket_wisata_blueprint)

    from .routes.itinerari_routes import itinerari as itinerari_blueprint
    app.register_blueprint(itinerari_blueprint)

    @app.errorhandler(404)
    def page_not_found(e):
        """Menangani error 404 (Halaman Tidak Ditemukan)."""
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        """Menangani error 500 (Kesalahan Internal Server)."""
        return render_template('errors/500.html'), 500

    return app