from flask import render_template, url_for, redirect, flash, request
from canopus_flask import application as app, db
from flask_login import login_user, logout_user, current_user, login_required
from canopus_flask.forms import SignUpForm, LoginForm, CreateCarouselForm, AddImageForm
from canopus_flask.models import User, Image, Carousel
from canopus_flask.utilities import encrypt_password, check_password, save_image, ImageCombo, CarouselCombo


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
        user = User(username=form.username.data, email=form.email.data, password=encrypt_password(form.password.data),
                    is_admin=False)
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
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password(user.password, form.password.data):
            login_user(user)
            flash(f"{form.username.data} logged successfully", category='success')
            carousel_count = len(Carousel.query.filter_by(user_id=user.id).all())
            if carousel_count:
                return redirect(url_for('account'))
            else:
                return redirect(url_for('create'))
        else:
            flash(f"Login failed for {form.username.data}. Please try again.", category='danger')
    return render_template('login.html', title='Login', form=form)


# Logout
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('homepage'))


# Account Page and main User Carousel Display
@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    current_user_name = current_user.username
    carousels = Carousel.query.filter_by(user_id=current_user.id).order_by(Carousel.id).all()
    list_of_carousels = list()
    # Populate list of carousels - collect from query, crate Image Objects, form list
    for carousel in carousels:
        images = Image.query.filter_by(carousel_id=carousel.id).order_by(Image.id).all()
        images = [ImageCombo(image.raw_image_name, image.id, image.image_caption) for image in images]
        carousel_obj = CarouselCombo(carousel.carousel_name, carousel.id, images)
        list_of_carousels.append(carousel_obj)
    # Display the first carousel by ID by default, redirect to create if there are no carousels
    if not list_of_carousels:
        return redirect(url_for('create'))
    carousel_shown = list_of_carousels[0]
    if request.method == "POST":
        selected_carousel = request.form.get("selected_carousel")
        if request.form.get("create") == "create":
            return redirect(url_for('create'))
        else:
            # If a specific carousel is clicked on the account page, it becomes carousel_shown
            for carousel in list_of_carousels:
                carousel_id = carousel.carousel_id
                carousel_name = carousel.carousel_name
                # Selects and displays a new carousel_shown
                if selected_carousel == carousel_name:
                    carousel_shown = carousel
                    break
                elif request.form.get("edit") == carousel_name:
                    return redirect(url_for('edit', carousel_to_edit=carousel_id))
                elif request.form.get("delete") == carousel_name:
                    # Delete Images tied to carousel on Image table of DB
                    Image.query.filter_by(carousel_id=carousel_id).delete()
                    # Delete the carousel row itself from DB
                    Carousel.query.filter_by(id=carousel_id).delete()
                    db.session.commit()
                    flash(f"Carousel {carousel_name} was deleted.", category="danger")
                    return redirect(url_for('account'))
    return render_template('account.html', title='Account', username=current_user_name,
                           user_carousels=list_of_carousels, carousel_shown=carousel_shown)


# Edit Carousel
@app.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
    carousel_id = int(request.args.get('carousel_to_edit', None))
    carousel_data = Carousel.query.filter_by(id=carousel_id).first()
    images = Image.query.filter_by(carousel_id=carousel_id).order_by(Image.id).all()
    images = [ImageCombo(image.raw_image_name, image.id, image.image_caption) for image in images]
    carousel = CarouselCombo(carousel_name=carousel_data.carousel_name, carousel_id=int(carousel_id), img_list=images)
    img_count = len(images)
    form = AddImageForm()
    # Form is to add images to the Carousel
    if form.validate_on_submit():
        new_image = form.image.data
        new_image_name = save_image(new_image)
        image = Image(carousel_id=carousel_id, image_file=new_image.read(),
                      raw_image_name=new_image_name,
                      image_caption=form.caption.data)
        db.session.add(image)
        db.session.commit()
        flash(f"Image {new_image_name} was added to Carousel {carousel.carousel_name}!", category='success')
        return redirect(url_for('edit', carousel_to_edit=carousel_id))
    # Going straight to POST is for deleting images from the carousel
    if request.method == "POST":
        if request.form.get("delete") == "delete":
            image_del_id = request.args.get("img_to_delete", None)
            if image_del_id is not None:
                if img_count < 2:
                    flash(f"Carousel must have at least 1 image!", category='danger')
                else:
                    image = Image.query.filter_by(id=int(image_del_id), carousel_id=carousel_id)
                    image_name = image.first().raw_image_name
                    image.delete()
                    db.session.commit()
                    flash(f"Image {image_name} was removed from Carousel {carousel.carousel_name}!", category="error")
                return redirect(url_for('edit', carousel_to_edit=carousel_id))
    return render_template('edit_carousel.html', title='Edit Carousel', carousel=carousel, form=form,
                           carousel_to_edit=carousel_id, carousel_img_count=img_count)


# Create Carousel
@app.route('/create_carousel', methods=['GET', 'POST'])
@login_required
def create():
    form = CreateCarouselForm()
    if form.validate_on_submit():
        carousel = Carousel(carousel_name=form.carousel_name.data, user_id=current_user.id)
        db.session.add(carousel)
        db.session.commit()
        db.session.refresh(carousel)
        carousel_id = carousel.id
        first_image = form.first_carousel_image.data
        first_image_name = save_image(first_image)
        image = Image(carousel_id=carousel_id, image_file=first_image.read(),
                      raw_image_name=first_image_name,
                      image_caption=form.first_image_caption.data)
        db.session.add(image)
        db.session.commit()
        return redirect(url_for('edit', carousel_to_edit=carousel_id))
    return render_template('create_carousel.html', form=form)


# Admin Page
@app.route('/admin', methods=['POST'])
@login_required
def admin():
    if request.method == 'POST':
        if request.form.get("go_home") == "go_home":
            return redirect(url_for('homepage'))
    return render_template('admin/index.html')
