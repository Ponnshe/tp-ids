# frontend/app.py
from flask import Flask, render_template,request, redirect, url_for, session
from datetime import datetime
import requests
import urllib
app = Flask(__name__)

app.secret_key = 'una_clave_super_secreta_y_larga_que_nadie_pueda_adivinar'


usuarios = {
    'root': 'root',
}

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
    

@app.errorhandler(404)
def page_not_found(e):
    return render_template('page_404.html'), 404

# Rutas para la administración de cabañas
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        # Verificar si los campos están presentes en request.form
        if 'username' in request.form and 'password' in request.form:
            username = request.form['username']
            password = request.form['password']
            if username in usuarios and usuarios[username] == password:
                session['username'] = username
                return redirect(url_for('admin'))
            else:
                error = 'Usuario o contraseña incorrectos. Inténtalo de nuevo.'
        else:
            error = 'Faltan campos en el formulario. Inténtalo de nuevo.'
    return render_template('admin_login.html', error=error)

@app.route('/admin')
def admin():
    if 'username' in session:
        response = requests.get('http://backend:5001/cabins')
        if response.status_code == 200:
            cabins = response.json()
            return render_template('admin.html', cabins=cabins)
        else:
            return "Error al obtener los datos del backend"
        return render_template('admin.html', username=session['username'])
    # Si no hay sesión de usuario, redirigir al login
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/admin/add_cabin',methods=['GET', 'POST'])       
def admin_add_cabin():
    if 'username' in session:
        if request.method == "GET":
            return render_template('add_cabin.html')
        elif request.method == "POST":
            try:
                data = {
                    "nombre": request.form['nombre'],
                    "capacidad": request.form['capacidad'],
                    "descripcion": request.form['descripcion'],
                    "precio": request.form['precio'],
                    "imagen": request.form['imagen']
                }
                response = requests.post('http://backend:5001/create_cabin', json=data)
                if response.status_code == 200:
                    return redirect(url_for('admin'))
                else:
                    return f"Error al agregar la cabaña. Código de error: {response.status_code}"
            except Exception as e:
                return f"Error en la solicitud al backend: {str(e)}", 500

    return redirect(url_for('login'))

@app.route('/admin/delete_cabin/<int:id>',methods=['GET'])
def admin_delete_cabin(id):
    if 'username' in session:
        try:
            cabin_data = {
                "id": id
            }

            response = requests.delete('http://backend:5001/delete_cabin', json=cabin_data)

            if response.status_code == 200:
                return redirect(url_for('admin'))  # Redirigir a la página de administración
            else:
                return f"Error al eliminar la cabaña. Código de error: {response.status_code}. Verifica que no existan reservas asociadas a esta cabaña."

        except Exception as e:
            return f"Error en la solicitud al backend: {str(e)}", 500
    return redirect(url_for('login'))

@app.route('/admin/update_cabin/<int:id>',methods=['GET', 'POST'])
def admin_update_cabin(id):
    if 'username' in session:
        if request.method == "GET":
            response = requests.get(f'http://backend:5001/cabins/{id}')
            if response.status_code == 200:
                cabin = response.json()
                return render_template('update_cabin.html', cabin=cabin)
            else:
                return "Error al obtener los datos del backend"

        elif request.method == "POST":
            try:
                data = {
                        "id": id,
                        "nombre": request.form['nombre'],
                        "capacidad": request.form['capacidad'],
                        "descripcion": request.form['descripcion'],
                        "precio": request.form['precio'],
                        "imagen": request.form['imagen']
                    }
                response = requests.put('http://backend:5001/update_cabin', json=data)
                if response.status_code == 200:
                    return redirect(url_for('admin'))
                else:
                    return f"Error al actualizar la cabaña. Código de error: {response.status_code}"
            except Exception as e:
                    return f"Error en la solicitud al backend: {str(e)}", 500
    return redirect(url_for('login'))
    
@app.route('/reservasadmin')
def reservasadmin():
    if 'username' in session:
        response = requests.get('http://backend:5001/reservas-admin')
        if response.status_code == 200:
            reservas= response.json()
            return render_template('admin-reservas.html', reservas=reservas)
        else:
            
            return "Error al obtener los datos del backend"
    return redirect(url_for('login'))


    
@app.route('/admin/delete_reserva/<int:id>',methods=['GET'])
def admin_delete_reserva(id):
    if 'username' in session:
        try:
            reserva_data = {
                "id": id
            }
                
            response = requests.delete(f'http://backend:5001/reservas/{id}')
                
            if response.status_code == 200:
                return redirect(url_for('reservasadmin'))
            else:
                return f"Error al eliminar la reserva. Código de error: {response.status_code}."

        except Exception as e:
            return f"Error en la solicitud al backend: {str(e)}", 500
    return redirect(url_for('login'))

@app.route('/admin/update_reserva/<int:id>',methods=['GET', 'POST'])
def admin_update_reserva(id):
    if 'username' in session:
        if request.method == "GET":
            response = requests.get(f'http://backend:5001/reservas/{id}')
            if response.status_code == 200:
                reserva = response.json()
                return render_template('update_reserva.html', reserva=reserva)
            else:
                return "Error al obtener los datos del backend"

        elif request.method == "POST":
            try:
                data = {
                    "id": id,
                    "nombre": request.form['nombre'],
                    "apellido": request.form['apellido'],
                    "documento": request.form['documento'],
                    "celular": request.form['celular'],
                    "email": request.form['email'],
                    "cantidad_personas": request.form['cantidad_personas'],
                    "fecha_ingreso": request.form['fecha_ingreso'],
                    "fecha_salida": request.form['fecha_salida'],
                    "cabin_id": request.form['cabin_id']
                }
                response = requests.put(f'http://backend:5001/reservas/{id}', json=data)
                if response.status_code == 200:
                    return redirect(url_for('reservasadmin'))
                else:
                    return f"Error al actualizar la reserva. Código de error: {response.status_code}"
            except Exception as e:
                    return f"Error en la solicitud al backend: {str(e)}", 500
    return redirect(url_for('login'))

            
@app.route('/admin/detalle_reserva/<int:id>',methods=['GET', 'POST'])
def admin_detalle_reserva(id):
    if 'username' in session:
        if request.method == "GET":
            response = requests.get(f'http://backend:5001/reservas/{id}')
            if response.status_code == 200:
                reserva = response.json()
                return render_template('detalle_reserva.html', reserva=reserva)
            else:
                return "Error al obtener los datos del backend"

        elif request.method == "POST":
            try:
                data = {
                    "id": id,
                    "nombre": request.form['nombre'],
                    "apellido": request.form['apellido'],
                    "documento": request.form['documento'],
                    "celular": request.form['celular'],
                    "email": request.form['email'],
                    "cantidad_personas": request.form['cantidad_personas'],
                    "fecha_ingreso": request.form['fecha_ingreso'],
                    "fecha_salida": request.form['fecha_salida'],
                    "cabin_id": request.form['cabin_id']
                }
                response = requests.put(f'http://backend:5001/reservas/{id}', json=data)
                if response.status_code == 200:
                    return redirect(url_for('reservasadmin'))
                else:
                    return f"Error al actualizar la reserva. Código de error: {response.status_code}"
            except Exception as e:
                    return f"Error en la solicitud al backend: {str(e)}", 500  
    return redirect(url_for('login'))
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
