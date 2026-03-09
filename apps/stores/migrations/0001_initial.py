from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('categories', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Store',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('slug', models.SlugField(unique=True)),
                ('bio', models.TextField(blank=True)),
                ('logo_url', models.URLField(blank=True)),
                ('is_verified', models.BooleanField(default=False)),
                ('is_live', models.BooleanField(default=False)),
                ('avg_rating', models.DecimalField(decimal_places=2, default=0.0, max_digits=3)),
                ('status', models.CharField(choices=[('ACTIVE', 'Active'), ('PENDING', 'Pending'), ('SUSPENDED', 'Suspended')], default='PENDING', max_length=20)),
                ('follower_count', models.PositiveIntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('admin', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='store', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'stores',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='StoreCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stores.store')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='categories.category')),
            ],
            options={
                'db_table': 'store_categories',
                'unique_together': {('store', 'category')},
            },
        ),
        migrations.AddField(
            model_name='store',
            name='categories',
            field=models.ManyToManyField(blank=True, through='stores.StoreCategory', to='categories.category'),
        ),
        migrations.CreateModel(
            name='StoreLink',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('platform', models.CharField(choices=[('TIKTOK', 'TikTok'), ('FACEBOOK', 'Facebook'), ('INSTAGRAM', 'Instagram'), ('SHOPEE', 'Shopee'), ('YOUTUBE', 'YouTube'), ('TWITTER', 'Twitter/X'), ('WEBSITE', 'Website'), ('OTHER', 'Other')], max_length=20)),
                ('url', models.URLField()),
                ('label', models.CharField(blank=True, max_length=100)),
                ('click_count', models.PositiveIntegerField(default=0)),
                ('display_order', models.PositiveSmallIntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='links', to='stores.store')),
            ],
            options={
                'db_table': 'store_links',
                'ordering': ['display_order'],
            },
        ),
    ]
