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
    posts = Posts.query.order_by(Posts.date.desc())

    page = request.args.get('page')
    if page and page.isdigit():
        page = int(page)
    else:
        page = 1
    pages = posts.paginate(page=page, per_page=7)

    return render_template('posts/index.html', posts=posts, pages=pages)


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


@posts.route('/<slug>')
def post_detail(slug):
    post = Posts.query.filter(Posts.slug == slug).first()
    return render_template('posts/post_detail.html', post=post)


@posts.route('/<slug>/edit', methods=['POST', 'GET'])
def edit_post(slug):
    post = Posts.query.filter(Posts.slug == slug).first()
    if request.method == 'POST':
        form = PostForm(formdata=request.form, obj=post)
        form.populate_obj(post)
        db.session.commit()

        return redirect(url_for('posts.post_detail', slug=post.slug))
    form = PostForm(obj=post)
    return render_template('posts/edit_post.html', post=post, form=form)

