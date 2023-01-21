import view

from app import app
from models import db

from posts.posts import posts
from registration.registration import registration
from product.product import product

app.register_blueprint(posts, name="blue_posts", url_prefix='/blog')  # имя изменено
app.register_blueprint(registration, url_prefix='/auth')
app.register_blueprint(product, name='p', url_prefix='/product')

if __name__ == "__main__":
    app.run()
