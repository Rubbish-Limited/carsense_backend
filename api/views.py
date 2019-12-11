from rest_framework import viewsets
from api.models import ParkingSpot
from api.serializers import ParkingSpotSerializer

class ParkingSpotViewSet(viewsets.ModelViewSet):
    serializer_class = ParkingSpotSerializer
    queryset = ParkingSpot.objects.all()