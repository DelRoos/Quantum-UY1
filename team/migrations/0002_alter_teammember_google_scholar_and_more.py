# Generated by Django 5.1.3 on 2024-11-29 17:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('team', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teammember',
            name='google_scholar',
            field=models.URLField(blank=True, null=True, verbose_name='Google Scholar'),
        ),
        migrations.AlterField(
            model_name='teammember',
            name='linkedin',
            field=models.URLField(blank=True, null=True, verbose_name='LinkedIn'),
        ),
        migrations.AlterField(
            model_name='teammember',
            name='orcid',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='ORCID'),
        ),
        migrations.AlterField(
            model_name='teammember',
            name='researchgate',
            field=models.URLField(blank=True, null=True, verbose_name='ResearchGate'),
        ),
        migrations.AlterField(
            model_name='teammember',
            name='twitter',
            field=models.URLField(blank=True, null=True, verbose_name='Twitter'),
        ),
        migrations.AlterField(
            model_name='teammember',
            name='website',
            field=models.URLField(blank=True, null=True, verbose_name='Site web personnel'),
        ),
    ]