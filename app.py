import requests
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Lista para almacenar los pacientes (solo para este ejemplo)
pacientes = []

# URL del servidor HAPI FHIR
server_url = "http://localhost:8080"
# server_url = "http://hapi.fhir.org/baseR4"


@app.route('/')
def index():
    return render_template('registro_paciente.html')

@app.route('/registrar_paciente', methods=['POST'])
def registrar_paciente():
    nombre = request.form['nombre']
    genero = request.form['genero']
    fecha_nacimiento = request.form['fecha_nacimiento']
    direccion = request.form['direccion']
    telefono = request.form['telefono']

    # Crear un recurso de paciente en formato FHIR JSON
    paciente_fhir = {
        "resourceType": "Patient",
        "name": [{"text": nombre}],
        "gender": genero,
        "birthDate": fecha_nacimiento,
        "address": [{"text": direccion}],
        "telecom": [{"value": telefono}]
    }

    # Enviar la solicitud POST al servidor HAPI FHIR
    response = requests.post(f"{server_url}/fhir/Patient", json=paciente_fhir)

    # Verificar si la solicitud fue exitosa
    if response.status_code == 201:
        pacientes.append(paciente_fhir)  # Opcional: agregar el paciente a la lista local
        return redirect(url_for('index'))
    else:
        return "Error al registrar el paciente en el servidor HAPI FHIR", 500

@app.route('/buscar_pacientes', methods=['GET'])
def buscar_pacientes():
    nombre_buscado = request.args.get('buscar')
    server_url="http://localhost:8080/fhir"
    # Realiza una solicitud GET al servidor HAPI FHIR para buscar pacientes por nombre
    response = requests.get(f"{server_url}/Patient?name={nombre_buscado}")

    # Verifica si la solicitud fue exitosa
    if response.status_code == 200:
        # Parsea la respuesta JSON
        pacientes_encontrados = response.json()
        for entry in pacientes_encontrados.get('entry', []):
            paciente = entry.get('resource', {})
            nombre = paciente.get('name', [{}])[0].get('text', 'Nombre no disponible')
            if nombre=='Nombre no disponible':
                given=paciente.get('name', [{}])[0].get('given')
                #print(given[0])
                nombre = given[0]+ " "+paciente.get('name', [{}])[0].get('family', 'Nombre no disponible')
            #print("Nombre del paciente:", nombre)
            
        #print(pacientes_encontrados)
        return render_template('registro_paciente.html', pacientes=pacientes_encontrados)
        #return render_template('registro_paciente.html')
    else:
        return "Error al buscar pacientes en el servidor HAPI FHIR", 500


@app.route('/buscar', methods=['GET'])
def buscar():
    return render_template('registro_paciente.html', pacientes=pacientes)


if __name__ == '__main__':
    app.run(debug=True)