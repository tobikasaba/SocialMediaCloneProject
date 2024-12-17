from django.db import models
from django.urls import reverse
from django.conf import settings
import misaka
from groups.models import Group
from django.contrib.auth import get_user_model

"""
get_user_model is a utility function provided by Django to retrieve the currently
active user model in your project.
It dynamically fetches the user model being used in your Django project.
Doing this all
It can also used in situations where you want to reference the user model but do not want to directly rely on
Django's default auth.User model.
This function ensures compatibility with custom user models.
This allows the User model to be used as a Foreign Key field in the models present.
"""
User = get_user_model()


# Create your models here.

class Post(models.Model):
    user = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    message = models.TextField()
    message_html = models.TextField(editable=False)
    group = models.ForeignKey(Group, related_name='posts', null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.message

    def save(self, *args, **kwargs):
        self.message_html = misaka.html(self.message)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('posts:single', kwargs={'username': self.user.username, 'pk': self.pk})

    class Meta:
        ordering = ['-created_at']
        unique_together = ['user', 'message']
