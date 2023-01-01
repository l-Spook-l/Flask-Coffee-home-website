from flask import Flask, render_template, redirect, url_for, request, Response, make_response
from werkzeug.utils import secure_filename

from models import Product
from db import db_init, db

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
db_init(app)


@app.route("/")
@app.route("/home")
def index():
    product = Product.query.order_by(Product.title).all()
    return render_template("index.html", data=product)


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


if __name__ == "__main__":
    app.run(debug=True)
