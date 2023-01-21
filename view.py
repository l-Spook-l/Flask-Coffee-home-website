from flask import render_template, request, redirect, url_for
from models import Product, db
from app import app
from flask_login import login_required, current_user
from uuid import uuid4
from os import path


@app.route("/")
@app.route("/home")
def index():
    product = Product.query.order_by(Product.id).all()
    return render_template("index.html", data=product)


@app.route('/profile')
@login_required
def profile():
    print(current_user.name)
    print(current_user.email)
    print(current_user.id)
    print(current_user.roles[0].name)
    product = Product.query.order_by(Product.id).all()
    return render_template('profile.html', name=current_user.name, email=current_user.email, data=product)


# @app.route("/add-product", methods=["POST", "GET"])
# @login_required
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
#             return redirect(url_for("profile"))
#         except:
#             db.session.rollback()
#             print("Ошибка добавления в БД")
#     return render_template("product/add-product.html")


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
