from flask import Flask
from config import Configuration
# from posts.posts import posts
# from registration.registration import registration
from flask_login import current_user
from models import db, Posts, Product, User, Role
from flask_migrate import Migrate

from flask_admin import Admin
from flask_admin import AdminIndexView
from flask_admin.contrib.sqla import ModelView

# from flask_security import SQLAlchemyUserDatastore, Security

from flask import render_template, redirect, url_for, request, Response
from werkzeug.utils import secure_filename

app = Flask(__name__)

app.config.from_object(Configuration)

# app.register_blueprint(posts, name="blue_posts", url_prefix='/blog')  # имя изменено
# app.register_blueprint(registration, url_prefix='/auth')

db.init_app(app)
migrate = Migrate(app, db)

# user_datastore = SQLAlchemyUserDatastore(db, User, Role)
# security = Security(app, user_datastore)


# ============================================
# -------------------admin--------------------
# ============================================

# перенести в новый модуль
class AdminMixin:
    def is_accessible(self):
        if current_user.is_authenticated:
            print(current_user.id, ' - id текущего пользователя')
            # print(Role.query.filter_by(name='admin').first().id, ' - id нужной роли')
            return current_user.roles[0].name == 'admin'

    def inaccessible_callback(self, name, **kwargs):
        # return redirect(url_for('security.login', next=request.url))  # для переадрисации
        return redirect(url_for('index'))
        # return redirect(url_for('page_not_found'))


class BaseModelView(ModelView):
    def on_model_change(self, form, model, is_created):
        model.generate_slu()
        return super(BaseModelView, self).on_model_change(form, model, is_created)


class AdminView(AdminMixin, ModelView):
    pass


class HomeAdminView(AdminMixin, AdminIndexView):
    pass


class PostAdminView(AdminMixin, BaseModelView):
    form_columns = ['title', 'text']


admin = Admin(app, 'Shop', url='/', index_view=HomeAdminView())
admin.add_view(AdminView(Product, db.session))
admin.add_view(PostAdminView(Posts, db.session))
admin.add_view(AdminView(User, db.session))
admin.add_view(AdminView(Role, db.session))

# ===========================================================
@app.route("/add-product", methods=["POST", "GET"])
def add_product():
    if request.method == "POST":
        title = request.form['title']
        image = request.files['image']
        text = request.form['description']
        price = request.form['price']
        count = request.form['count']

        file_name = secure_filename(image.filename)
        mimetype = image.mimetype

        try:
            product = Product(title=title, image=image.read(), text=text, price=price, count=count,
                              mimetype=mimetype,
                              name_image=file_name)

            db.session.add(product)
            db.session.flush()
            db.session.commit()
            return redirect("/")
        except:
            db.session.rollback()
            print("Ошибка добавления в БД")
    return render_template("add-product.html")


@app.route('/show_image/<int:id>')
def show_image(id):
    file_data = Product.query.filter_by(id=id).first()
    return Response(file_data.image, mimetype=file_data.mimetype)


# 2й вариант отображения картинки
# @app.route('/image/<int:id>')
# def image(id):
#     file_data = Product.query.filter_by(id=id).first()
#     h = make_response(file_data.image)
#     h.headers["Content-Type"] = 'image/png'
#     return h


@app.route("/profile")
# @app.route("/profile/<int:id>")
def profile(id):
    pass


@app.route('/test_views')
def test_views():
    pass
