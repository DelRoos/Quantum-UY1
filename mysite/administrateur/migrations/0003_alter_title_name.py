# Generated by Django 5.0.9 on 2024-12-02 01:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administrateur', '0002_rename_titre_title_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='title',
            name='name',
            field=models.CharField(max_length=100, null=True),
        ),
    ]