from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomizeUser(AbstractUser):
    last_updated = models.DateTimeField(auto_now=True)
    avatar = models.ImageField(null=True, blank=True, upload_to='images/')

    @property
    def avatar_url(self):
        if self.avatar and hasattr(self.avatar, 'url'):
            return self.avatar.url
        else:
            return 'media/images/th.jfif'


class PasswordSafe(models.Model):
    site_name = models.CharField(max_length=255)
    site = models.URLField()
    user = models.ForeignKey(CustomizeUser, on_delete=models.CASCADE)
    email = models.EmailField(max_length=255)
    password = models.CharField(max_length=50)

    def __str__(self):
        return self.site_name