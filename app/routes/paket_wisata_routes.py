from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required
from app import db
from app.models.paket_wisata import PaketWisata
from app.forms import PaketWisataForm
from app.utils.decorators import admin_required

paket_wisata = Blueprint('paket_wisata', __name__)

@paket_wisata.route('/paket-wisata')
def list_paket():
    """
    Rute untuk menampilkan daftar semua paket wisata.
    """
    semua_paket = PaketWisata.query.order_by(PaketWisata.nama).all()

    return render_template('paket_wisata/list.html', daftar_paket=semua_paket)

@paket_wisata.route('/paket-wisata/detail/<int:id>')
def detail_paket(id):
    """
    Rute untuk menampilkan detail dari satu paket wisata spesifik.
    """
    paket = PaketWisata.query.get_or_404(id)

    return render_template('paket_wisata/detail.html', paket=paket)

@paket_wisata.route('/paket-wisata/tambah', methods=['GET', 'POST'])
@login_required
@admin_required
def tambah_paket():
    """
    Rute untuk menambah data paket wisata baru.
    Hanya dapat diakses oleh pengguna dengan peran 'admin'.
    """
    form = PaketWisataForm()
    if form.validate_on_submit():
        paket_baru = PaketWisata(
            nama=form.nama.data,
            deskripsi=form.deskripsi.data,
            harga=form.harga.data,
            destinasi=form.destinasi.data
        )

        db.session.add(paket_baru)
        db.session.commit()

        flash('Paket wisata baru berhasil ditambahkan!', 'success')
        return redirect(url_for('paket_wisata.list_paket'))
    
    return render_template('paket_wisata/tambah_edit.html', form=form, judul_halaman='Tambah Paket Wisata')

@paket_wisata.route('/paket-wisata/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_paket(id):
    """
    Rute untuk mengubah data paket wisata yang sudah ada.
    Hanya dapat diakses oleh pengguna dengan peran 'admin'.
    """
    paket = PaketWisata.query.get_or_404(id)
    form = PaketWisataForm(obj=paket)
    if form.validate_on_submit():
        paket.nama = form.nama.data
        paket.deskripsi = form.deskripsi.data
        paket.harga = form.harga.data
        paket.destinasi = form.destinasi.data
        db.session.commit()

        flash('Paket wisata berhasil diperbarui!', 'success')
        return redirect(url_for('paket_wisata.detail_paket', id=paket.id))
    
    return render_template('paket_wisata/tambah_edit.html', form=form, judul_halaman='Edit Paket Wisata')

@paket_wisata.route('/paket-wisata/hapus/<int:id>', methods=['POST'])
@login_required
@admin_required
def hapus_paket(id):
    """
    Rute untuk menghapus data paket wisata dari database.
    Hanya menerima metode POST untuk keamanan.
    """
    paket = PaketWisata.query.get_or_404(id)
    db.session.delete(paket)
    db.session.commit()

    flash('Paket wisata telah berhasil dihapus.', 'info')
    return redirect(url_for('paket_wisata.list_paket'))