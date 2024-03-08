# Generated by Django 3.2.25 on 2024-03-08 10:36

import autoslug.fields
import cloudinary.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import worksifly.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='SecurityFeature',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from='title', unique=True)),
                ('created_on', models.DateTimeField(auto_now=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('preparation_time', models.IntegerField(default=0)),
                ('cook_time', models.IntegerField(default=0)),
                ('description', models.TextField()),
                ('ingredients', models.TextField(validators=[worksifly.validators.textfield_not_empty])),
                ('method', models.TextField(validators=[worksifly.validators.textfield_not_empty])),
                ('image', cloudinary.models.CloudinaryField(default='placeholder', max_length=255, verbose_name='image')),
                ('status', models.IntegerField(choices=[(0, 'Save for later'), (1, 'Publish Now')], default=1)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='security_features', to=settings.AUTH_USER_MODEL)),
                ('bookmarks', models.ManyToManyField(blank=True, related_name='bookmarks', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_on'],
            },
        ),
        migrations.CreateModel(
            name='TechSecurItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.IntegerField(choices=[(0, 'Monday'), (1, 'Tuesday'), (2, 'Wednesday'), (3, 'Thursday'), (4, 'Friday'), (5, 'Saturday'), (6, 'Sunday')], default=0)),
                ('security_feature', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tech_secur_items', to='worksifly.securityfeature')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tech_securs', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['day'],
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.TextField()),
                ('created_on', models.DateTimeField(auto_now=True)),
                ('security_feature', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='worksifly.securityfeature')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['created_on'],
            },
        ),
    ]
