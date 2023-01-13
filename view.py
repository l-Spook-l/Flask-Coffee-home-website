from flask import render_template
from models import Product, User
from app import app


@app.route("/")
@app.route("/home")
def index():
    product = Product.query.order_by(Product.title).all()
    return render_template("index.html", data=product)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
