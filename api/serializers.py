from rest_framework import serializers
from api.models import ParkingSpot

class ParkingSpotSerializer(serializers.ModelSerializer):

    class Meta:
        model = ParkingSpot
        fields = (
            'id',
            'x',
            'y',
            'free'
        )
        