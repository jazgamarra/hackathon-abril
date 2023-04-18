
from time import time
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

from datetime import datetime, time, date


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///basededatos.db'
db = SQLAlchemy(app)

class Pabellon(db.Model):
    id_pabellon = db.Column (db.Integer, primary_key=True)
    nombre_pabellon = db.Column(db.String(10), nullable=False)

class Guardia(db.Model):
    id_guardia = db.Column (db.Integer, primary_key=True)
    nombre_guardia = db.Column (db.String (50), nullable=False)
    # id_espacio_asignado = db.Column (db.Integer, db.ForeignKey('espacioasignado.id_espacio_asignado'))

class Espacios(db.Model):
    id_espacio = db.Column (db.Integer, primary_key=True)
    nombre_espacio = db.Column (db.String (20), nullable=False)
    descripcion = db.Column (db.String (100), nullable = True)

class EspacioAsignado(db.Model):
    id_espacio_asignado = db.Column (db.Integer, primary_key=True)
    nombre_guardia = db.Column (db.String (50), db.ForeignKey('guardia.nombre_guardia'))
    id_espacio = db.Column (db.Integer, db.ForeignKey('espacios.id_espacio'))
    hora_inicio = db.Column (db.Time, nullable=False)
    hora_fin = db.Column (db.Time, nullable=False)
    fecha = db.Column (db.Date, nullable=False)

class PPL(db.Model):
    id_PPL = db.Column (db.Integer, primary_key=True)
    nombre_ppl = db.Column (db.String(50), nullable=False)
    n_de_celda = db.Column (db.Integer, nullable=False)
    id_guardia = db.Column (db.Integer, db.ForeignKey('guardia.id_guardia'))
    id_pabellon = db.Column (db.Integer, db.ForeignKey('pabellon.id_pabellon'))


with app.app_context():
    db.create_all()

@app.route("/espacioinput", methods = ["GET","POST"])
def agregar_datos_espacios(): 
    if request.method == "POST":
        diccionario = request.form
        nombre_espacio = diccionario ["nombre_espacio"]
        descripcion = diccionario ["descripcion"]
        datos_a_agregar = Espacios(nombre_espacio=nombre_espacio, descripcion=descripcion)
        db.session.add(datos_a_agregar)
        db.session.commit()
    return (render_template("formularioespacios.html"))

@app.route("/guardiainput", methods = ["GET","POST"])
def agregar_datos_guardias():
    if request.method == "POST":
        diccionario= request.form
        nombre_guardia = diccionario ["nombre_guardia"]
        id_espacio_asignado = diccionario ["id_espacio_asignado"]
        datos_a_agregar = Guardia(nombre_guardia=nombre_guardia, id_espacio_asignado=id_espacio_asignado)
        db.session.add(datos_a_agregar)
        db.session.commit()
    return (render_template("formularioguardias.html"))
    
@app.route("/pabelloninput", methods = ["GET", "POST"])
def agregar_datos_pabellon():
    if request.method == "POST":
        diccionario = request.form
        nombre_pabellon = diccionario ["nombre_pabellon"]
        datos_a_agregar = Pabellon(nombre_pabellon=nombre_pabellon)
        db.session.add(datos_a_agregar)
        db.session.commit()
    return (render_template("formulariopabellon.html"))

@app.route("/espacioasignadoinput", methods = ["GET", "POST"])
def agregar_datos_espacioasignado():
    if request.method == "POST":
        diccionario = request.form
        id_espacio= diccionario["id_espacio"]
        hora_inicio_raw = diccionario ["hora_inicio"]
        hora_fin_raw = diccionario ["hora_fin"]
        fecha = diccionario ["fecha"]
        nombre_guardia = diccionario ["nombre_guardia"]
        print(fecha)

        hora_inicio = datetime.strptime(hora_inicio_raw, '%H:%M').time()
        hora_fin = datetime.strptime(hora_fin_raw, '%H:%M').time()
        

        print("---------------------------------------------------")
        print(hora_inicio, hora_fin)
        print(type(hora_inicio), type(hora_fin))

        print("---------------------------------------------------")


        datos_a_agregar = EspacioAsignado(id_espacio=id_espacio, hora_inicio=hora_inicio, hora_fin=hora_fin, fecha=date, nombre_guardia=nombre_guardia)
        db.session.add(datos_a_agregar)         
        db.session.commit()
    return(render_template("formularioespacioasignado.html"))

@app.route("/pplinput", methods= ["GET", "POST"])
def agregar_datos_ppl():
    if request.method == "POST":
        diccionario = request.form
        nombre_ppl=diccionario ["nombre_ppl"]
        n_de_celda = diccionario ["n_de_celda"]
        id_guardia = diccionario ["id_guardia"]
        id_pabellon = diccionario ["id_pabellon"]
        datos_a_agregar = PPL(nombre_ppl=nombre_ppl, n_de_celda=n_de_celda,id_guardia=id_guardia,id_pabellon=id_pabellon)
        db.session.add(datos_a_agregar)
        db.session.commit()
    return(render_template("formularioppl.html"))
       




#Esto para que podamos correr
if __name__ == "__main__":
    app.run (debug=True)