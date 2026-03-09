from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from drf_spectacular.utils import extend_schema
from .models import Store, StoreLink
from .serializers import StoreSerializer, StoreCreateSerializer, StoreLinkSerializer


@extend_schema(tags=['Stores'])
class StoreViewSet(viewsets.ModelViewSet):
    queryset = Store.objects.filter(status='ACTIVE').prefetch_related('links', 'categories')
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'create':
            return StoreCreateSerializer
        return StoreSerializer

    def perform_create(self, serializer):
        serializer.save(admin=self.request.user, status='ACTIVE')

    @extend_schema(tags=['Stores'])
    @action(detail=True, methods=['patch'], url_path='live-status')
    def live_status(self, request, pk=None):
        store = self.get_object()
        if store.admin != request.user:
            return Response({'error': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
        is_live = request.data.get('is_live', False)
        store.is_live = is_live
        store.save(update_fields=['is_live'])
        return Response({'is_live': store.is_live})


@extend_schema(tags=['Store Links'])
class StoreLinkViewSet(viewsets.ModelViewSet):
    serializer_class = StoreLinkSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return StoreLink.objects.filter(store__admin=self.request.user)

    def perform_create(self, serializer):
        store = Store.objects.get(admin=self.request.user)
        serializer.save(store=store)
