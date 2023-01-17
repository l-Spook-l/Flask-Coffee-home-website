from flask import Blueprint, redirect, url_for, render_template
from flask import request, render_template, redirect, url_for, flash
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
# from .forms import LoginForm, RegisterForm
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Role
from app import app


registration = Blueprint('registration', __name__, template_folder='templates', static_folder='static')

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(userid):
    return User.query.get(userid)


@registration.route('/login', methods=["POST", "GET"])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False

        user = User.query.filter_by(email=email).first()

        # check if the user actually exists
        # take the user-supplied password, hash it, and compare it to the hashed password in the database
        if not user or not check_password_hash(user.password, password):
            flash('Please check your login details and try again.')
            return redirect(
                url_for('registration.login'))  # if the user doesn't exist or password is wrong, reload the page

        # if the above check passes, then we know the user has the right credentials
        login_user(user, remember=remember)
        return redirect(url_for('registration.profile'))
    return render_template('registration/login.html')


@registration.route('/signup', methods=["POST", "GET"])
def signup():
    if request.method == 'POST':
        user = User.query.filter_by(email=request.form['email']).first()
        # Здесь надо проверить корректность данных но это тут не будем делать
        if user:  # if a user is found, we want to redirect back to signup page so user can try again
            print(user.name, user.email)
            flash('Email address already exists')
            return redirect(url_for('registration.signup'))
        try:
            # генерируем хеш пароля
            hash = generate_password_hash(request.form.get('password'))
            # Передаем данные
            email = request.form.get('email')
            name = request.form.get('name')
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
            flash('')
            return render_template('registration/register.html')

    return render_template('registration/register.html')


@registration.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы вышли из аккаута')
    return redirect(url_for('registration.login'))


@registration.route('/profile')
@login_required
def profile():
    print(current_user.name)
    print(current_user.email)
    print(current_user.id)
    print(current_user.roles[0].name)
    return render_template('registration/profile.html', name=current_user.name)
# =================================================================
# =================================================================
# =================================================================
# login_manager = LoginManager()
# login_manager.init_app(app)
#
#
# @login_manager.user_loader
# def load_user(user_id):
#     return User.get(user_id)
# # @login_manager.user_loader
# # def load_user(user_id):
# #     print('load_user')
# #     return UserLogin().fromDB(user_id)
#
#
# @registration.route('/register', methods=["POST", "GET"])
# def register():
#     if request.method == 'POST':
#         # Здесь надо проверить корректность данных но это тут не будем делать
#         try:
#             # генерируем хеш пароля
#             hash = generate_password_hash(request.form['password'])
#             # Передаем данные
#             email = request.form['email']
#             name = request.form['name']
#             u = User(name=name, email=email, password=hash)
#             db.session.add(u)  # добавляем запись в табл
#             db.session.flush()  # из сессии перемещает запись в таблицу
#             db.session.commit()  # сохраняем изменения табл
#             flash('Вы успешно зарегистрировались')
#             return redirect(url_for('registration.login'))
#         except:
#             flash('')
#             return render_template('registration/register.html')
#
#     return render_template('registration/register.html')
#
# # работает :)
# @registration.route('/logout')
# @login_required
# def logout():
#     logout_user()
#     flash('Вы вышли из аккаута')
#     return redirect(url_for('registration.login'))
#
#
# @registration.route('/login', methods=["POST", "GET"])
# def login():
#     if request.method == 'POST':
#         user = User.query.filter_by(email=request.form['email']).first()
#         if user and check_password_hash(user.password, request.form['password']):
#             # user_login = UserLogin().create(user)
#             # load_user(user_login)
#             load_user(user)
#             # flash('Logged in successfully.')
#             # return redirect(url_for('index'))
#             return redirect(url_for('registration.profile'))
#             # return redirect(next or url_for('index'))
#         flash("Неверный логин или пароль", "error")
#     return render_template('registration/login.html')
#
#

# =========================================================================================
# =========================================================================================
# =========================================================================================

