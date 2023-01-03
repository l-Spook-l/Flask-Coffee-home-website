from flask import Blueprint
from flask import render_template, request, redirect, url_for
from db import db


from models import Product, Posts
from .forms import PostForm

posts = Blueprint('posts', __name__, template_folder='templates', static_folder='static')

# отображение товаров, перенеси
# @posts.route('/')
# def index():
#     product = Product.query.all()
#     return render_template('posts/index.html', product=product)


@posts.route('/')
def index():
    posts = Posts.query.order_by(Posts.date)
    return render_template('posts/index.html', posts=posts)


@posts.route('/create', methods=['POST', 'GET'])
def create_post():
    if request.method == 'POST':
        title = request.form['title']
        text = request.form['text']
        try:
            post = Posts(title=title, text=text)
            db.session.add(post)
            db.session.commit()
        except:
            print("Что-то пошло не так")
        return redirect(url_for('posts.index'))

    form = PostForm()
    return render_template('posts/create_post.html', form=form)
