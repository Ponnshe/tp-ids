# frontend/app.py
from flask import Flask, render_template,request
import requests
import urllib
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index1.html')

@app.route('/admin',methods=['GET','POST'])
def admin():
    
    if request.method == "POST" :
        nombre = request.form.get("fnombre")
        descripcion = request.form.get("fdescripcion")
        capacidad = request.form.get("fcapacidad")
        precio = request.form.get("fprecio")
        imagen = request.form.get("fimagen")

        cabin_data = {
            "nombre": nombre,
            "descripcion": descripcion,
            "capacidad": capacidad,
            "precio": precio,
            "imagen": imagen
        }

        response = requests.post('http://backend:5001/create_cabin', json=cabin_data)
        
    response = requests.get('http://backend:5001/cabins')

    if response.status_code == 200:
        cabins= response.json()
        return render_template('admin.html', cabins=cabins)
    else:
        
        return "Error al obtener los datos del backend"
    

    
@app.route('/reservasadmin')
def reservasadmin():

    response = requests.get('http://backend:5001/reservas-admin')

    if request.method == "POST" :
        nombre = request.form.get("fnombre")
        capacidad = request.form.get("fcapacidad")
        entrada = request.form.get("fentrada")
        salida = request.form.get("fsalida")

        reserva_data = {
            "nombre": nombre,
            "cantidad_personas": capacidad,
            "fecha_entrada": entrada,
            "fecha_salida": salida
        }

        response = requests.post('http://backend:5001/reservas', json=reserva_data)

    if response.status_code == 200:
        reservas= response.json()
        return render_template('reservas-admin.html', reservas=reservas)
    else:
        
        return "Error al obtener los datos del backend"
    

@app.route('/admin/delete_cabin',methods=['GET','POST'])
def admin_delete_cabin():
    response = requests.get('http://backend:5001/cabins')

    if request.method == "POST" :
        id = request.form.get("fid")
        
        cabin_data = {
            "id": id
        }
        
        response = requests.delete('http://backend:5001/delete_cabin', json=cabin_data)
        
        
    if response.status_code == 200:
        cabins= response.json()
        return render_template('admin-delete-cabin.html', cabins=cabins)
    else:
        
        return "Error al obtener los datos del backend"



@app.route('/cabins')
def cabins():
# Hacer la solicitud GET a la API del backend para obtener los datos
    response = requests.get('http://backend:5001/cabins')
    # Si la solicitud es exitosa, obtener los datos en formato JSON
    if response.status_code == 200:
        cabins= response.json()
        # Renderizar la plantilla HTML con los datos obtenidos
        return render_template('cabins.html', cabins=cabins)
    else:
        # Si la solicitud falla, mostrar un mensaje de error
        return "Error al obtener los datos del backend"

@app.route('/cabin/<int:id>')
def cabin(id):
    response = requests.get(f'http://backend:5001/cabins/{id}')
    if response.status_code == 200:
        cabin = response.json()
        return render_template('cabin.html', cabin=cabin)
    else:
        return "Error al obtener los datos del backend"


@app.route('/reservar', methods=['GET'])
def reservar():
    data = request.args.get('data')
    cabin_id = request.args.get('id')
    data = eval(data)
    return render_template('reservar.html', data=data, id=cabin_id)

@app.route('/filtered_cabins', methods=['POST'])
def filtered_cabins():
    fecha_entrada = request.form['fechaIngreso']
    fecha_salida = request.form['fechaSalida']
    cantidad_personas = request.form['personas']

    filtered_cabins = requests.get(f'http://backend:5001/filter_cabins?fechaIngreso={fecha_entrada}&fechaSalida={fecha_salida}&personas={cantidad_personas}')

    if filtered_cabins.status_code != 200:
        return "Error al obtener los datos del backend"

    filtered_cabins = filtered_cabins.json()
    data = {
        "fecha_salida": fecha_salida,
        "fecha_entrada": fecha_entrada,
        "cantidad_personas":cantidad_personas
    }
    return render_template('filtered_cabins.html', filtered_cabins=filtered_cabins, data=data)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
