from flask import render_template, url_for, redirect, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from canopus_flask.forms import SignUpForm, LoginForm, CreateCarouselForm
from canopus_flask import app, db
from canopus_flask.models import User, Image, Carousel
from canopus_flask.utilities import convert_image, encrypt_password, check_password


# Icon for tab in browser
@app.route('/favicon.ico')
def favicon():
    return url_for('static', filename='favicon.ico')


# Home Page and default Carousel Display
@app.route('/')
@app.route('/home', methods=['GET', 'POST'])
def homepage():
    return render_template('home.html', title='Home')


# Signup Page and Operation
@app.route('/signup', methods=['POST', 'GET'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, password=encrypt_password(form.password.data))
        db.session.add(user)
        db.session.commit()
        flash(f"Account successfully created for {form.username.data}", category='success')
        return redirect(url_for('login'))
    return render_template('signup.html', title='Signup', form=form)


# Login Page and Operation
@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user_login = User.query.filter_by(username=form.username.data).first()
        if user_login and check_password(user_login.password, form.password.data):
            login_user(user_login)
            flash(f"{form.username.data} logged successfully", category='success')
            return redirect(url_for('account'))
        else:
            flash(f"Login failed for {form.username.data}. Please try again.", category='danger')
    return render_template('login.html', title='Login', form=form)


# Logout
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('homepage'))


# Account Page
@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    current_user_name = current_user.username
    carousels = Carousel.query.filter_by(user_id=current_user.id).order_by(Carousel.id).all()
    print(current_user_name, carousels)
    dict_of_carousels = dict()
    if request.method == "POST":
        print("Method is POST")
        if request.form.get("edit") == "edit":
            return redirect(url_for('edit'))
        elif request.form.get("delete") == "delete":
            print("Delete Requested")
            return redirect(url_for('account'))
        elif request.form.get("create") == "create":
            print("Create New Carousel Selected")
            return redirect(url_for('create'))
    if request.method == "GET":
        print("Entered GET")
        for carousel in carousels:
            images = Image.query.filter_by(carousel_id=carousel.id).order_by(Image.id).all()
            print("Got thru query")
            images = [convert_image(image.image_file, image.raw_image_name) for image in images]
            print("Got through conversion")
            dict_of_carousels[carousel.carousel_name] = images
            print(dict_of_carousels[carousel.carousel_name])
    return render_template('account.html', title='Account', username=current_user_name,
                           user_carousels=dict_of_carousels)


# Edit Carousel
@app.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
    return render_template('edit_carousel.html')


# Create Carousel
@app.route('/create_carousel', methods=['GET', 'POST'])
@login_required
def create():
    form = CreateCarouselForm()
    print(form.validate_on_submit())
    if form.validate_on_submit():
        carousel = Carousel(carousel_name=form.carousel_name.data, user_id=current_user.id)
        print(Carousel)
        db.session.add(carousel)
        db.session.commit()
        db.session.refresh(carousel)
        carousel_id = carousel.id
        first_image = form.first_carousel_image.data.read()
        image = Image(carousel_id=carousel_id, image_file=first_image,
                      raw_image_name=form.first_carousel_image.data.filename,
                      image_caption=form.first_image_caption.data)
        db.session.add(image)
        db.session.commit()

    return render_template('create_carousel.html', form=form)
