from django.db import models
from django.contrib.auth.models import User
from PIL import Image


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    class Meta:
        verbose_name_plural = 'Профили'

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        super().save()

        userpic = Image.open(self.image.path)

        if userpic.height > 300 or userpic.width > 300:
            output_size = (300, 300)
            userpic.thumbnail(output_size)
            userpic.save(self.image.path)
