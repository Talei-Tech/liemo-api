from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Store, StoreLink
from .serializers import StoreSerializer, StoreCreateSerializer, StoreLinkSerializer


class StoreViewSet(viewsets.ModelViewSet):
    queryset = Store.objects.filter(status='ACTIVE').select_related('admin').prefetch_related('links', 'categories')
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['is_live', 'status']
    search_fields = ['name', 'bio']
    ordering_fields = ['avg_rating', 'follower_count', 'created_at']
    lookup_field = 'slug'

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return StoreCreateSerializer
        return StoreSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy', 'toggle_live']:
            return [IsAuthenticated()]
        return [AllowAny()]

    @action(detail=True, methods=['patch'], permission_classes=[IsAuthenticated])
    def toggle_live(self, request, slug=None):
        """US-013: Toggle live status"""
        store = self.get_object()
        if store.admin != request.user:
            return Response({'error': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
        store.is_live = not store.is_live
        store.save()
        return Response({'is_live': store.is_live})


class StoreLinkViewSet(viewsets.ModelViewSet):
    """US-011: Manage store links"""
    serializer_class = StoreLinkSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return StoreLink.objects.filter(store__admin=self.request.user)

    def perform_create(self, serializer):
        store = self.request.user.store
        serializer.save(store=store)
