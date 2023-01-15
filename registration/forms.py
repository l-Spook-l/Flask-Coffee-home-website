from flask_wtf import FlaskForm

from wtforms import BooleanField  # для работы checkbox
from wtforms import PasswordField  # для работы с полем ввода пароля
from wtforms import StringField  # для работы с полем ввода
from wtforms import SubmitField  # для работы submit
from wtforms.validators import DataRequired  # требует чтобы в поле ввода был хотя бы 1 символ
from wtforms.validators import Email
from wtforms.validators import Length  # длинна
from wtforms.validators import EqualTo  # для проверки пароля


class LoginForm(FlaskForm):
    email = StringField("Email: ", validators=[Email("Некорректный email")])
    password = PasswordField("Пароль: ", validators=[DataRequired(), Length(min=4, max=100, message="Пароль должен быть от 4 до 100 символов")])
    remember = BooleanField("Запомнить", default=False)  # запомнить нас или нет
    submit = SubmitField("Войти")


class RegisterForm(FlaskForm):
    name = StringField("Имя: ", validators=[Length(min=4, max=100, message="Имя должно быть от 4 до 100 символов")])
    email = StringField("Email: ", validators=[Email("Некорректрый email")])
    password = PasswordField("Пароль: ", validators=[DataRequired(),
                                                     Length(min=4, max=10, message="Пароль должен быть от 4 до 100 символов")])
    password_2 = PasswordField("Повтор пароля: ", validators=[DataRequired(), EqualTo("password", message="Пароли не совподают")])

    submit = SubmitField("Регистрация")
