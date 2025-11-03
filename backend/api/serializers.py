
# cab_booking/serializers.py
from rest_framework import serializers
from .utils import get_coordinates, get_distance_km

from .models import Booking

class BookingSerializer(serializers.ModelSerializer):
    distance_km = serializers.SerializerMethodField()#wanted to add dintance as well in the api res so added this method 
    class Meta:
        model = Booking
        fields = ['id', 'user', 'pickup_location', 'drop_location', 'fare', 'created_at', 'distance_km']
        read_only_fields = ['id', 'user', 'fare', 'created_at']

    def get_distance_km(self, obj):
        origin_lat, origin_lng = get_coordinates(obj.pickup_location)
        dest_lat, dest_lng = get_coordinates(obj.drop_location)
        return get_distance_km(origin_lat, origin_lng, dest_lat, dest_lng)


CAR_CHOICES = ["sedan", "suv", "coupe", "mini van"]

class DistanceRequestSerializer(serializers.Serializer):
    
    pickup = serializers.CharField(max_length=255)
    drop = serializers.CharField(max_length=255)
    choice = serializers.ChoiceField(choices=CAR_CHOICES, default="sedan")

    def validate(self, data):
        
        pickup = data.get("pickup", "").strip().lower()
        drop = data.get("drop", "").strip().lower()
        if pickup == drop:
            raise serializers.ValidationError("Pickup and drop locations must be different.")
        return data 