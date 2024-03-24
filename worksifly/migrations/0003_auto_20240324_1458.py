# Generated by Django 3.2.25 on 2024-03-24 14:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('worksifly', '0002_auto_20240324_1418'),
    ]

    operations = [
        migrations.RenameField(
            model_name='securityfeature',
            old_name='serch_time',
            new_name='search_time',
        ),
        migrations.AddField(
            model_name='securityfeature',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='securityfeature_like', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='securityfeature',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='securityfeatures', to=settings.AUTH_USER_MODEL),
        ),
    ]