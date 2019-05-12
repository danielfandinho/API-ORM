""" se comienza importando OS que se encargara de interactuar conla variable que declaremos con la ruta de la
base de datos en el comando  """
import os

""" se prosigue a darle a conocer a flas que es lo que vamos a hacer importando sus formulario
render_template: el cual utilizamos para redireccionar al usario al lugar donde quiere ir (aqui se manda el html y
las variables que interactuan con el en python
)  """
from flask import Flask, render_template, request
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
""" declarar a la variable para que cuando ejecutemos flask la reconozca, es un inicializador practicamente   """
app = Flask(__name__)
""" conexion a la base de datos por medio de la variable DATABASE_URL en comando utilizando BASH  """
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

"""cada @app.route es para que flas sepa en que parte del programa  esta por asi decirlo, un ejemplo sencillo es
que cada url se separa por /, si algo le sigue entonces es como una extencion de esa url, bueno es algo asi lo que
se ase con @app.route  """
@app.route("/")
def index():
    """ en la linea 24 con el fetchall es traer todos los datos que estan en esa consulta   """
    flights = db.execute("SELECT * FROM flights").fetchall()
    """  redireccionar y mandar la variable que necesita la pagina  """
    return render_template("index.html", flights=flights)

""" los metodos son por haber importado el request de flask
con este metodo se trabaja las peticiones y respuestas del usuario
para mas informacion entrar aqui
https://www.josedomingo.org/pledin/2018/03/flask-trabajando-con-peticiones-y-respuestas-3a-parte/
o ver el archivo de texto que deje con todos los links de referencia """
@app.route("/book", methods=["POST"])
def book():

    # Get form information.
    name = request.form.get("name")
    try:
        """ equest.form.get, obtiene el valor de flight_id par asignarla a la variable
        mas informacion aqui
        https://stackoverflow.com/questions/13279399/how-to-obtain-values-of-request-variables-using-python-and-flask"""
        flight_id = int(request.form.get("flight_id"))
    except ValueError:
        return render_template("error.html", message="Invalid flight number.")

    # Make sure flight exists.
    if db.execute("SELECT * FROM flights WHERE id = :id", {"id": flight_id}).rowcount == 0:
        return render_template("error.html", message="No such flight with that id.")
    db.execute("INSERT INTO passengers (name, flight_id) VALUES (:name, :flight_id)",
            {"name": name, "flight_id": flight_id})
    db.commit()
    return render_template("success.html")


@app.route("/flights")
def flights():

    flights = db.execute("SELECT * FROM flights").fetchall()
    return render_template("flights.html", flights=flights)


@app.route("/flights/<int:flight_id>")
def flight(flight_id):


    # Make sure flight exists.
    """el fetchone solo trae el primer valor de la consulta  """
    flight = db.execute("SELECT * FROM flights WHERE id = :id", {"id": flight_id}).fetchone()
    if flight is None:
        return render_template("error.html", message="No such flight.")

    # Get all passengers.
    passengers = db.execute("SELECT name FROM passengers WHERE flight_id = :flight_id",
                            {"flight_id": flight_id}).fetchall()
    return render_template("flight.html", flight=flight, passengers=passengers)
