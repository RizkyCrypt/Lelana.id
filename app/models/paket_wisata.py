from app import db
from datetime import datetime

# Association Table untuk relasi Many-to-Many antara PaketWisata dan Wisata
paket_wisata_association = db.Table('paket_wisata_association',
    db.Column('paket_id', db.Integer, db.ForeignKey('paket_wisata.id'), primary_key=True),
    db.Column('wisata_id', db.Integer, db.ForeignKey('wisata.id'), primary_key=True)
)

class PaketWisata(db.Model):
    """
    Model Database untuk paket wisata yang dibuat oleh admin.
    """
    __tablename__ = 'paket_wisata'

    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(150), nullable=False, index=True)
    deskripsi = db.Column(db.Text, nullable=False)
    harga = db.Column(db.Integer, nullable=False)
    tanggal_dibuat = db.Column(db.DateTime, default=datetime.utcnow)

    # Mendefinisikan relasi many-to-many ke model Wisata
    destinasi = db.relationship('Wisata', secondary=paket_wisata_association,
                                lazy='subquery',
                                backref=db.backref('paket_termasuk', lazy=True))

    def __repr__(self):
        return f'<PaketWisata {self.nama}>'