from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(UserMixin, db.Model):
    """
    Model User untuk menyimpan data pengguna di database.
    """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(10), default='user', nullable=False) # Bisa 'user' atau 'admin'

    # Relasi ke Review: Satu user bisa punya banyak review
    reviews = db.relationship('Review', backref='author', lazy='dynamic')

    # Relasi ke Itinerari: Satu user bisa membuat banyak itinerari
    itinerari = db.relationship('Itinerari', backref='penulis', lazy='dynamic')

    @property
    def password(self):
        """
        Mencegah password diakses secara langsung (read-only).
        """
        raise AttributeError('Password bukan atribut yang bisa dibaca')
    
    @password.setter
    def password(self, password):
        """
        Mengatur password dengan mengubahnya menjadi hash.
        """
        self.password_hash = generate_password_hash(password)
    
    def verify_password(self, password):
        """
        Memeriksa apakah password yang dimasukkan cocok dengan hash di database.
        """
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        """
        Representasi string dari objek User untuk kemudahan debugging.
        """
        return f'<User {self.username}>'