from rest_framework import viewsets
from api.models import ParkingSpot
from api.serializers import ParkingSpotSerializer
from generator.generate import init_state
from rest_framework.views import APIView

class ParkingSpotViewSet(viewsets.ModelViewSet):
    serializer_class = ParkingSpotSerializer
    queryset = ParkingSpot.objects.all()


class CurrentLocation(APIView):

    def get(self, request):
        return init_state()