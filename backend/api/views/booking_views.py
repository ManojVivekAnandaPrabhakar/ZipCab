#api/views/booking_views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated,AllowAny
from ..serializers import DistanceRequestSerializer, BookingSerializer
from ..utils import get_coordinates, get_distance_km, calculate_price
from ..models import Booking


# price calculation this cbv uses the utility fbv

class CalculateFareView(APIView):
    
    
    permission_classes=[IsAuthenticated]
    def post(self, request):
        serializer = DistanceRequestSerializer(data=request.data)
        if serializer.is_valid():
            pickup = serializer.validated_data['pickup']
            drop = serializer.validated_data['drop']
            choice = serializer.validated_data['choice']

            try:
                origin_lat, origin_lng = get_coordinates(pickup)
                dest_lat, dest_lng = get_coordinates(drop)
                distance_km = get_distance_km(origin_lat, origin_lng, dest_lat, dest_lng)
                fare = calculate_price(distance_km, choice)

                return Response({
                    "pickup": pickup,
                    "drop": drop,
                    "choice": choice,
                    "distance_km": round(distance_km, 2),
                    "fare": round(fare, 2),
                }, status=status.HTTP_200_OK)

            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



#just for testing (hardcoded)

@api_view(['GET'])
def test_utilities(request):
    try:
        coords = get_coordinates("marina mall chennai, ashok pillar chennai")
        distance = get_distance_km(coords[0], coords[1], 37.422, -122.084)
        fare = calculate_price(distance, "sedan")
        return Response({
            "distance_km": round(distance, 2),
            "fare": round(fare, 2)
        })
    except Exception as e:
        return Response({"error": str(e)})



#booking create 

class CreateBookingView(APIView):
    permission_classes= [IsAuthenticated]

    def post(self, request):
        data = request.data
        pickup = data.get('pickup_location')
        drop = data.get('drop_location')

        if not pickup or not drop:
            return Response(
                {"error": "Pickup and Drop locations are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            
            origin_lat, origin_lng = get_coordinates(pickup)
            dest_lat, dest_lng = get_coordinates(drop)

            
            distance_km = get_distance_km(origin_lat, origin_lng, dest_lat, dest_lng)

           
            fare = calculate_price(distance_km, data.get('vehicle_choice'))

            
            booking = Booking.objects.create(
                user=request.user,
                pickup_location=pickup,
                drop_location=drop,
                fare=fare
            )

            
            serializer = BookingSerializer(booking)
            booking_data = serializer.data
            booking_data['distance_km'] = round(distance_km, 2)

            return Response(booking_data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


#booking history

class BookingListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        bookings = Booking.objects.filter(user=request.user)
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data)