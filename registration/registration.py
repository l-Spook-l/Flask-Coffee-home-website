from flask import Blueprint
from flask import request, render_template, redirect, url_for, flash
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from .forms import LoginForm, RegisterForm
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Role, Product
from app import app
# ===============
from models import Product
from uuid import uuid4
from os import path
# ===============

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
        # check if the user actually exists
        # take the user-supplied password, hash it, and compare it to the hashed password in the database
        # if not user or not check_password_hash(user.password, password_form):
        if user and check_password_hash(user.password, password_form):
            login_user(user, remember=remember)
            # return redirect(request.args.get('next'), url_for('registration.profile'))  # перенаправление не работает
            return redirect(url_for('profile'))

        flash('Неверная пара логин/пароль')
        # if the user doesn't exist or password is wrong, reload the page
        # if the above check passes, then we know the user has the right credentials
    return render_template('registration/login.html', form=form)


@registration.route('/signup', methods=["POST", "GET"])
def signup():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        # Здесь надо проверить корректность данных но это тут не будем делать
        if user:  # if a user is found, we want to redirect back to signup page so user can try again
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
            flash('хм...')
            # return render_template('registration/register.html')

    return render_template('registration/register.html', form=form)


@registration.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы вышли из аккаута')
    return redirect(url_for('registration.login'))


# @app.route("/add-product", methods=["POST", "GET"])
# # @login_required
# def add_product():
#     if request.method == "POST":
#         title = request.form['title']
#         image = request.files['image']
#         text = request.form['description']
#         price = request.form['price']
#         count = request.form['count']
#
#         file_name = f'{uuid4()}.jpg'  # уникальное имя файла
#         # file_name = secure_filename(image.filename)  #  для сохранения в бд
#         image.save(path.join('static/images', file_name))  # для сохранения в папке
#         # mimetype = image.mimetype
#
#         try:
#             product = Product(title=title, text=text, price=price, count=count, name_image=file_name)
#             # product = Product(title=title, image=image.read(), text=text, price=price, count=count,
#             #                   mimetype=mimetype,
#             #                   name_image=file_name)
#             db.session.add(product)
#             db.session.flush()
#             db.session.commit()
#             return redirect("/")
#         except:
#             db.session.rollback()
#             print("Ошибка добавления в БД")
#     return render_template("add-product.html")
#

# ================================================================================
# ================================================================================
# ================================================================================


# ========= для security ============
# from app import app, user_datastore
# from flask import render_template
# from models import db, Role
# with app.app_context():
#     user_datastore.create_user(email="my7_email@me.com", password="password")
#     db.session.commit()
# with app.app_context():
#     user_datastore.create_role(name='admin', description='administrator')
#     db.session.commit()
# with app.app_context():
#     user = User.query.filter(User.email == 'uaspookua@gmail.com')
#     role = Role.query.filter(Role.name == 'admin')
#     user_datastore.add_role_to_user(user, role)
#     db.session.commit()


# ================================================================================
# ================================================================================
# ================================================================================
# создание роли
# with app.app_context():
#     name = 'user'
#     description = 'user'
#     role = Role(name=name, description=description)
#     db.session.add(role)  # добавляем запись в табл
#     db.session.flush()  # из сессии перемещает запись в таблицу
#     db.session.commit()  # сохраняем изменения табл
# ================================================================================
# ================================================================================
# ================================================================================
# with app.app_context():
#     user = User.query.filter_by(email='uaspookua@gmail.com').first()
#     role = Role.query.filter_by(name='admin').first()
#     # user = User()
#     # role = Role()
#     user.roles.append(role)
#     db.session.add(user)
#     db.session.commit()
