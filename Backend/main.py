from fastapi import FastAPI, HTTPException
import pandas as pd
from datetime import datetime
from functions import *

df_aircrafts = None
df_airports = None
df_tickets = None
df_passengers = None
df_flights = None

df_mainView = None

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/load_data")
async def load_data():
    global df_aircrafts
    global df_airports
    global df_tickets
    global df_passengers
    global df_flights

    df_aircrafts = pd.read_csv('data/aircrafts.csv')
    df_airports = pd.read_csv('data/airports.csv')
    df_tickets = pd.read_csv('data/tickets.csv')
    df_passengers = pd.read_csv('data/passengers.csv')
    df_flights = pd.read_csv('data/flights.csv')

    return {'message': 'Successful upload!'}

@app.get("/load_mainView")
async def load_mainView():
    global df_mainView

    año_actual = datetime.now().year
    df_passengers['age'] = año_actual - df_passengers['birthDate'].astype(int)
    # Unir DataFrames para obtener datos completos de vuelos
    df_merged = pd.merge(df_tickets, df_flights, on='flightNumber')
    df_merged = pd.merge(df_merged, df_passengers, on='passengerID')
    df_merged = pd.merge(df_merged, df_aircrafts, on='aircraftID')
    # Unir con df_airports para origen y destino
    # Asegúrate de renombrar las columnas para evitar conflictos
    df_merged = pd.merge(df_merged, df_airports.rename(columns={'name': 'name_origin', 'lat': 'lat_origin', 'lon': 'lon_origin'}), left_on='originIATA', right_on='airportIATA')
    df_merged = pd.merge(df_merged, df_airports.rename(columns={'name': 'name_destination', 'lat': 'lat_destination', 'lon': 'lon_destination'}), left_on='destinationIATA', right_on='airportIATA')
    # Calcular la edad promedio de pasajeros por vuelo
    edad_promedio = df_merged.groupby('flightNumber')['age'].mean().astype(int)
    # Contar la cantidad de pasajeros por vuelo
    cantidad_pasajeros = df_merged.groupby('flightNumber').size()
    # Crear el DataFrame final con la información requerida
    df_mainView = df_merged[['flightNumber', 'name_origin', 'name_destination', 'airline', 'year', 'month', 'lat_origin', 'lon_origin', 'lat_destination', 'lon_destination']]
    df_mainView = df_mainView.drop_duplicates(subset=['flightNumber'])
    df_mainView['edad_promedio'] = df_mainView['flightNumber'].map(edad_promedio)
    df_mainView['cantidad_pasajeros'] = df_mainView['flightNumber'].map(cantidad_pasajeros)
    df_mainView['distancia'] = df_mainView.apply(lambda row: haversine(row['lat_origin'], row['lon_origin'], row['lat_destination'], row['lon_destination']), axis=1)
    df_mainView.drop(['lat_origin', 'lon_origin','lat_destination', 'lon_destination'], axis=1, inplace=True)
    # Ordenar el DataFrame final
    df_mainView = df_mainView.sort_values(by=['year', 'month', 'flightNumber'])

    return {'message': 'Successful upload!'}

@app.get("/flightView/{flightNumber}")
async def flightView(flightNumber: str):
    df_flights_especifico = df_flights[df_flights['flightNumber'] == int(flightNumber)]
    df_flights_aircraft = pd.merge(df_flights_especifico, df_aircrafts, on='aircraftID')

    df_final = pd.merge(df_flights_aircraft, df_airports.rename(columns={'name': 'name_origin', 'lat': 'lat_origin', 'lon': 'lon_origin'}), left_on='originIATA', right_on='airportIATA')
    df_final = pd.merge(df_final, df_airports.rename(columns={'name': 'name_destination', 'lat': 'lat_destination', 'lon': 'lon_destination'}), left_on='destinationIATA', right_on='airportIATA')

    return df_final.to_dict()


@app.get("/flightViewPassengers/{flightNumber}")
async def flightViewPassengers(flightNumber: str):
    df_flights_especifico = df_flights[df_flights['flightNumber'] == int(flightNumber)]
    df_flights_tickets = pd.merge(df_flights_especifico, df_tickets, on='flightNumber')
    df_final = pd.merge(df_flights_tickets, df_passengers, on='passengerID')

    df_final = df_final[['avatar', 'firstName', 'lastName', 'age', 'gender', 'weight(kg)', 'height(cm)', 'seatNumber']]
    return df_final.to_dict()


@app.get("/mainView")
async def mainView():
    return df_mainView.to_dict()