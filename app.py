from flask import Flask
from config import Configuration
from flask_login import current_user
from models import db, Posts, Product, User, Role
from flask_migrate import Migrate
from flask_admin import Admin
from flask_admin import AdminIndexView
from flask_admin.contrib.sqla import ModelView


from flask import redirect, url_for


app = Flask(__name__, static_url_path='/static')

app.config.from_object(Configuration)

db.init_app(app)
migrate = Migrate(app, db)


# ============================================
# -------------------admin--------------------
# ============================================

class AdminMixin:
    def is_accessible(self):
        if current_user.is_authenticated:
            print(current_user.id, ' - id текущего пользователя')
            # print(Role.query.filter_by(name='admin').first().id, ' - id нужной роли')
            return current_user.roles[0].name == 'admin'

    def inaccessible_callback(self, name, **kwargs):
        # return redirect(url_for('security.login', next=request.url))  # для переадрисации
        return redirect(url_for('index'))
        # return redirect(url_for('page_not_found'))


class BaseModelView(ModelView):
    def on_model_change(self, form, model, is_created):
        model.generate_slug()
        return super(BaseModelView, self).on_model_change(form, model, is_created)


class AdminView(AdminMixin, ModelView):
    pass


class HomeAdminView(AdminMixin, AdminIndexView):
    pass


class PostAdminView(AdminMixin, BaseModelView):
    form_columns = ['title', 'text']


admin = Admin(app, 'Shop', url='/', index_view=HomeAdminView())
admin.add_view(AdminView(Product, db.session))
admin.add_view(PostAdminView(Posts, db.session))
admin.add_view(AdminView(User, db.session))
admin.add_view(AdminView(Role, db.session))


