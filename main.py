from app import app
from models import db

from posts.posts import posts
from registration.registration import registration
app.register_blueprint(posts, name="blue_posts", url_prefix='/blog')  # имя изменено
app.register_blueprint(registration, url_prefix='/auth')


import view


if __name__ == "__main__":
    app.run()
