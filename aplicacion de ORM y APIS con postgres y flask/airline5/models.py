import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class vuelo(db.Model):
    __tablename__ = "vuelo"
    id = db.Column(db.Integer, primary_key=True)
    origen = db.Column(db.String, nullable=False)
    destino = db.Column(db.String, nullable=False)
    duracion = db.Column(db.Integer, nullable=False)
    pasajeros = db.relationship("pasajero", backref="vuelo", lazy=True)

    def add_pasajero(self, name):
        p = pasajero(name=name, vuelo_id=self.id)
        db.session.add(p)
        db.session.commit()


class Pasajero(db.Model):
    __tablename__ = "pasajero"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String, nullable=False)
    vuelos_id = db.Column(db.Integer, db.ForeignKey("vuelo.id"), nullable=False)

def main():
    db.create_all()

if __name__=="__main__":
    with app.app_context():
        main()
