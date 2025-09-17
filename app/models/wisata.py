from app import db
from datetime import datetime

class Wisata(db.Model):
    """
    Model Database untuk destinasi wisata.
    """
    __tablename__ = 'wisata'

    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(100), nullable=False, index=True)
    kategori = db.Column(db.String(50), nullable=False)
    lokasi = db.Column(db.String(200), nullable=False)
    deskripsi = db.Column(db.Text, nullable=False)
    gambar_url = db.Column(db.String(255), nullable=True)
    tanggal_dibuat = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Wisata {self.nama}>'