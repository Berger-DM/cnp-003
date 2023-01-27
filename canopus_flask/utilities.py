import os
from canopus_flask import application as app, bcrypt


class ImageCombo:
    def __init__(self, img_name: str, img_id: int, img_cap: str):
        self.image_name = img_name
        self.image_id = img_id
        self.image_caption = img_cap


class CarouselCombo:
    def __init__(self, carousel_name: str, carousel_id: int, img_list: list()):
        self.carousel_name = carousel_name
        self.carousel_id = carousel_id
        self.image_list = img_list


def encrypt_password(password):
    return bcrypt.generate_password_hash(password.encode('utf-8')).decode('utf-8')


def check_password(db_pass, input_pass):
    return bcrypt.check_password_hash(db_pass, input_pass)


def save_image(image_to_save):
    image_name = image_to_save.filename
    image_path = os.path.join(app.root_path, 'static/images', image_name)
    if not os.path.exists(image_path):
        image_to_save.save(image_path)
    return image_name


def load_image(image_name):
    print(app.root_path)
    return os.path.join(app.root_path, 'static/images', image_name)
