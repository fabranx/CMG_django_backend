from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    image = models.ImageField(default='default.jpg', upload_to='profile_pics', blank=True)


# class Profile(models.Model):
#     user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
#     image = models.ImageField(default='default.jpg', upload_to='profile_pics')
#     def __str__(self):
#         return f'{self.user.username} Profile'
