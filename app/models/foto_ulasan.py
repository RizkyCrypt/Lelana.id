from app import db

class FotoUlasan(db.Model):
    """
    Model Database untuk menyimpan path file foto yang diunggah untuk setiap ulasan.
    """
    __tablename__ = 'foto_ulasan'

    id = db.Column(db.Integer, primary_key=True)
    nama_file = db.Column(db.String(100), nullable=False)

    review_id = db.Column(db.Integer, db.ForeignKey('reviews.id'), nullable=False)

    def __repr__(self):
        return f'<FotoUlasan {self.nama_file}>'