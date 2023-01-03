from flask import Blueprint
from flask import request, render_template

from werkzeug.security import generate_password_hash

from app import app
from db import db
from models import Users, Profiles


registration = Blueprint('registration', __name__, template_folder='templates', static_folder='static')


@app.route('/register', methods=["POST", "GET"])
def register():
    # проверяем пришли ли данные
    if request.method == 'POST':
        # Здесь надо проверить корректность данных но это тут не будем делать
        try:
            # генерируем хеш пароля
            hash = generate_password_hash(request.form['password'])
            # Передаем данные
            u = Users(email=request.form['email'], password=hash)
            db.session.add(u)  # добавляем запись в табл
            db.session.flush()  # из сессии перемещает запись в таблицу

            # добавление записи в табл - profiles (все имена такие же как и в классе выше
            p = Profiles(name=request.form['name'], old=request.form['old'],
                         city=request.form['city'], user_id=u.id)
            db.session.add(p)  # добавляем запись в табл
            db.session.commit()  # сохраняем изменения табл
        except:
            db.session.rollback()  # если что-то полшо не так, откатываем состояние табл.
            print('Ошибка добавления в БД')
    return render_template("lesson_22_register.html")
