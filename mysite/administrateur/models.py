from django.db import models

class Title(models.Model):
    name = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.name

class ExpertiseField(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name