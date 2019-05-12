from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class vuelos(db.Model):
    __tablename__ = "vuelos"
    id = db.Column(db.Integer, primary_key=True)
    origen = db.Column(db.String, nullable=False)
    destino = db.Column(db.String, nullable=False)
    duracion = db.Column(db.Integer, nullable=False)


class Pasajeros(db.Model):
    __tablename__ = "pasageros"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String, nullable=False)
    id_vuelos = db.Column(db.Integer, db.ForeignKey("vuelos.id"), nullable=False)
