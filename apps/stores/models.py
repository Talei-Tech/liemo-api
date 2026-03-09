from django.db import models
from django.utils.text import slugify
from apps.users.models import User
from apps.categories.models import Category


class Store(models.Model):
    class Status(models.TextChoices):
        ACTIVE = 'ACTIVE', 'Active'
        PENDING = 'PENDING', 'Pending'
        SUSPENDED = 'SUSPENDED', 'Suspended'

    admin = models.OneToOneField(User, on_delete=models.CASCADE, related_name='store')
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    bio = models.TextField(blank=True)
    logo_url = models.URLField(blank=True)
    is_verified = models.BooleanField(default=False)
    is_live = models.BooleanField(default=False)
    avg_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    categories = models.ManyToManyField(Category, blank=True, related_name='stores')
    follower_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'stores'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class StoreLink(models.Model):
    class Platform(models.TextChoices):
        TIKTOK = 'TIKTOK', 'TikTok'
        FACEBOOK = 'FACEBOOK', 'Facebook'
        INSTAGRAM = 'INSTAGRAM', 'Instagram'
        SHOPEE = 'SHOPEE', 'Shopee'
        YOUTUBE = 'YOUTUBE', 'YouTube'
        TWITTER = 'TWITTER', 'Twitter/X'
        WEBSITE = 'WEBSITE', 'Website'

    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='links')
    platform = models.CharField(max_length=20, choices=Platform.choices)
    url = models.URLField()
    label = models.CharField(max_length=100, blank=True)
    click_count = models.PositiveIntegerField(default=0)
    display_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'store_links'
        ordering = ['display_order']

    def __str__(self):
        return f'{self.store.name} - {self.platform}'
