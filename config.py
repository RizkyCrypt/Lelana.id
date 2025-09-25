import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config:
    """
    Kelas konfigurasi dasar. Berisi pengaturan default dan pengaturan
    yang berlaku untuk semua lingkungan (environment).
    """
    SECRET_KEY = os.environ.get('SECRET_KEY') or '$^peg=i8qm@*!-a2ew!l)kf@#ix@djujv**#-o%sqga!x%8hsj'

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'lelana.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    UPLOAD_FOLDER = os.path.join(basedir, 'app/static/uploads')
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

class DevelopmentConfig(Config):
    """
    Konfigurasi untuk lingkungan pengembangan (development).
    """
    DEBUG = True

class TestingConfig(Config):
    """
    Konfigurasi untuk lingkungan pengujian (testing).
    """
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'test_lelana.db')
    WTF_CSRF_ENABLED = False # Nonaktifkan CSRF saat menjalankan tes

class ProductionConfig(Config):
    """
    Konfigurasi untuk lingkungan produksi (production).
    """
    DEBUG = False
    TESTING = False

# Dictionary untuk mengakses kelas konfigurasi berdasarkan nama
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}