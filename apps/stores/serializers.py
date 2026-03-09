from rest_framework import serializers
from .models import Store, StoreLink
from apps.categories.serializers import CategorySerializer


class StoreLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreLink
        fields = ['id', 'platform', 'url', 'label', 'click_count', 'display_order']
        read_only_fields = ['id', 'click_count']


class StoreSerializer(serializers.ModelSerializer):
    links = StoreLinkSerializer(many=True, read_only=True)
    categories = CategorySerializer(many=True, read_only=True)
    category_ids = serializers.PrimaryKeyRelatedField(
        many=True, write_only=True,
        queryset=__import__('apps.categories.models', fromlist=['Category']).Category.objects.all(),
        source='categories'
    )

    class Meta:
        model = Store
        fields = [
            'id', 'name', 'slug', 'bio', 'logo_url',
            'is_verified', 'is_live', 'avg_rating', 'status',
            'categories', 'category_ids', 'links',
            'follower_count', 'created_at'
        ]
        read_only_fields = ['id', 'slug', 'is_verified', 'avg_rating', 'follower_count', 'created_at']


class StoreCreateSerializer(serializers.ModelSerializer):
    category_ids = serializers.PrimaryKeyRelatedField(
        many=True, write_only=True,
        queryset=__import__('apps.categories.models', fromlist=['Category']).Category.objects.all(),
        source='categories',
        required=False
    )

    class Meta:
        model = Store
        fields = ['name', 'bio', 'logo_url', 'category_ids']

    def create(self, validated_data):
        categories = validated_data.pop('categories', [])
        store = Store.objects.create(**validated_data)
        if categories:
            store.categories.set(categories)
        return store
