from db import db
from datetime import datetime
from re import sub


def slugify(title):
    pattern = r'[^\w+]'
    return sub(pattern, '-', title)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    text = db.Column(db.Text, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    count = db.Column(db.Integer, nullable=False)

    image = db.Column(db.LargeBinary, nullable=False)
    name_image = db.Column(db.String(100), nullable=False)
    mimetype = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"<Product {self.id}>"


# class Images(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     image = db.Column(db.LargeBinary, nullable=False)
#     name_image = db.Column(db.String(100), nullable=False)
#     mimetype = db.Column(db.Text, nullable=False)
#
#     def __repr__(self):
#         return '<Product %r>' % self.id


class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=True)
    slug = db.Column(db.String(150), unique=True)
    text = db.Column(db.Text)
    date = db.Column(db.DateTime, default=datetime.now())

    def __init__(self, *args, **kwargs):
        super(Posts, self).__init__(*args, **kwargs)
        self.slug = self.generate_slug()

    def generate_slug(self):
        if self.title:
            self.slug = slugify(self.title)
            return self.slug

    def __repr__(self):
        return f"<Posts {self.id}>"


# class Users(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.String(50), unique=True)
#     password = db.Column(db.String(500), nullable=True)
#     date = db.Column(db.DateTime, default=datetime.utcnow())
#
#     data_profile = db.relationship('Profiles', backref='users', uselist=False)
#
#     def __repr__(self):
#         return f"<Users {self.id}>"
#
#
# class Profiles(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(50), nullable=True)
#     old = db.Column(db.Integer)
#     city = db.Column(db.String(100))
#
#     user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
#
#     def __repr__(self):
#         return f"<Profiles   {self.id}>"
