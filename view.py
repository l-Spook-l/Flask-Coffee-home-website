from flask import render_template
from models import Product
from app import app


@app.route("/")
@app.route("/home")
def index():
    product = Product.query.order_by(Product.title).all()
    return render_template("index.html", data=product)