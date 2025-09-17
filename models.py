from db import db
from flask_login import UserMixin

class Usuario(UserMixin, db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(30), nullable=False)
    senha = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)