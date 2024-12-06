from django.db import models
from django.conf import settings
from administrateur.models import Title, ExpertiseField


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        default=1 
    )
    expertise = models.ManyToManyField(ExpertiseField)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(
        upload_to='users/%Y/%m/%d/',
        blank=True
    )

    def __str__(self):
        return f'Profile of {self.user.username}'