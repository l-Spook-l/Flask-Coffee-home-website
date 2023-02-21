from flask import Blueprint
from flask import render_template, request, redirect, url_for
from models import db, Posts
from flask_login import login_required
from .forms import PostForm


posts = Blueprint('blue_posts', __name__, template_folder='templates', static_folder='static')


@posts.route('/')
def index():
    posts = Posts.query.order_by(Posts.date.desc())

    page = request.args.get('page')
    if page and page.isdigit():
        page = int(page)
    else:
        page = 1
    pages = posts.paginate(page=page, per_page=5)

    return render_template('posts/index.html', posts=posts, pages=pages)


@posts.route('/create', methods=['POST', 'GET'])
@login_required
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
        return redirect(url_for('blue_posts.index'))

    form = PostForm()
    return render_template('posts/create_post.html', form=form)


@posts.route('/<slug>')
def post_detail(slug):
    post = Posts.query.filter(Posts.slug == slug).first_or_404()
    return render_template('posts/post_detail.html', post=post)


@posts.route('/<slug>/edit', methods=['POST', 'GET'])
@login_required
def edit_post(slug):
    post = Posts.query.filter(Posts.slug == slug).first_or_404()
    if request.method == 'POST':
        form = PostForm(formdata=request.form, obj=post)
        form.populate_obj(post)
        db.session.commit()

        return redirect(url_for('blue_posts.post_detail', slug=post.slug))
    form = PostForm(obj=post)
    return render_template('posts/edit_post.html', post=post, form=form)


@posts.route('/<slug>/delete ')
@login_required
def delete_post(slug):
    post_delete = Posts.query.filter(Posts.slug == slug).first_or_404()
    try:
        db.session.delete(post_delete)
        db.session.commit()
        return redirect(url_for('blue_posts.index'))
    except:
        return "Error database"
