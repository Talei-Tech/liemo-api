from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StoreViewSet, StoreLinkViewSet

router = DefaultRouter()
router.register(r'', StoreViewSet, basename='store')
router.register(r'links', StoreLinkViewSet, basename='store-link')

urlpatterns = [
    path('', include(router.urls)),
]
