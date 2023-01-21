from flask import render_template
from models import Product
from app import app
from flask_login import login_required, current_user


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


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
