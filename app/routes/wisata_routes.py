from flask import Blueprint, render_template, redirect, url_for, flash, abort, request, jsonify
from flask_login import login_required, current_user
from app import db
from app.models.wisata import Wisata
from app.models.review import Review
from app.models.foto_ulasan import FotoUlasan
from app.forms import WisataForm, ReviewForm
from app.utils.decorators import admin_required
from app.services.file_handler import save_pictures

wisata = Blueprint('wisata', __name__)

@wisata.route('/wisata')
def list_wisata():
    """
    Rute untuk menampilkan daftar semua destinasi wisata dengan paginasi.
    """
    page = request.args.get('page', 1, type=int)

    pagination = Wisata.query.order_by(Wisata.nama).paginate(
        page=page, per_page=5, error_out=False
    )
    daftar_wisata_halaman_ini = pagination.items

    return render_template('wisata/list.html', 
                            daftar_wisata=daftar_wisata_halaman_ini,
                            pagination=pagination)

@wisata.route('/wisata/detail/<int:id>', methods=['GET', 'POST'])
def detail_wisata(id):
    """
    Rute untuk menampilkan detail wisata, daftar review, dan form untuk menambah review.
    """
    w = Wisata.query.get_or_404(id) # Mengambi data wisata berdasarkan ID, jika tidak ada akan menampilkan error 404
    form = ReviewForm()

    if form.validate_on_submit() and current_user.is_authenticated:
        review_baru = Review(
            rating=form.rating.data,
            komentar=form.komentar.data,
            author=current_user,
            wisata_reviewed=w
        )
        db.session.add(review_baru)

        if form.foto.data:
            if form.foto.data[0].filename:
                try:
                    filenames = save_pictures(form.foto.data)
                    for filename in filenames:
                        foto_baru = FotoUlasan(nama_file=filename, review=review_baru)
                        db.session.add(foto_baru)
                except Exception as e:
                    flash(f'Terjadi kesalahan saat mengunggah gambar: {e}', 'danger')
                    db.session.rollback()
                    return redirect(url_for('wisata.detail_wisata', id=w.id))

        db.session.commit()
        flash('Terima kasih! Review Anda telah ditambahkan.', 'success')
        return redirect(url_for('wisata.detail_wisata', id=w.id))
    
    semua_review = w.reviews.order_by(Review.tanggal_dibuat.desc()).all()

    return render_template('wisata/detail.html', wisata=w, reviews=semua_review, form=form)

@wisata.route('/wisata/tambah', methods=['GET', 'POST'])
@login_required
@admin_required
def tambah_wisata():
    """
    Rute untuk menambah destinasi wisata baru.
    Hanya bisa diakses oleh admin.
    """
    form = WisataForm()
    if form.validate_on_submit():
        wisata_baru = Wisata(
            nama=form.nama.data,
            kategori=form.kategori.data,
            lokasi=form.lokasi.data,
            deskripsi=form.deskripsi.data,
            gambar_url=form.gambar_url.data,
            latitude=form.latitude.data,
            longitude=form.longitude.data
        )
        db.session.add(wisata_baru)
        db.session.commit()

        flash('Destinasi wisata baru berhasil ditambahkan!', 'success')
        return redirect(url_for('wisata.list_wisata'))
    
    return render_template('wisata/tambah_edit.html', form=form, judul_halaman='Tambah Wisata')

@wisata.route('/wisata/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_wisata(id):
    """
    Rute untuk mengedit destinasi wisata yang sudah ada.
    """
    wisata_item = Wisata.query.get_or_404(id)
    form = WisataForm(obj=wisata_item)

    if form.validate_on_submit():
        wisata_item.nama = form.nama.data
        wisata_item.kategori = form.kategori.data
        wisata_item.lokasi = form.lokasi.data
        wisata_item.deskripsi = form.deskripsi.data
        wisata_item.gambar_url = form.gambar_url.data
        wisata_item.latitude = form.latitude.data
        wisata_item.longitude = form.longitude.data
        db.session.commit()

        flash('Data wisata berhasil diperbarui!', 'success')
        return redirect(url_for('wisata.detail_wisata', id=wisata_item.id))
    
    return render_template('wisata/tambah_edit.html', form=form, judul_halaman='Edit Wisata')

@wisata.route('/wisata/hapus/<int:id>', methods=['POST'])
@login_required
@admin_required
def hapus_wisata(id):
    """
    Rute untuk menghapus destinasi wisata.
    Hanya menerima metode POST untuk keamanan.
    """
    wisata_item = Wisata.query.get_or_404(id)
    db.session.delete(wisata_item)
    db.session.commit()

    flash('Data wisata telah berhasil dihapus.', 'info')
    return redirect(url_for('wisata.list_wisata'))

@wisata.route('/api/wisata/lokasi')
def api_lokasi_wisata():
    """
    API endpoint untuk menyediakan data lokasi semua wisata dalam format JSON.
    """
    semua_wisata = Wisata.query.filter(Wisata.latitude.isnot(None), Wisata.longitude.isnot(None)).all()

    daftar_lokasi = []
    for w in semua_wisata:
        daftar_lokasi.append({
            'nama': w.nama,
            'lat': w.latitude,
            'lon': w.longitude,
            'detail_url': url_for('wisata.detail_wisata', id=w.id, _external=True)
        })
        return jsonify(daftar_lokasi)