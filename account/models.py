from django.db import models
from django.contrib.auth.models import User

class MemberEmail(models.Model):
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.email