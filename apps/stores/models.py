from django.db import models
from apps.users.models import User
from apps.categories.models import Category


class StoreStatus(models.TextChoices):
    ACTIVE = 'ACTIVE', 'Active'
    PENDING = 'PENDING', 'Pending'
    SUSPENDED = 'SUSPENDED', 'Suspended'


class Platform(models.TextChoices):
    TIKTOK = 'TIKTOK', 'TikTok'
    FACEBOOK = 'FACEBOOK', 'Facebook'
    INSTAGRAM = 'INSTAGRAM', 'Instagram'
    SHOPEE = 'SHOPEE', 'Shopee'
    YOUTUBE = 'YOUTUBE', 'YouTube'
    TWITTER = 'TWITTER', 'Twitter/X'
    WEBSITE = 'WEBSITE', 'Website'
    OTHER = 'OTHER', 'Other'


class Store(models.Model):
    admin = models.OneToOneField(User, on_delete=models.CASCADE, related_name='store')
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    bio = models.TextField(blank=True)
    logo_url = models.URLField(blank=True)
    is_verified = models.BooleanField(default=False)
    is_live = models.BooleanField(default=False)
    avg_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    status = models.CharField(max_length=20, choices=StoreStatus.choices, default=StoreStatus.PENDING)
    categories = models.ManyToManyField(Category, through='StoreCategory', blank=True)
    follower_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'stores'
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class StoreCategory(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        db_table = 'store_categories'
        unique_together = ['store', 'category']


class StoreLink(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='links')
    platform = models.CharField(max_length=20, choices=Platform.choices)
    url = models.URLField()
    label = models.CharField(max_length=100, blank=True)
    click_count = models.PositiveIntegerField(default=0)
    display_order = models.PositiveSmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'store_links'
        ordering = ['display_order']

    def __str__(self):
        return f'{self.store.name} - {self.platform}'
