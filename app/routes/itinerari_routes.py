from flask import Blueprint, render_template, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from app import db
from app.models.itinerari import Itinerari
from app.forms import ItinerariForm
from app.utils.decorators import admin_required

itinerari = Blueprint('itinerari', __name__)

@itinerari.route('/itinerari')
def list_itinerari():
    """Menampilkan semua itinerari yang telah dibuat, dari yang terbaru."""
    semua_itinerari = Itinerari.query.order_by(Itinerari.tanggal_dibuat.desc()).all()

    return render_template('itinerari/list.html', daftar_itinerari=semua_itinerari)

@itinerari.route('/itinerari/detail/<int:id>')
def detail_itinerari(id):
    """Menampilkan halaman detail untuk satu itinerari."""
    it = Itinerari.query.get_or_404(id)

    return render_template('itinerari/detail.html', itinerari=it)

@itinerari.route('/itinerari/buat', methods=['GET', 'POST'])
@login_required
def buat_itinerari():
    """Halaman form untuk membuat itinerari baru."""
    form = ItinerariForm()
    if form.validate_on_submit():
        it_baru = Itinerari(
            judul=form.judul.data,
            deskripsi=form.deskripsi.data,
            penulis=current_user,
            wisata_termasuk=form.wisata_termasuk.data
        )

        db.session.add(it_baru)
        db.session.commit()

        flash('Itinerari Petualangan baru berhasil dibuat!', 'success')
        return redirect(url_for('itinerari.detail_itinerari', id=it_baru.id))
    
    return render_template('itinerari/buat_edit.html', form=form, judul_halaman='Buat Itinerari Baru')

@itinerari.route('/itinerari/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_itinerari(id):
    """Halaman form untuk mengedit itinerari yang sudah ada."""
    it = Itinerari.query.get_or_404(id)
    if it.penulis != current_user:
        abort(403)

    form = ItinerariForm(obj=it)
    if form.validate_on_submit():
        it.judul = form.judul.data
        it.deskripsi = form.deskripsi.data
        it.wisata_termasuk = form.wisata_termasuk.data
        db.session.commit()

        flash('Itinerari berhasil diperbarui!', 'success')
        return redirect(url_for('itinerari.detail_itinerari', id=it.id))
    
    return render_template('itinerari/buat_edit.html', form=form, judul_halaman='Edit Itinerari')

@itinerari.route('/itinerari/hapus/<int:id>', methods=['POST'])
@login_required
def hapus_itinerari(id):
    """Rute untuk menghapus itinerari."""
    it = Itinerari.query.get_or_404(id)
    if it.penulis != current_user:
        abort(403)

    db.session.delete(it)
    db.session.commit()

    flash('Itinerari telah berhasil dihapus.', 'info')
    return redirect(url_for('itinerari.list_itinerari'))