import numpy as np

def haversine(lat1, lon1, lat2, lon2):
    """
    Calcula la distancia en kilómetros entre dos puntos en la Tierra dados por sus coordenadas latitudinales y longitudinales.
    """
    # Radio de la Tierra en kilómetros
    R = 6371.0

    # Conversión de coordenadas de grados a radianes
    lat1 = np.radians(lat1)
    lon1 = np.radians(lon1)
    lat2 = np.radians(lat2)
    lon2 = np.radians(lon2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    # Fórmula del Haversine
    a = np.sin(dlat / 2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2)**2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))

    # Distancia en kilómetros
    distance = R * c
    return int(distance)