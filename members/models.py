from django.db import models

class Title(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class ExpertiseField(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Member(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    expertise = models.ManyToManyField(ExpertiseField)
    email = models.EmailField(unique=True) 
    password = models.CharField(max_length=128) 
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)

    def __str__(self):
        return f"{self.title.name} {self.first_name} {self.last_name}"

