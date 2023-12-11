import os
import json
import csv
import pandas as pd
from google.api_core.protobuf_helpers import get_messages
from google.cloud import storage
import pathlib
from fastapi import FastAPI
from dotenv import load_dotenv
import xml.etree.ElementTree as ET
import yaml

load_dotenv()

GOOGLE_APPLICATION_CREDENTIAL = os.getenv('GOOGLE_APPLICATION_CREDENTIAL')
BUCKET_NAME = os.getenv('BUCKET_NAME')

# Unir todos los flights en un archivo JSON
def merge_json_flights(blob_names, files):
    # Lista para almacenar datos combinados
    flights_data = []

    # Iterar sobre cada archivo de entrada
    for name in blob_names:
        path = pathlib.Path('data/' + name)
        info = name.split('-')
        # print(info)
        with open(path, 'r') as archivo:
            # Cargar datos JSON del archivo actual
            data = json.load(archivo)
            # Agregar información de la aerolínea al conjunto de datos
            for flight in data:
                flight['year'] = info[1]
                flight['month'] = info[2]
                      
            # Agregar datos al conjunto combinado
            flights_data.extend(data)

    # Guardar datos combinados en un nuevo archivo JSON
    path = pathlib.Path('data/flights.json')
    files.append('data/flights.json')
    with open(path, 'w') as archivo:
        json.dump(flights_data, archivo, indent=2)

# Eliminar flights ya descargados:
def eliminar_archivo(ruta_archivo):
    try:
        os.remove(ruta_archivo)
        #print(f"El archivo {ruta_archivo} ha sido eliminado correctamente.")
    except FileNotFoundError:
        print(f"El archivo {ruta_archivo} no fue encontrado.")
    except Exception as e:
        print(f"Ocurrió un error al intentar eliminar el archivo {ruta_archivo}: {str(e)}")


# Iterar sobre cada archivo en el depósito y guradarlo en la carpeta data
def descargar_blobs(bucket):
    blob_names = []
    files = []
    flight_files = []
    for blob in bucket.list_blobs(BUCKET_NAME):
        
        if str(blob.name).find('flights') != -1:
            # print('NOMBRE:', blob.name)
            name = str(blob.name).replace('/', '-')
            blob_names.append(name)
            blob.download_to_filename('data/' + str(name))
            flight_files.append('data/' + str(name))
        else:
            files.append('data/' + str(blob.name))
            blob.download_to_filename('data/' + str(blob.name))

    merge_json_flights(blob_names, files)
    #print('FILES:', files)
    #print('FLIGHTS:', flight_files)
    for file in flight_files:
        eliminar_archivo(file)
    
    return files

#JSON a CSV
def json_to_csv(archivo_json, archivo_csv):
    with open(archivo_json, 'r') as archivo_entrada:
        datos_json = json.load(archivo_entrada)

    # Asegurarse de que los datos sean una lista de diccionarios
    if isinstance(datos_json, list) and all(isinstance(item, dict) for item in datos_json):
        # Crear un DataFrame de pandas a partir de la lista de diccionarios
        df = pd.DataFrame(datos_json)

        # Guardar el DataFrame en un archivo CSV
        df.to_csv(archivo_csv, index=False, encoding='utf-8')

        print(f"La conversión de {archivo_json} a {archivo_csv} fue exitosa.")
    else:
        print(f"El archivo {archivo_json} no tiene el formato esperado.")

# XML a CSV
def convertir_xml_a_csv(archivo_xml, archivo_csv):
    tree = ET.parse(archivo_xml)
    root = tree.getroot()

    # Inicializar una lista para almacenar los datos del XML
    datos_xml = []

    # Iterar sobre los elementos del XML
    for elemento in root.findall('.//row'):
        fila = {}
        for campo in elemento.findall('./*'):
            fila[campo.tag] = campo.text
        datos_xml.append(fila)

    # Crear un DataFrame de pandas a partir de la lista de datos del XML
    df = pd.DataFrame(datos_xml)

    # Guardar el DataFrame en un archivo CSV
    df.to_csv(archivo_csv, index=False, encoding='utf-8')

    print(f"La conversión de {archivo_xml} a {archivo_csv} fue exitosa.")

# YAML a CSV
def convertir_yaml_a_csv(archivo_yaml, archivo_csv):
    with open(archivo_yaml, 'r') as archivo_entrada:
        datos_yaml = yaml.safe_load(archivo_entrada)

    if isinstance(datos_yaml, dict) and 'passengers' in datos_yaml:
        # Extraer la lista de pasajeros del diccionario
        lista_pasajeros = datos_yaml['passengers']

        # Crear un DataFrame de pandas a partir de la lista de pasajeros
        df = pd.DataFrame(lista_pasajeros)

        # Guardar el DataFrame en un archivo CSV
        df.to_csv(archivo_csv, index=False, encoding='utf-8')

        print(f"La conversión de {archivo_yaml} a {archivo_csv} fue exitosa.")
    else:
        print(f"El archivo {archivo_yaml} no tiene la estructura adecuada para la conversión.")
