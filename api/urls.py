from django.urls import include, path
from rest_framework.routers import DefaultRouter
from api.views import ParkingSpotViewSet, CurrentLocation

router = DefaultRouter(trailing_slash=False)
router.register('parkingspots', ParkingSpotViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('/get_points', CurrentLocation.as_view())
]
