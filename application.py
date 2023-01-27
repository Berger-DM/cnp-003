from canopus_flask import application, db, admin_manager
from flask_admin.contrib.sqla import ModelView
from canopus_flask.models import User, Carousel

# Setup for admin management - Adding views for users and carousels
admin_manager.add_view(ModelView(User, db.session))
admin_manager.add_view(ModelView(Carousel, db.session))

if __name__ == '__main__':
    application.debug = True
    application.run(host="0.0.0.0")
