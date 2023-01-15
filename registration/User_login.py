from flask_login import UserMixin
from models import User
from flask import url_for


# в __user - храниться вся информация
class UserLogin(UserMixin):
    # используеться при создании декоратора userloader
    def fromDB(self, user_id):
        self.__user = User.query.filter_by(id=user_id)
        return self

    # вызываем когда пользователь проходит авторизацию
    def create(self, user):
        self.__user = user
        return self

    def get_id(self):
        return str(self.__user['id'])

    def getName(self):
        return self.__user['name'] if self.__user else "Без имени"

    def getEmail(self):
        return self.__user['email'] if self.__user else "Без email"

    # def getAvatar(self, app):
    #     img = None
    #     # если для нашего пользователя нет аватара
    #     if not self.__user['avatar']:
    #         try:
    #             # то пытаемся загрузить дефолтную аватарку
    #             with app.open_resource(app.root_path + url_for('static', filename='images/default.png'), "rb") as f:
    #                 img = f.read()
    #         except FileNotFoundError as e:
    #             print(f"Не найден аватар по-умолчанию: {e}")
    #     else:
    #         # если у пользователя есть аватар грузим ее из БД
    #         img = self.__user['avatar']
    #     return img

    # def verifyExt(self, filename):
    #     # разделение файлы с конца по точке
    #     ext = filename.rsplit('.', 1)[1]
    #     if ext == "png" or ext == "PNG":
    #         return True
    #     return False

    # ==============================================================================

    # импортированный модуль заменяет эти строки они уже  реализованны в нем
    # def is_authenticated(self):
    #     return True
    #
    # def is_active(self):
    #     return True
    #
    # def is_anonymous(self):
    #     return False
