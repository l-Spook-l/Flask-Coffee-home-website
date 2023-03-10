from flask import Blueprint
from flask import render_template, redirect, url_for, flash
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from .forms import LoginForm, RegisterForm
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Role
from app import app


registration = Blueprint('registration', __name__, template_folder='templates', static_folder='static')

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'registration.login'
login_manager.login_message = 'Авторизуйтесь для доступа'


@login_manager.user_loader
def load_user(userid):
    return User.query.get(userid)


@registration.route('/login', methods=["POST", "GET"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password_form = form.password.data
        remember = True if form.remember.data else False
        user = User.query.filter_by(email=email).first()
        # проверить, существует ли пользователь на самом деле
        # берем предоставленный пользователем пароль, хешируем его и сравниваем с хешированным паролем в базе данных
        if user and check_password_hash(user.password, password_form):
            login_user(user, remember=remember)
            return redirect(url_for('profile'))
        flash('Неверная пара логин/пароль')
        # если пользователь не существует или пароль неверный, перезагружаем страницу
    return render_template('registration/login.html', form=form)


@registration.route('/signup', methods=["POST", "GET"])
def signup():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        # Здесь надо проверить корректность данных, но это тут не будем делать
        if user:  # если user найден, то перенаправляем его на страницу входа
            print(user.name, user.email)
            flash('Эта почта уже зарегистрирована')
            return redirect(url_for('registration.signup'))
        try:
            # генерируем хеш пароля
            hash = generate_password_hash(form.password.data)
            # Передаем данные
            email = form.email.data
            name = form.name.data
            new_user = User(name=name, email=email, password=hash)
            db.session.add(new_user)  # добавляем запись в табл
            db.session.flush()  # из сессии перемещает запись в таблицу

            user_for_add_role = User.query.filter_by(email=email).first()
            role = Role.query.filter_by(name='user').first()
            user_for_add_role.roles.append(role)
            db.session.add(user_for_add_role)
            db.session.commit()  # сохраняем изменения табл
            flash('Вы успешно зарегистрировались')
            return redirect(url_for('registration.login'))
        except:
            flash('Ошибка БД')

    return render_template('registration/register.html', form=form)


@registration.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы вышли из аккаута')
    return redirect(url_for('registration.login'))
