from django.db import models
from django.contrib.auth import models


# Create your models here.
class User(models.User, models.PermissionsMixin):
    """
    PermissionsMixin is a Django mixin class used to add permissions-related functionality to a model,
    typically a user model.
    It is a mixin class provided by Django that adds methods and fields for handling user permissions
    """

    def __str__(self):
        # username is an inbuilt attribute in django's user
        return f"@{self.username}"
