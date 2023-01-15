from flask_wtf import FlaskForm

from wtforms import StringField, TextAreaField


class PostForm(FlaskForm):
    title = StringField('Title')
    text = TextAreaField('Text')
