from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from app import db
from app.models.event import Event
from app.forms import EventForm
from app.utils.decorators import admin_required

event = Blueprint('event', __name__)

@event.route('/event')
def list_event():
    """
    Rute untuk menampilkan daftar semua event dengan paginasi.
    """
    page = request.args.get('page', 1, type=int)
    pagination = Event.query.order_by(Event.tanggal.desc()).paginate(
        page=page, per_page=5, error_out=False
    )
    daftar_event_halaman_ini = pagination.items

    return render_template('event/list.html', 
                            daftar_event=daftar_event_halaman_ini,
                            pagination=pagination)

@event.route('/event/detail/<int:id>')
def detail_event(id):
    """
    Rute untuk menampilkan detail dari satu event spesifik.
    """
    event_item = Event.query.get_or_404(id)

    return render_template('event/detail.html', event=event_item)

@event.route('/event/tambah', methods=['GET', 'POST'])
@login_required
@admin_required
def tambah_event():
    """
    Rute untuk menambah data event baru.
    Hanya dapat diakses oleh pengguna dengan peran 'admin'.
    """
    form = EventForm()
    if form.validate_on_submit():
        event_baru = Event(
            nama=form.nama.data,
            tanggal=form.tanggal.data,
            lokasi=form.lokasi.data,
            deskripsi=form.deskripsi.data,
            penyelenggara=form.penyelenggara.data
        )
        db.session.add(event_baru)
        db.session.commit()
            
        flash('Event baru berhasil ditambahkan!', 'success')
        return redirect(url_for('event.list_event'))
    
    return render_template('event/tambah_edit.html', form=form, judul_halaman='Tambah Event Baru')

@event.route('/event/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_event(id):
    """
    Rute untuk mengubah data event yang sudah ada.
    Hanya dapat diakses oleh pengguna dengan peran 'admin'.
    """
    event_item = Event.query.get_or_404(id)
    form = EventForm(obj=event_item)
    if form.validate_on_submit():
        event_item.nama = form.nama.data
        event_item.tanggal = form.tanggal.data
        event_item.lokasi = form.lokasi.data
        event_item.deskripsi = form.deskripsi.data
        event_item.penyelenggara = form.penyelenggara.data
        db.session.commit()

        flash('Data event berhasil diperbarui!', 'success')
        return redirect(url_for('event.detail_event', id=event_item.id))
    
    return render_template('event/tambah_edit.html', form=form, judul_halaman='Edit Event')

@event.route('/event/hapus/<int:id>', methods=['POST'])
@login_required
@admin_required
def hapus_event(id):
    """
    Rute untuk menghapus data event dari database.
    Hanya menerima metode POST untuk keamanan.
    """
    event_item = Event.query.get_or_404(id)
    db.session.delete(event_item)
    db.session.commit()

    flash('Event telah berhasil dihapus.', 'info')
    return redirect(url_for('event.list_event'))