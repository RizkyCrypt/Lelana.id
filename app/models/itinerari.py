from app import db
from datetime import datetime

itinerari_wisata_association = db.Table('itinerari_wisata_association',
    db.Column('itinerari_id', db.Integer, db.ForeignKey('itinerari.id'), primary_key=True),
    db.Column('wisata_id', db.Integer, db.ForeignKey('wisata.id'), primary_key=True)
)

class Itinerari(db.Model):
    """
    Model Database untuk fitur Itinerari Petualangan yang dibuat oleh pengguna.
    """
    __tablename__ = 'itinerari'

    id = db.Column(db.Integer, primary_key=True)
    judul = db.Column(db.String(150), nullable=False)
    deskripsi = db.Column(db.Text, nullable=True)
    tanggal_dibuat = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    # Foreign Key untuk relasi ke tabel User
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    wisata_termasuk = db.relationship('Wisata', secondary=itinerari_wisata_association,
                                      lazy='subquery',
                                      backref=db.backref('termasuk_dalam_itinerari', lazy=True))

    def __repr__(self):
        return f'<Itinerari {self.judul}>'