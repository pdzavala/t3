import os
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from google.api_core.protobuf_helpers import get_messages
from google.cloud import storage
import pandas as pd
import populate_data as pop
from dotenv import load_dotenv
from transform_data import *

load_dotenv()

GOOGLE_APPLICATION_CREDENTIAL = os.getenv('GOOGLE_APPLICATION_CREDENTIAL')
BUCKET_NAME = os.getenv('BUCKET_NAME')

class Bucket:
    def __init__(self, storage_client):
        self.client = storage_client

    def list_blobs(self, bucket_name):
        blobs = self.client.list_blobs(bucket_name)
        return blobs


    # Crear cliente de almacenamiento
storage_client = storage.Client.from_service_account_json(GOOGLE_APPLICATION_CREDENTIAL)
bucket = Bucket(storage_client)

### INICIO DE LA API ###
app = FastAPI()

@app.get("/")
def root():
    return {"message": "Taller de Integración - Tarea 3"}

@app.get("/loadData", response_class=HTMLResponse)
async def loadData():
    files = pop.descargar_blobs(bucket)
    for file in files:
        aux = file.split('.')
        if aux[1] == 'json':
            pop.json_to_csv(file, aux[0]+'.csv')
            pop.eliminar_archivo(file)
        elif aux[1] == 'xml':
            pop.convertir_xml_a_csv(file, aux[0]+'.csv')
            pop.eliminar_archivo(file)
        elif aux[1] == 'yaml':
            pop.convertir_yaml_a_csv(file, aux[0]+'.csv')
            pop.eliminar_archivo(file)
    

    df_aircrafts = None
    df_airports = None
    df_tickets = None
    df_passengers = None
    df_flights = None
    df_mainView = None


    df_aircrafts, df_airports, df_tickets, df_passengers, df_flights = load_data(df_aircrafts, df_airports, df_tickets, df_passengers, df_flights)
    print('Data loaded successfully!')
    df_aircrafts, df_airports, df_tickets, df_passengers, df_flights, df_mainView = load_mainView(df_aircrafts, df_airports, df_tickets, df_passengers, df_flights, df_mainView)
    print('Data loaded successfully!')

   

    

