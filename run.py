import os
from app import create_app, db
from app.models.user import User
from flask_migrate import Migrate

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)

@app.shell_context_processor
def make_shell_context():
    """
    Membuat variabel tambahan tersedia di dalam konteks shell Flask.
    Ini memudahkan pengujian dan interaksi dengan komponen aplikasi
    melalui command line.
    """
    return dict(db=db, User=User)