from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Velo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.Integer)
    estPris = db.Column(db.Boolean)


class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_velo = db.Column(db.Integer, db.ForeignKey('velo.id'))
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'))
    date_debut = db.Column(db.DateTime(timezone=True), default=func.now())
    date_fin = db.Column(db.DateTime(timezone=True), default=func.now())


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(120))
    est_admin = db.Column(db.Boolean)
    password = db.Column(db.String(150))


class Historique(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'))
    id_velo = db.Column(db.Integer, db.ForeignKey('velo.id'))
    date_debut = db.Column(db.DateTime(timezone=True), default=func.now())
    date_fin = db.Column(db.DateTime(timezone=True), default=func.now())
