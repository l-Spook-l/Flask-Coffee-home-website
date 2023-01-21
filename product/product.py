from flask import Blueprint, request, redirect, render_template, url_for
from flask_login import login_required
from uuid import uuid4
from os import path
from models import db, Product


product = Blueprint('p', __name__, template_folder='templates', static_folder='static')


@product.route("/add-product", methods=["POST", "GET"])
@login_required
def add_product():
    if request.method == "POST":
        title = request.form['title']
        image = request.files['image']
        text = request.form['description']
        price = request.form['price']
        count = request.form['count']

        file_name = f'{uuid4()}.jpg'  # уникальное имя файла
        # file_name = secure_filename(image.filename)  #  для сохранения в бд
        image.save(path.join('static/images', file_name))  # для сохранения в папке
        # mimetype = image.mimetype

        try:
            product = Product(title=title, text=text, price=price, count=count, name_image=file_name)
            # product = Product(title=title, image=image.read(), text=text, price=price, count=count,
            #                   mimetype=mimetype,
            #                   name_image=file_name)
            db.session.add(product)
            db.session.flush()
            db.session.commit()
            return redirect(url_for("profile"))
        except:
            db.session.rollback()
            print("Ошибка добавления в БД")
    return render_template("product/add-product.html")
