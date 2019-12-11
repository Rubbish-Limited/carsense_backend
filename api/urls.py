from django.urls import include, path
from rest_framework.routers import DefaultRouter
from api.views import ParkingSpotViewSet

router = DefaultRouter(trailing_slash=False)
router.register('parkingspots', ParkingSpotViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
