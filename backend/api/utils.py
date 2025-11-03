# cab_booking/utils.py
import requests
from django.conf import settings
from django.core.cache import cache
import logging
import math

logger = logging.getLogger(__name__)

CACHE_TIMEOUT = 86400  # 1 day

def get_coordinates(address):
    
    cached = cache.get(f"coords:{address}")
    if cached:
        return cached

    api_key = settings.API_KEY
    url = f"https://api.distancematrix.ai/maps/api/geocode/json?address={address}&key={api_key}"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        results = data.get('result')
        if data.get('status') == 'OK' and results:
            location = results[0].get('geometry', {}).get('location')
            if location and 'lat' in location and 'lng' in location:
                coords = (location['lat'], location['lng'])
                cache.set(f"coords:{address}", coords, CACHE_TIMEOUT)
                return coords

        raise Exception(data.get('error_message', 'Unknown geocoding error.'))

    except Exception as e:
        logger.error(f"Geocoding error: {e}")
        raise


def get_distance_km(origin_lat, origin_lng, dest_lat, dest_lng):
    
    key = f"distance:{origin_lat},{origin_lng}:{dest_lat},{dest_lng}"
    cached = cache.get(key)
    if cached:
        return cached

    api_key = settings.API_KEY
    url = f"https://api.distancematrix.ai/maps/api/distancematrix/json?origins={origin_lat},{origin_lng}&destinations={dest_lat},{dest_lng}&key={api_key}"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        rows = data.get('rows', [])
        if data.get('status') == 'OK' and rows:
            elements = rows[0].get('elements', [])
            if elements and elements[0].get('status') == 'OK':
                distance_km = elements[0]['distance']['value'] / 1000
                cache.set(key, distance_km, CACHE_TIMEOUT)
                return distance_km

        # fallback to Haversine if API fails
        distance_km = haversine_distance(origin_lat, origin_lng, dest_lat, dest_lng)
        logger.warning(f"Using Haversine fallback for distance: {distance_km} km")
        cache.set(key, distance_km, CACHE_TIMEOUT)
        return distance_km

    except Exception as e:
        logger.error(f"Distance calculation error: {e}")
        # fallback to Haversine if API fails
        distance_km = haversine_distance(origin_lat, origin_lng, dest_lat, dest_lng)
        logger.warning(f"Using Haversine fallback for distance: {distance_km} km")
        cache.set(key, distance_km, CACHE_TIMEOUT)
        return distance_km


def haversine_distance(lat1, lng1, lat2, lng2):
    
    R = 6371  # Earth radius in km
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lng2 - lng1)

    a = math.sin(delta_phi / 2) ** 2 + \
        math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


def calculate_price(distance_km, vehicle_model):
     
    base_fares = {"sedan": 50, "suv": 70, "coupe": 60, "mini van": 65}
    per_km_rates = {"sedan": 12, "suv": 15, "coupe": 30, "mini van": 13}

    base_fare = base_fares.get(vehicle_model.lower(), 50)
    per_km_rate = per_km_rates.get(vehicle_model.lower(), 12)

    return base_fare + (per_km_rate * distance_km)
