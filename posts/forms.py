from wtforms import Form, StringField, TextAreaField
# from flask_security import forms # тоже самое глянь


class PostForm(Form):
    title = StringField('Title')
    text = TextAreaField('Text')