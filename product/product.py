from flask import Blueprint, request, redirect, render_template, url_for
from flask_login import login_required
from uuid import uuid4
from os import path, remove
from models import db, Product
from .forms import ProductForm


product = Blueprint('p', __name__, template_folder='templates', static_folder='static')


@product.route("/add-product", methods=["POST", "GET"])
@login_required
def add_product():
    if request.method == "POST":
        title = request.form['title']
        image = request.files['image']
        text = request.form['text']
        price = request.form['price']
        count = request.form['count']
        file_name = f'{uuid4()}.jpg'  # уникальное имя файла
        image.save(path.join('static/images', file_name))  # для сохранения в папке

        try:
            product = Product(title=title, text=text, price=price, count=count, name_image=file_name)
            db.session.add(product)
            db.session.flush()
            db.session.commit()
            return redirect(url_for("profile"))
        except:
            db.session.rollback()
            print("Ошибка добавления в БД")
    form = ProductForm()
    return render_template("product/add-product.html", form=form)


@product.route('/<title>/edit', methods=['POST', 'GET'])
@login_required
def edit_product(title):
    product_edit = Product.query.filter(Product.title == title).first_or_404()
    if request.method == 'POST':
        form = ProductForm(formdata=request.form, obj=product_edit)
        form.populate_obj(product_edit)
        db.session.commit()
        return redirect(url_for('profile'))
    form = ProductForm(obj=product_edit)
    return render_template('product/edit_product.html', product=product_edit, form=form)


@product.route('/<title>/delete ')
@login_required
def delete_product(title):
    product_delete = Product.query.filter(Product.title == title).first_or_404()
    try:
        remove(f'static/images/{product_delete.name_image}')
        db.session.delete(product_delete)
        db.session.commit()
        return redirect(url_for('profile'))
    except:
        return "Error database"
