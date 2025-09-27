from flask import Blueprint, render_template, abort, flash, redirect, url_for
from flask_login import login_required, current_user
from app.utils.decorators import admin_required
from app import db
from app.models.wisata import Wisata
from app.models.user import User
from app.models.event import Event
from app.models.paket_wisata import PaketWisata
from app.forms import AdminEditUserForm

admin = Blueprint('admin', __name__)

@admin.route('/admin/dashboard')
@login_required
@admin_required
def dashboard():
    """
    Halaman utama untuk dashboard admin.
    """
    return render_template('admin/dashboard.html')

@admin.route('/admin/users')
@login_required
@admin_required
def manage_users():
    """
    Menampilkan daftar semua pengguna untuk manajemen.
    """
    users = User.query.order_by(User.id).all()

    return render_template('admin/manage_users.html', users=users)

@admin.route('/admin/users/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_user(id):
    """ Mengedit data pengguna oleh admin. """
    user_to_edit = User.query.get_or_404(id)
    form = AdminEditUserForm(original_user=user_to_edit)

    if form.validate_on_submit():
        user_to_edit.username = form.username.data
        user_to_edit.email = form.email.data
        user_to_edit.role = form.role.data
        db.session.commit()

        flash(f'Data pengguna {user_to_edit.username} berhasil diperbarui.', 'success')
        return redirect(url_for('admin.manage_users'))
    
    form.username.data = user_to_edit.username
    form.email.data = user_to_edit.email
    form.role.data = user_to_edit.role

    return render_template('admin/edit_user.html', form=form, user=user_to_edit)

@admin.route('/admin/users/hapus/<int:id>', methods=['POST'])
@login_required
@admin_required
def hapus_user(id):
    """ Menghapus pengguna oleh admin. """
    user_to_delete = User.query.get_or_404(id)

    if user_to_delete.id == current_user.id:
        flash('Anda tidak dapat menghapus akun Anda sendiri.', 'danger')
        return redirect(url_for('admin.manage_users'))

    db.session.delete(user_to_delete)
    db.session.commit()

    flash(f'Pengguna {user_to_delete.username} telah berhasil dihapus.', 'info')
    return redirect(url_for('admin.manage_users'))

@admin.route('/admin/wisata')
@login_required
@admin_required
def manage_wisata():
    """ Menampilkan daftar semua data wisata untuk manajemen. """
    semua_wisata = Wisata.query.order_by(Wisata.nama).all()

    return render_template('admin/manage_wisata.html', daftar_wisata=semua_wisata)

@admin.route('/admin/event')
@login_required
@admin_required
def manage_event():
    """ Menampilkan daftar semua data event untuk manajemen. """
    semua_event = Event.query.order_by(Event.tanggal.desc()).all()

    return render_template('admin/manage_event.html', daftar_event=semua_event)

@admin.route('/admin/paket-wisata')
@login_required
@admin_required
def manage_paket_wisata():
    """ Menampilkan daftar semua data paket wisata untuk manajemen. """
    semua_paket = PaketWisata.query.order_by(PaketWisata.nama).all()
    
    return render_template('admin/manage_paket_wisata.html', daftar_paket=semua_paket)