from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from .models.user import User

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