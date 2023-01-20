import os
from canopus_flask import app, bcrypt
from PySide2.QtGui import QPixmap


def encrypt_password(password):
    return bcrypt.generate_password_hash(password.encode('utf-8')).decode('utf-8')


def check_password(db_pass, input_pass):
    return bcrypt.check_password_hash(db_pass, input_pass)


def save_image(image_to_save):
    image_name = image_to_save.filename
    image_path = os.path.join(app.root_path, 'static/images', image_name)
    image_to_save.save(image_path)
    return image_name


def convert_image(image, image_name):
    print("Print at the start of convert_image")
    pixmap = QPixmap()
    extension = image_name.split(".")[-1]
    print(extension)
    pixmap.loadFromData(image, extension)
    print("Print before return of convert_image")
    return pixmap
