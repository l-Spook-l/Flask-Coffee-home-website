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


# <!-- <img class="Card_image" src="{{url_for('show_image', id=el.id)}}" alt="" /> -->
# 1й вариант отображения картинки
# @app.route('/show_image/<int:id>')
# def show_image(id):
#     file_data = Product.query.filter_by(id=id).first()
#     return Response(file_data.image, mimetype=file_data.mimetype)


# 2й вариант отображения картинки
# @app.route('/image/<int:id>')
# def image(id):
#     file_data = Product.query.filter_by(id=id).first()
#     h = make_response(file_data.image)
#     h.headers["Content-Type"] = 'image/png'
#     return h
