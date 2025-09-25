import uuid
import os
from werkzeug.utils import secure_filename
from flask import current_app

def save_pictures(form_pictures):
    """
    Fungsi service untuk menyimpan file gambar yang diunggah.

    Logika ini dipisahkan dari route untuk menjaga kebersihan kode dan
    memudahkan pengujian serta penggunaan kembali (reusability).

    Args:
        form_pictures (list): Daftar objek file dari form (misal: form.foto.data).

    Returns:
        list: Daftar nama file yang telah berhasil disimpan.
    """
    saved_filenames = []
    for picture in form_pictures:
        _, f_ext = os.path.splitext(picture.filename)
        picture_fn = str(uuid.uuid4()) + f_ext

        filename = secure_filename(picture_fn)

        picture_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)

        picture.save(picture_path)
        saved_filenames.append(filename)
    return saved_filenames