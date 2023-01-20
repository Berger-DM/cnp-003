from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, PasswordField, SubmitField, FieldList, FormField, BooleanField
from wtforms.validators import Length, DataRequired, Email


class SignUpForm(FlaskForm):
    username = StringField(label='Username', validators=[DataRequired(), Length(min=6, max=20)])
    email = StringField(label='Email', validators=[DataRequired(), Email()])
    password = PasswordField(label='Password', validators=[DataRequired(), Length(min=8, max=20)])
    submit = SubmitField(label='Sign Up')


class LoginForm(FlaskForm):
    username = StringField(label='Username', validators=[DataRequired(), Length(min=6, max=20)])
    password = PasswordField(label='Password', validators=[DataRequired(), Length(min=8, max=20)])
    submit = SubmitField(label='Login')


class CreateCarouselForm(FlaskForm):
    carousel_name = StringField(label='Carousel Name', validators=[DataRequired(), Length(min=3, max=20)])
    first_carousel_image = FileField(label='First Image',
                                     validators=[FileRequired(), FileAllowed(('jpg', 'png'), message="Images Only!")])
    first_image_caption = StringField(label='Caption:')
    submit_carousel = SubmitField(label='Create Carousel')


class ImageEntryForm(FlaskForm):
    image = StringField()
    delete = BooleanField(label='Delete?')


class EditCarouselForm(FlaskForm):
    images = FieldList(FormField(ImageEntryForm), min_entries=1)
    submit = SubmitField(label="Finalize Edits")


class AddImageForm(FlaskForm):
    image = FileField(label='Update Image', validators=[FileRequired(), FileAllowed('jpg', 'png')])
    caption = StringField(label="Caption:")
    submit = SubmitField(label='Upload Image')
