from api.app import db
from flask_login import UserMixin


# Table database model
class Table(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    seats = db.Column(db.Integer)
    orders = db.relationship('Order')


# Orders database model
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    table = db.Column(db.Integer, db.ForeignKey('table.id'))
    items = db.Column(db.PickleType)
    total = db.Column(db.Numeric(precision=5, scale=2))


# Category database model
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256))
    items = db.relationship('Item')


# Items database model
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    icon = db.Column(db.Unicode(2, collation='utf8mb4_bin'))
    name = db.Column(db.String(256))
    category = db.Column(db.Integer, db.ForeignKey('category.id'))
    price = db.Column(db.Numeric(precision=5, scale=2))
    orders = db.Column(db.Integer)


# User database model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256))
    admin = db.Column(db.Boolean)
    email = db.Column(db.String(256), unique=True)
    password = db.Column(db.String(256))
