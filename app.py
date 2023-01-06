from flask import Flask
from config import Configuration
from posts.posts import posts

from models import db, Posts, Product, User, Role

from flask_migrate import Migrate

from flask_admin import Admin
from flask_admin import AdminIndexView
from flask_admin.contrib.sqla import ModelView

from flask_security import SQLAlchemyUserDatastore, Security, current_user


from flask import render_template, redirect, url_for, request, Response
from werkzeug.utils import secure_filename


app = Flask(__name__)

app.config.from_object(Configuration)

app.register_blueprint(posts, name="blue_posts", url_prefix='/blog')  # имя надо поменять!!!

db.init_app(app)
migrate = Migrate(app, db)


# --------admin-----------
# перенсти в новый модуль
class AdminMixin:
    def is_accessible(self):
        return current_user.has_role('admin')

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('security.login', next=request.url))


class BaseModelView(ModelView):
    def on_model_change(self, form, model, is_created):
        model.generate_slu()
        return super(BaseModelView, self).on_model_change(form, model, is_created)


class AdminView(AdminMixin, ModelView):
    pass


class HomeAdminView(AdminMixin, AdminIndexView):
    pass


class PostAdminView(AdminMixin, BaseModelView):
    form_columns = ['title', 'body', 'tags']


class TagAdminView(AdminMixin, BaseModelView):
    form_columns = ['name', 'posts']


admin = Admin(app)
admin.add_view(ModelView(Product, db.session))
admin.add_view(ModelView(Posts, db.session))


user_datastore = SQLAlchemyUserDatastore(db, User, Role)
app.security = Security(app, user_datastore)


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


# @app.route('info-users')
# def info-users()


@app.route("/profile")
# @app.route("/profile/<int:id>")
def profile(id):
    pass


@app.route('/test_views')
def test_views():
    pass
