from flask import Blueprint, render_template
from flask_login import login_required, current_user

main = Blueprint('main', __name__)

@main.route('/')
def index():
    """
    Rute untuk halaman utama (landing page).
    """
    return render_template('main/index.html')

@main.route('/profile')
@login_required # Decorator ini akan melindungi halaman.
def profile():
    """
    Rute untuk halaman profil pengguna.
    Hanya bisa diakses jika pengguna sudah login.
    """
    return render_template('main/profile.html', user=current_user)

@main.route('/peta-wisata')
def peta_wisata():
    """
    Rute untuk menampilkan halaman peta interaktif.
    """
    return render_template('main/peta.html')