from app import db
from datetime import datetime

class Review(db.Model):
    """
    Model Database untuk review dan rating dari pengguna terhadap destinasi wisata.
    """
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False) # Rating dari 1 sampai 5
    komentar = db.Column(db.Text, nullable=False)
    tanggal_dibuat = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    # Foreign Key untuk relasi ke tabel User
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # Foreign key untuk relasi ke tabel Wisata
    wisata_id = db.Column(db.Integer, db.ForeignKey('wisata.id'), nullable=False)

    def __repr__(self):
        return f'<Review {self.id} oleh User {self.user_id}>'