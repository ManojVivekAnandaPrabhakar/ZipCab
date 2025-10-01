#cab_booking/utils.py
import requests
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

def get_coordinates(address):
    
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
                return location['lat'], location['lng']
        raise Exception(data.get('error_message', 'Unknown geocoding error.'))
    except Exception as e:
        logger.error(f"Geocoding error: {e}")
        raise

def get_distance_km(origin_lat, origin_lng, dest_lat, dest_lng):
    
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
                return elements[0]['distance']['value'] / 1000
        raise Exception(elements[0].get('status', 'Unknown distance error.') if elements else 'No elements found.')
    except Exception as e:
        logger.error(f"Distance calculation error: {e}")
        raise

def calculate_price(distance_km, vehicle_model):
    
    base_fares = {"sedan": 50, "suv": 70, "coupe": 60, "mini van": 65}
    per_km_rates = {"sedan": 12, "suv": 15, "coupe": 30, "mini van": 13}
    base_fare = base_fares.get(vehicle_model.lower(), 50)
    per_km_rate = per_km_rates.get(vehicle_model.lower(), 12)
    return base_fare + (per_km_rate * distance_km)
 