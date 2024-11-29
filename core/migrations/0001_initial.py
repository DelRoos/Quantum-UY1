# Generated by Django 5.1.3 on 2024-11-26 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('subject', models.CharField(max_length=200)),
                ('message', models.TextField()),
                ('date_sent', models.DateTimeField(auto_now_add=True)),
                ('is_read', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Newsletter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='SiteConfig',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('site_name', models.CharField(default='Quantum UY1', max_length=100)),
                ('site_description', models.TextField(default='Laboratoire de Recherche en Physique Quantique')),
                ('contact_email', models.EmailField(default='contact@quantum-uy1.com', max_length=254)),
                ('address', models.TextField(blank=True)),
                ('phone', models.CharField(blank=True, max_length=20)),
                ('twitter_url', models.URLField(blank=True)),
                ('linkedin_url', models.URLField(blank=True)),
                ('researchgate_url', models.URLField(blank=True)),
            ],
            options={
                'verbose_name': 'Configuration du site',
                'verbose_name_plural': 'Configuration du site',
            },
        ),
    ]
