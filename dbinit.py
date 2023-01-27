# This file is onle used to initialize the database in a DB service. It needs to be run exactly once.

from canopus_flask import application as app, db

# Affirming the current context for Flask
app.app_context().push()

# For creating the Database
db.create_all()

# Final check
from canopus_flask.models import User, Carousel, Image
User.query.all()
Carousel.query.all()
Image.query.all()
