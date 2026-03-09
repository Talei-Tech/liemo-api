from rest_framework import serializers
from .models import Store, StoreLink
from apps.categories.serializers import CategorySerializer


class StoreLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreLink
        fields = ['id', 'platform', 'url', 'label', 'click_count', 'display_order']
        read_only_fields = ['click_count']


class StoreSerializer(serializers.ModelSerializer):
    links = StoreLinkSerializer(many=True, read_only=True)
    categories = CategorySerializer(many=True, read_only=True)

    class Meta:
        model = Store
        fields = [
            'id', 'name', 'slug', 'bio', 'logo_url',
            'is_verified', 'is_live', 'avg_rating', 'status',
            'follower_count', 'categories', 'links', 'created_at'
        ]
        read_only_fields = ['slug', 'avg_rating', 'follower_count', 'is_verified']


class StoreCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ['name', 'bio', 'logo_url']

    def create(self, validated_data):
        from django.utils.text import slugify
        import uuid
        name = validated_data['name']
        slug = slugify(name)
        # Ensure unique slug
        if Store.objects.filter(slug=slug).exists():
            slug = f'{slug}-{str(uuid.uuid4())[:8]}'
        validated_data['slug'] = slug
        validated_data['admin'] = self.context['request'].user
        return Store.objects.create(**validated_data)
