from flask import Flask
from config import Configuration
from posts.posts import posts
from db import db_init, db



from flask import render_template, redirect, url_for, request, Response, make_response
from werkzeug.utils import secure_filename
from models import Product
# from db import db_init, db

from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView


app = Flask(__name__)

app.config.from_object(Configuration)
app.register_blueprint(posts, url_prefix='/blog')

db_init(app)


# admin = Admin(app)
# admin.add_view(ModelView())


# @app.route("/")
# @app.route("/home")
# def index():
#     product = Product.query.order_by(Product.title).all()
#     return render_template("index.html", data=product)


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
