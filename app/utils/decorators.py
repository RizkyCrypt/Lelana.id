from functools import wraps
from flask_login import current_user
from flask import abort

def admin_required(f):
    """
    Decorator untuk memastikan pengguna yang mengakses adalah admin.
    Jika bukan, kirim response 403 Forbidden.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            abort(403) # HTTP status code untuk Forbidden
        return f(*args, **kwargs)
    return decorated_function