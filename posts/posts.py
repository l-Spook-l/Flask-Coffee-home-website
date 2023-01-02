from flask import Blueprint
from flask import render_template

from models import Product

posts = Blueprint('posts', __name__, template_folder='templates', static_folder='static')


@posts.route('/')
def index():
    product = Product.query.all()
    return render_template('posts/index.html', product=product)
