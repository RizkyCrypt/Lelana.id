from app import db
from datetime import datetime

class Event(db.Model):
    """
    Model Database untuk event atau acara lokal.
    """
    __tablename__ = 'event'

    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(150), nullable=False, index=True)
    tanggal = db.Column(db.DateTime, nullable=False)
    lokasi = db.Column(db.String(200), nullable=False)
    deskripsi = db.Column(db.Text, nullable=False)
    penyelenggara = db.Column(db.String(100))
    tanggal_dibuat = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Event {self.nama}>'