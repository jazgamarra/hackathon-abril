
from time import time
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy

import datetime
import time


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///basededatos.db'
db = SQLAlchemy(app)

class Pabellon(db.Model):
    id_pabellon = db.Column (db.Integer, primary_key=True)
    nombre_pabellon = db.Column(db.String(10), nullable=False)

class Guardia(db.Model):
    id_guardia = db.Column (db.Integer, primary_key=True)
    nombre_guardia = db.Column (db.String (50), nullable=False) 
    id_pabellon = db.Column (db.Integer, db.ForeignKey('pabellon.id_pabellon'))
    # id_espacio_asignado = db.Column (db.Integer, db.ForeignKey('espacioasignado.id_espacio_asignado'))

class Espacios(db.Model):
    id_espacio = db.Column (db.Integer, primary_key=True)
    nombre_espacio = db.Column (db.String (20), nullable=False)
    descripcion = db.Column (db.String (100), nullable = True)

class EspacioAsignado(db.Model):
    id_espacio_asignado = db.Column (db.Integer, primary_key=True)
    id_guardia = db.Column (db.Integer, db.ForeignKey('guardia.id_guardia'))
    id_espacio = db.Column (db.Integer, db.ForeignKey('espacios.id_espacio'))
    epoch_inicio = db.Column (db.Integer, nullable=False)
    epoch_fin = db.Column (db.Integer, nullable=False)
    

class PPL(db.Model):
    id_PPL = db.Column (db.Integer, primary_key=True)
    nombre_ppl = db.Column (db.String(50), nullable=False)
    n_de_celda = db.Column (db.Integer, nullable=False)
    id_guardia = db.Column (db.Integer, db.ForeignKey('guardia.id_guardia'))
    id_pabellon = db.Column (db.Integer, db.ForeignKey('pabellon.id_pabellon'))


with app.app_context():
    db.create_all()

def convertir_a_epoch (fecha_str, hora_str):
    '''Convertir fecha y hora a objetos datetime''' 
    fecha_hora_str = fecha_str + ' ' + hora_str
    fecha_hora = datetime.datetime.strptime(fecha_hora_str, '%Y-%m-%d %H:%M')
    #calcular epoch
    epoch = int(time.mktime(fecha_hora.timetuple()))
    return epoch


        
        

@app.route("/espacioinput", methods = ["GET","POST"])
def agregar_datos_espacios(): 
    if request.method == "POST":
        diccionario = request.form
        nombre_espacio = diccionario ["nombre_espacio"]
        descripcion = diccionario ["descripcion"]
        datos_a_agregar = Espacios(nombre_espacio=nombre_espacio, descripcion=descripcion)
        db.session.add(datos_a_agregar)
        db.session.commit()
    return render_template("formularioespacios.html")

@app.route("/guardiainput", methods = ["GET","POST"])
def agregar_datos_guardias():
    if request.method == "POST":
        diccionario= request.form
        nombre_guardia = diccionario ["nombre_guardia"]
        id_pabellon = diccionario ["id_pabellon"]

        datos_a_agregar = Guardia(nombre_guardia=nombre_guardia, id_pabellon=id_pabellon)  
        db.session.add(datos_a_agregar)
        db.session.commit()

    #  Obtener lista de pabellones de la db 
    lista_pabellones = Pabellon.query.all()

    return (render_template("formularioguardias.html", lista_pabellones=lista_pabellones))
    
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
        id_espacio = diccionario["id_espacio"]
        hora_inicio_raw = diccionario ["hora_inicio"]
        hora_fin_raw = diccionario ["hora_fin"]
        fecha_raw = diccionario ["fecha"]
        id_guardia = diccionario ["id_guardia"]
   
        hora_inicio = convertir_a_epoch (fecha_raw, hora_inicio_raw)
        hora_fin = convertir_a_epoch (fecha_raw, hora_fin_raw)

        datos_a_agregar = EspacioAsignado(id_guardia=id_guardia, id_espacio=id_espacio, epoch_inicio=hora_inicio, epoch_fin=hora_fin)
        db.session.add(datos_a_agregar)         
        db.session.commit()
    lista_espacios = Espacios.query.all()
    lista_guardias = Guardia.query.all()
    return(render_template("formularioespacioasignado.html", lista_espacios = lista_espacios, lista_guardias=lista_guardias))

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

    lista_guardias = Guardia.query.all()
    lista_pabellones = Pabellon.query.all()
    return(render_template("formularioppl.html", lista_guardias=lista_guardias, lista_pabellones=lista_pabellones))

def crear_lista_turnos(): 
    query_espacios_asignados = EspacioAsignado.query.all()
    lista_espacios = []

    for esp in query_espacios_asignados: 
        lista_espacios.append({
            'espacio': Espacios.query.get(esp.id_espacio).nombre_espacio, 
            'guardia': Guardia.query.get(esp.id_guardia).nombre_guardia, 
            'hora_inicio': esp.epoch_inicio, 
            'hora_fin': esp.epoch_fin
        })
        
    return lista_espacios

@app.route("/api_turnos")
def api_turnos():
    datos = crear_lista_turnos()
    return jsonify(datos)

@app.route("/ver_turnos")
def ver_turnos():   
    return render_template('test_visualizacion.html')  


@app.route('/borrar/<int:id>')
def borrar(id):
    elemento_borrar = Guardia.query.get(id)
    db.session.delete(elemento_borrar)
    db.session.commit()
    return 'se borro el id',id

if __name__ == "__main__":
    app.run (debug=True)