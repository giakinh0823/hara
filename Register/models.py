from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.template.defaultfilters import slugify
from django.urls import reverse


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birthday = models.DateTimeField()
    address = models.CharField(max_length=2000)
    certificate = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=20)
    image = models.ImageField(upload_to='profile', blank=True, null=True)
    slug = models.SlugField(max_length=2000, null=False)

    def get_absolute_url(self):
        return reverse('register:profile', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = slugify(self.user.username)
        return super().save(*args, **kwargs)
