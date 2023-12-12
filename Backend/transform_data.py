
from fastapi import FastAPI, HTTPException
import pandas as pd
from datetime import datetime
from dateutil import parser
from dateutil import relativedelta
from functions import *

spanish_months = {
    'enero': 'January',
    'febrero': 'February',
    'marzo': 'March',
    'abril': 'April',
    'mayo': 'May',
    'junio': 'June',
    'julio': 'July',
    'agosto': 'August',
    'septiembre': 'September',
    'octubre': 'October',
    'noviembre': 'November',
    'diciembre': 'December'
}


def parse_spanish_date(date_str):
    for spanish_month, english_month in spanish_months.items():
        date_str = date_str.replace(spanish_month, english_month)
    
    date_str = date_str.replace("de", "").strip()
    
    return parser.parse(date_str, dayfirst=True)


def load_data(df_aircrafts, df_airports, df_tickets, df_passengers, df_flights):
    
    df_aircrafts = pd.read_csv('data/aircrafts.csv')
    df_airports = pd.read_csv('data/airports.csv')
    df_tickets = pd.read_csv('data/tickets.csv')
    df_passengers = pd.read_csv('data/passengers.csv')
    df_flights = pd.read_csv('data/flights.csv')

    return df_aircrafts, df_airports, df_tickets, df_passengers, df_flights

def load_mainView(df_aircrafts, df_airports, df_tickets, df_passengers, df_flights, df_mainView):

    df_passengers['birthDate'] = df_passengers['birthDate'].apply(
    lambda x: parse_spanish_date(x).strftime('%d-%m-%Y')
    )

    fecha_actual = datetime.now()

    df_passengers['age'] = df_passengers['birthDate'].apply(
        lambda x: relativedelta.relativedelta(fecha_actual, parser.parse(x))
    ).apply(lambda x: x.years)


    # Unir DataFrames para obtener datos completos de vuelos
    df_merged = pd.merge(df_tickets, df_flights, on='flightNumber')
    df_merged = pd.merge(df_merged, df_passengers, on='passengerID')
    df_merged = pd.merge(df_merged, df_aircrafts, on='aircraftID')
    # Unir con df_airports para origen y destino
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

    return df_aircrafts, df_airports, df_tickets, df_passengers, df_flights, df_mainView

def load_passengers(df_aircrafts, df_airports, df_tickets, df_passengers, df_flights, df_mainView):
    df_passengers['birthDate'] = df_passengers['birthDate'].apply(
        lambda x: parse_spanish_date(x).strftime('%d-%m-%Y')
    )

    fecha_actual = datetime.now()

    df_passengers['age'] = df_passengers['birthDate'].apply(
        lambda x: relativedelta.relativedelta(fecha_actual, parser.parse(x))
    ).apply(lambda x: x.years)

    # Unir DataFrames para obtener datos completos de vuelos
    df_merged = pd.merge(df_tickets, df_flights, on='flightNumber')
    df_merged = pd.merge(df_merged, df_passengers, on='passengerID')
    df_merged = pd.merge(df_merged, df_aircrafts, on='aircraftID')
    # Unir con df_airports para origen y destino
    df_merged = pd.merge(df_merged, df_airports.rename(columns={'name': 'name_origin', 'lat': 'lat_origin', 'lon': 'lon_origin'}), left_on='originIATA', right_on='airportIATA')
    df_merged = pd.merge(df_merged, df_airports.rename(columns={'name': 'name_destination', 'lat': 'lat_destination', 'lon': 'lon_destination'}), left_on='destinationIATA', right_on='airportIATA')
    # Calcular la edad promedio de pasajeros por vuelo
    edad_promedio = df_merged.groupby('flightNumber')['age'].mean().astype(int)
    # Contar la cantidad de pasajeros por vuelo
    cantidad_pasajeros = df_merged.groupby('flightNumber').size()
    # Obtener la lista de pasajeros por vuelo con información de clase
    passengers_info = df_merged.groupby('flightNumber').apply(lambda group: group[['passengerID', 'flightType']].to_dict(orient='records')).to_dict()

    # Crear el DataFrame final con la información requerida
    df_mainView = df_merged[['flightNumber', 'name_origin', 'name_destination', 'airline', 'year', 'month', 'lat_origin', 'lon_origin', 'lat_destination', 'lon_destination']]
    df_mainView = df_mainView.drop_duplicates(subset=['flightNumber'])
    df_mainView['edad_promedio'] = df_mainView['flightNumber'].map(edad_promedio)
    df_mainView['cantidad_pasajeros'] = df_mainView['flightNumber'].map(cantidad_pasajeros)
    df_mainView['distancia'] = df_mainView.apply(lambda row: haversine(row['lat_origin'], row['lon_origin'], row['lat_destination'], row['lon_destination']), axis=1)
    df_mainView.drop(['lat_origin', 'lon_origin','lat_destination', 'lon_destination'], axis=1, inplace=True)
    df_mainView['passenger_info'] = df_mainView['flightNumber'].map(passengers_info)
    # Ordenar el DataFrame final
    df_mainView = df_mainView.sort_values(by=['year', 'month', 'flightNumber'])

    return df_aircrafts, df_airports, df_tickets, df_passengers, df_flights, df_mainView




def flightView(df_flights, df_aircrafts, df_airports, flightNumber: str):
    df_flights_especifico = df_flights[df_flights['flightNumber'] == int(flightNumber)]
    df_flights_aircraft = pd.merge(df_flights_especifico, df_aircrafts, on='aircraftID')

    df_final = pd.merge(df_flights_aircraft, df_airports.rename(columns={'name': 'name_origin', 'lat': 'lat_origin', 'lon': 'lon_origin'}), left_on='originIATA', right_on='airportIATA')
    df_final = pd.merge(df_final, df_airports.rename(columns={'name': 'name_destination', 'lat': 'lat_destination', 'lon': 'lon_destination'}), left_on='destinationIATA', right_on='airportIATA')

    return df_final.to_dict()


def flightViewPassengers(df_flights, df_tickets, df_passengers, flightNumber: str):
    df_flights_especifico = df_flights[df_flights['flightNumber'] == int(flightNumber)]
    df_flights_tickets = pd.merge(df_flights_especifico, df_tickets, on='flightNumber')
    df_final = pd.merge(df_flights_tickets, df_passengers, on='passengerID')

    df_final = df_final[['avatar', 'firstName', 'lastName', 'age', 'gender', 'weight(kg)', 'height(cm)', 'seatNumber']]
    return df_final.to_dict()

def mainView(df_mainView):
    return df_mainView.to_dict()