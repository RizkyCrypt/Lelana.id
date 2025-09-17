from flask import Blueprint, render_template

main = Blueprint('main', __name__)

@main.route('/')
def index():
    """
    Rute untuk halaman utama (landing page).
    """
    return "<h1>Halo, Lelana.id!</h1><p>Halaman utama berfungsi.</p>"