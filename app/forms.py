from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, DateField, IntegerField, FloatField, widgets, MultipleFileField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, NumberRange, Optional
from .models.user import User
from wtforms_sqlalchemy.fields import QuerySelectMultipleField
from .models.wisata import Wisata

class RegistrationForm(FlaskForm):
    """
    Formulir untuk registrasi pengguna baru.
    """
    username = StringField('Username', 
                           validators=[DataRequired(message='Username wajib diisi.'), 
                                       Length(min=4, max=25, message='Username harus antara 4 dan 25 karakter.')])
    email = StringField('Email', 
                        validators=[DataRequired(message='Email wajib diisi.'), 
                                    Email(message='Format email tidak valid.')])
    password = PasswordField('Password', 
                             validators=[DataRequired(message='Password wajib diisi.'), 
                                         Length(min=6, message='Password minimal 6 karakter.')])
    confirm_password = PasswordField('Konfirmasi Password', 
                                     validators=[DataRequired(message='Konfirmasi password wajib diisi.'), 
                                                 EqualTo('password', message='Password tidak cocok.')])
    submit = SubmitField('Daftar')

    def validate_username(self, username):
        """Memvalidasi apakah username sudah ada di database."""
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username tersebut sudah digunakan. Silakan pilih yang lain.')
    
    def validate_email(self, email):
        """Memvalidasi apakah email sudah ada di database."""
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email tersebut sudah terdaftar. Silakan gunakan email lain.')

class LoginForm(FlaskForm):
    """
    Formulir untuk login pengguna.
    """
    email = StringField('Email', 
                        validators=[DataRequired(message='Email wajib diisi.'), 
                                    Email(message='Format email tidak valid.')])
    password = PasswordField('Password', 
                             validators=[DataRequired(message='Password wajib diisi.')])
    remember = BooleanField('Ingat Saya')
    submit = SubmitField('Login')

class WisataForm(FlaskForm):
    """
    Formulir untuk menambah atau mengedit data wisata.
    """
    nama = StringField('Nama Wisata', 
                       validators=[DataRequired(message='Nama wisata wajib diisi.')])
    kategori = StringField('Kategori', 
                           validators=[DataRequired(message='Kategori wajib diisi.')])
    lokasi = StringField('Lokasi (Alamat/Koordinat)', 
                         validators=[DataRequired(message='Lokasi wajib diisi.')])
    deskripsi = TextAreaField('Deskripsi', 
                              validators=[DataRequired(message='Deskripsi wajib diisi.')])
    gambar_url = StringField('URL Gambar (Opsional)')

    latitude = FloatField('Latitude (Contoh: -7.421... Opsional)',
                          validators=[Optional()])
    longitude = FloatField('Longitude (Contoh: 109.243 Opsional)',
                           validators=[Optional()])

    submit = SubmitField('Simpan')

class EventForm(FlaskForm):
    """
    Formulir untuk menambah atau mengedit data event.
    """
    nama = StringField('Nama Event', 
                       validators=[DataRequired(message='Nama event wajib diisi.')])
    tanggal = DateField('Tanggal Pelaksanaan', format='%Y-%m-%d', 
                        validators=[DataRequired(message='Tanggal wajib diisi.')])
    lokasi = StringField('Lokasi Event', 
                         validators=[DataRequired(message='Lokasi wajib diisi.')])
    deskripsi = TextAreaField('Deskripsi', 
                              validators=[DataRequired(message='Deskripsi wajib diisi.')])
    penyelenggara = StringField('Penyelenggara (Opsional)')
    submit = SubmitField('Simpan Event')

class ReviewForm(FlaskForm):
    """
    Formulir untuk mengirimkan review, kini dengan fungsionalitas unggah foto.
    """
    rating = IntegerField('Rating (1-5)', 
                          validators=[DataRequired(), NumberRange(min=1, max=5, message='Rating harus antara 1 dan 5.')])
    komentar = TextAreaField('Komentar Anda', 
                             validators=[DataRequired(message='Komentar tidak boleh kosong.')])
    foto = MultipleFileField('Unggah Foto (Opsional)', 
                             validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Hanya gambar (jpg, png, jpeg) yang diizinkan!')])
    submit = SubmitField('Kirim Review')

def get_all_wisata():
    """Fungsi helper untuk query semua data wisata, diurutkan berdasarkan nama."""
    return Wisata.query.order_by(Wisata.nama).all()

class PaketWisataForm(FlaskForm):
    """
    Formulir untuk menambah atau mengedit Paket Wisata.
    """
    nama = StringField('Nama Paket Wisata', 
                       validators=[DataRequired(message='Nama paket wajib diisi.')])
    deskripsi = TextAreaField('Deskripsi Paket', 
                              validators=[DataRequired(message='Deskripsi paket wajib diisi.')])
    harga = IntegerField('Harga (Rp)', 
                         validators=[DataRequired(message='Harga wajib diisi.')])

    destinasi = QuerySelectMultipleField(
        'Pilih Destinasi yang Termasuk dalam Paket',
        query_factory=get_all_wisata,
        get_label='nama',
        widget=widgets.ListWidget(prefix_label=False),
        option_widget=widgets.CheckboxInput()
    )
    submit = SubmitField('Simpan Paket Wisata')

class ItinerariForm(FlaskForm):
    """
    Formulir untuk membuat atau mengedit Itinerari Petualangan.
    """
    judul = StringField('Judul Itinerari', 
                        validators=[DataRequired(message='Judul wajib diisi.')])
    deskripsi = TextAreaField('Cerita atau Deskripsi Singkat (Opsional)')

    wisata_termasuk = QuerySelectMultipleField(
        'Pilih Tempat Wisata untuk Dimasukkan',
        query_factory=get_all_wisata,
        get_label='nama',
        widget=widgets.ListWidget(prefix_label=False),
        option_widget=widgets.CheckboxInput()
    )
    submit = SubmitField('Simpan Itinerari')