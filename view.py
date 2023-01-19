from flask import render_template
from models import Product
from app import app


@app.route("/")
@app.route("/home")
def index():
    product = Product.query.order_by(Product.id).all()
    # print(product[1].title)
    # print(product[1].name_image)
    return render_template("index.html", data=product)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
