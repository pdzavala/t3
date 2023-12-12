import os

from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
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

# CORS
origins = [
    '*'
]

app.add_middleware(CORSMiddleware,
                   allow_origins=origins,
                   allow_credentials=True,
                   allow_methods=['*'],
                   allow_headers=['*'],
                   max_age=3600)

@app.get("/")
def root():
    return {"message": "Taller de Integración - Tarea 3"}

@app.get("/loadflights")
async def loadflights():
    global df_mainView
    global df_aircrafts
    global df_airports
    global df_tickets
    global df_passengers
    global df_flights

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
    
    return df_mainView.to_json(orient='records')

@app.get("/getflights", response_model=list)
async def getflights():
    global df_mainView
    global df_aircrafts
    global df_airports
    global df_tickets
    global df_passengers
    global df_flights
    
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

    json_array = df_mainView.to_dict(orient='records')

    return JSONResponse(content=json_array)

@app.get("/flights/{flightNumber}", response_model=list)
async def flightView(flightNumber: int):
    df_flights_especifico = df_flights[df_flights['flightNumber'] == int(flightNumber)]
    df_flights_aircraft = pd.merge(df_flights_especifico, df_aircrafts, on='aircraftID')

    df_final = pd.merge(df_flights_aircraft, df_airports.rename(columns={'name': 'name_origin', 'lat': 'lat_origin', 'lon': 'lon_origin'}), left_on='originIATA', right_on='airportIATA')
    df_final = pd.merge(df_final, df_airports.rename(columns={'name': 'name_destination', 'lat': 'lat_destination', 'lon': 'lon_destination'}), left_on='destinationIATA', right_on='airportIATA')

    json_array = df_final.to_dict(orient='records')
    return JSONResponse(content=json_array)

    

