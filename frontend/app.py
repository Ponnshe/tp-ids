# frontend/app.py
from flask import Flask, render_template,request,url_for
from datetime import datetime
import requests
import urllib
app = Flask(__name__)

@app.route('/')
def index():
    # Hacer la solicitud GET a la API del backend para obtener los datos
    response = requests.get('http://backend:5001/cabins')
    # Si la solicitud es exitosa, obtener los datos en formato JSON
    if response.status_code == 200:
        cabins= response.json()
        # Renderizar la plantilla HTML con los datos obtenidos
        return render_template('index1.html', cabins=cabins)
    else:
        # Si la solicitud falla, mostrar un mensaje de error
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

@app.route('/reservar', methods=['GET', 'POST'])
def reservar():
    if request.method == 'POST':
        data = request.form
        response = requests.post('http://backend:5001/reservas', data=data)
        if response.status_code == 200 or response.status_code == 201:
            return render_template('confirmada.html')
        else:
            return "Error al hacer la reserva"
    else:
        data = request.args.get('data')
        cabin_id = request.args.get('id')
        response = requests.get(f'http://backend:5001/cabins/{cabin_id}')
        if response.status_code != 200:
            return "Error al hacer la reserva"
        cabin = response.json()
        if data:
            data = eval(data)
            fecha_salida = datetime.strptime(data['fecha_salida'], '%Y-%m-%d')
            fecha_entrada = datetime.strptime(data['fecha_entrada'], '%Y-%m-%d')
            noches = (fecha_salida - fecha_entrada).days
            precioTotal = float(cabin['precio']) * noches
            return render_template('reservar.html', data=data, cabin=cabin, precioTotal=precioTotal, noches=noches)
        return render_template('reservar.html')

@app.route('/listar_reservas')
def listar_reservas():
    response = requests.get('http://backend:5001/reservas')
    if response.status_code == 200:
        reservas = response.json()
        return render_template('lista_reservas.html', reservas=reservas)
    else:
        return "Error al obtener los datos del backend"

if __name__ == '__main__':
    app.run(host='0.0.0.0')
