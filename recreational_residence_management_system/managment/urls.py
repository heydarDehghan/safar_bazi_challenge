from rest_framework import routers
from managment.views import ResidenceViewSet, StandardCapacityDetailViewSet, ExtraCapacityDetailViewSet
from django.urls import path, include
from managment.views import free_residence_list, booking
# Define the router instance
router = routers.DefaultRouter()
# Register the viewsets with the router
router.register(r'residences', ResidenceViewSet)
router.register(r'standard_capacity_details', StandardCapacityDetailViewSet)
router.register(r'extra_capacity_details', ExtraCapacityDetailViewSet)

urlpatterns = router.urls

urlpatterns += [
     path("free-residence", free_residence_list),
     path("booking", booking),
]
