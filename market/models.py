from market import db, login_manager
from market import bcrypt
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(30))
    email = db.Column(db.String(50))
    password_hash = db.Column(db.String(60))
    orcamento = db.Column(db.Float(), default=1000.0)
    items = db.relationship('Item', backref='owned_user', lazy=True)

    @property
    def orcamento_formatado(self):
        if len(str(self.orcamento)) >= 4:
            return f'{str(self.orcamento)[:-5]},{str(self.orcamento)[-5:]}$'
        else:
            return f"{self.orcamento}$"

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self, login_password):
        return bcrypt.check_password_hash(self.password_hash, login_password)

    def can_purchase(self, items_obj):
        return self.orcamento >= items_obj.price

    def can_sell(self, items_obj):
        return items_obj in self.items

    def __repr__(self):
        return f'Usuario: {self.username}'


class Item(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(30))
    price = db.Column(db.Integer())
    barcode = db.Column(db.String(12))
    description = db.Column(db.String(1024))
    owner = db.Column(db.Integer(), db.ForeignKey('user.id'))

    def __repr__(self):
        return f'Item: {self.name}'

    def comprar(self, user):
        self.owner = user.id
        user.orcamento -= self.price
        db.session.commit()

    def vender(self, user):
        self.owner = None
        user.orcamento += self.price
        db.session.commit()
