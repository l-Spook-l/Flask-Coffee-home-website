from flask_wtf import FlaskForm

from wtforms import StringField, TextAreaField, IntegerField, FileField, SubmitField


class ProductForm(FlaskForm):
    title = StringField('Title')
    image = FileField('Image')
    text = TextAreaField('Text')
    price = IntegerField('Price')
    count = IntegerField('Count')
