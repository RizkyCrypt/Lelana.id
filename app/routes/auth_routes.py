from flask import Blueprint, render_template

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    """
    Rute untuk halaman login pengguna.
    """
    return "<h1>Halaman Login</h1><p>Blueprint auth berfungsi.</p>"

@auth.route('/register')
def register():
    """
    Rute untuk halaman registrasi pengguna.
    """
    return "<h1>Halaman Registrasi</h1>"