from flask import Flask, render_template, request, redirect, url_for
import os
import pandas as pd

from funciones import calcular_medias
from funciones import guardar_grafica
from funciones import mean,var,std

from funciones import price_per_hour, guardar_precio



app = Flask(__name__)

# Especifica la URL base directamente
BASE_URL = 'http://localhost:5000/'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'archivo' not in request.files:
        return 'No se envió ningún archivo CSV', 400

    archivo = request.files['archivo']

    if archivo.filename == '':
        return 'No se seleccionó ningún archivo', 400

    # Guarda el archivo en el servidor
    archivo_path = os.path.join('uploads', archivo.filename)
    archivo.save(archivo_path)
   
    total_list = calcular_medias(archivo_path)
    guardar_grafica(total_list)

    preciokwh_path='preciokwh.csv'
    precio= price_per_hour(archivo_path,preciokwh_path)
    guardar_precio(precio)

    # Redirige a la página de resultados
    return redirect(url_for('resultado', archivo_path=archivo_path))

@app.route('/resultado')
def resultado():
    # Obtiene la URL base y la ruta del archivo guardado
    archivo_path = request.args.get('archivo_path')
    df = pd.read_csv(archivo_path)
    m=mean(df['Consumo'])
    v=var(df['Consumo'])
    d=std(df['Consumo'])


    params = {
        'base_url': BASE_URL,
        'archivo_path': archivo_path,
        'media': m,
        'varianza': v,
        'desviacion': d,
    }
    return render_template('resultado.html', **params)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