# @login_manager.user_loader
# def load_user(user_id):
#     print('load user')
#     return User.get(user_id)
#
#
# @registration.route('/login', methods=["POST", "GET"])
# def login():
#     if current_user.is_authenticated:
#         return redirect(url_for('profile'))
#     form = LoginForm()
#     if form.validate_on_submit():
#         user = User.query.filter(User.email == form.email.data)
#         if user and check_password_hash(user.password, form.password.data):
#             remember_user = form.remember.data
#             login_user(user, remember=remember_user)
#             flash('Logged in successfully.')
#             # return redirect(url_for('index'))
#             return redirect(next or url_for('index'))
#         flash("Неверный логин или пароль", "error")
#     return render_template('registration/login.html', form=form)
#
#     # проверяем пришли ли данные
#     # if request.method == 'POST':
#     #     # Здесь надо проверить корректность данных но это тут не будем делать
#     #     try:
#     #         # генерируем хеш пароля
#     #         hash = generate_password_hash(request.form['password'])
#     #         # Передаем данные
#     #         u = User(email=request.form['email'], password=hash)
#     #         db.session.add(u)  # добавляем запись в табл
#     #         db.session.flush()  # из сессии перемещает запись в таблицу
#     #
#     #     except:
#     #         db.session.rollback()  # если что-то полшо не так, откатываем состояние табл.
#     #         print('Ошибка добавления в БД')
#     # return render_template("lesson_22_register.html", title="Регистрация")
#     # # при нажатие - авторизация, если уже авторизированны, переходим в свой профиль
#     # if current_user.is_authenticated:
#     #     return redirect(url_for('profile'))
#     # # создаем экземпляр класса
#     # form = LoginForm()
#     # # были ли отправлены данные - POST - запросом, и проверяет введенных корректность данных (в классе -forms)
#     # if form.validate_on_submit():
#     #     # обращаемся к БД и берем инфу по почте
#     #     # user = dbase.getUserByEmail(form.email.data)
#     #     user = User(email=request.form['email'], password=hash)
#     #     # если данные получены и пароль введен верно
#     #     if user and check_password_hash(user['password'], form.password.data):
#     #         # выполняем авторизацию пользователя
#     #         user_login = UserLogin().create(user)
#     #         # для запоминания пользователя
#     #         rm = form.remember.data
#     #         # авторизуем пользователя и запонимаем его
#     #         login_user(user_login, remember=rm)
#     #         # если  мы перешли на авторизацию с другой страницы, то после входа перейдем на неё иначе в профиль
#     #         return redirect(request.args.get("next") or url_for('profile'))
#     #     flash("Неверный логин или пароль", "error")
#     # form=form ссылка на экземпляр класса
#     # return render_template("login.html", menu=dbase.getMenu(), title="Авторизация", form=form)
#
#     # if request.method == "POST":
#     #     # обращаемся к БД и берем инфу по почте
#     #     user = dbase.getUserByEmail(request.form['email'])
#     #     # если данные получены и пароль введен верно
#     #     if user and check_password_hash(user['password'], request.form['password']):
#     #         user_login = UserLogin().create(user)
#     #         # для запоминания пользователя
#     #         rm = True if request.form.get('remainme') else False
#     #         # авторизуем пользователя и запонимаем его
#     #         login_user(user_login, remember=rm)
#     #         # если  мы перешли на авторизацию с другой страницы, то после входа перейдем на неё иначе в профиль
#     #         return redirect(request.args.get("next") or url_for('profile'))
#     #     flash("Неверный логин или пароль", "error")
#     # return render_template("login.html", menu=dbase.getMenu(), title="Авторизация")
#
#     # return render_template('registration/login.html')
#
#
# @registration.route('/register', methods=["POST", "GET"])
# def register():
#     #     # проверяем пришли ли данные
#     #     if request.method == 'POST':
#     #         # Здесь надо проверить корректность данных но это тут не будем делать
#     #         try:
#     #             # генерируем хеш пароля
#     #             hash = generate_password_hash(request.form['password'])
#     #             # Передаем данные
#     #             u = User(email=request.form['email'], password=hash)
#     #             db.session.add(u)  # добавляем запись в табл
#     #             db.session.flush()  # из сессии перемещает запись в таблицу
#     #
#     #             # добавление записи в табл - profiles (все имена такие же как и в классе выше
#     #             # p = Profiles(name=request.form['name'], old=request.form['old'],
#     #             #              city=request.form['city'], user_id=u.id)
#     #             # db.session.add(p)  # добавляем запись в табл
#     #             # db.session.commit()  # сохраняем изменения табл
#     #         except:
#     #             db.session.rollback()  # если что-то полшо не так, откатываем состояние табл.
#     #             print('Ошибка добавления в БД')
#     return render_template("registration/register.html")


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
