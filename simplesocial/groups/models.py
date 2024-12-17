from django.db import models
from django.urls import reverse
from django.utils.text import slugify

# allows link embedding
import misaka

# Create your models here.
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

from django import template

# enables you to use custom templates tags
register = template.Library()


class Group(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(allow_unicode=True, unique=True)
    # this field can be left blank
    description = models.TextField(blank=True, default='')
    description_html = models.TextField(editable=False, default='', blank=True)
    members = models.ManyToManyField(User, through='GroupMember')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        self.description_html = misaka.html(self.description)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('groups:single', kwargs={'slug': self.slug})

    class Meta:
        ordering = ['name']


class GroupMember(models.Model):
    group = models.ForeignKey(Group, related_name='memberships', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='user_groups', on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

    class Meta:
        unique_together = ('group', 'user')
