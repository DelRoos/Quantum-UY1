# Generated by Django 5.1.3 on 2024-11-26 19:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='newsletter',
            options={'ordering': ['-date_joined'], 'verbose_name': 'Abonné newsletter', 'verbose_name_plural': 'Abonnés newsletter'},
        ),
        migrations.AddField(
            model_name='newsletter',
            name='name',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Nom'),
        ),
        migrations.AlterField(
            model_name='newsletter',
            name='email',
            field=models.EmailField(max_length=254, unique=True, verbose_name='Email'),
        ),
    ]