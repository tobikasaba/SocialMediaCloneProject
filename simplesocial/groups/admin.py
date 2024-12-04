from django.contrib import admin
from . import models


# Register your models here.

class GroupMemberInline(admin.TabularInline):
    """
    admin.TabularInline is a subclass of admin.InlineModelAdmin in Django's admin interface

    It is used to define inline editing for a model related to another model
    through a foreign key or many-to-many relationship.

    It allows you to edit related objects (e.g., GroupMember) directly within
    the parent object's (e.g., Group) admin page in the admin site.
    ------------------------------------------------------------------
    It provides inline editing capabilities for the GroupMember model within
    the Django admin interface using a tabular layout.

    This class is used to facilitate the management of GroupMember instances
    directly from the parent model's page in the admin site, allowing for a more
    streamlined user experience when dealing with related data entries.

    :ivar model: Specifies the model class that this inline administers.
    :type model: models.GroupMember
    """
    model = models.GroupMember


admin.site.register(models.Group)
