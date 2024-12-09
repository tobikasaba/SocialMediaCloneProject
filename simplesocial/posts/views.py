from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic
from django.http import Http404
from braces.views import SelectRelatedMixin
from . import models
from . import forms
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your views here.

"""
Difference between user__username__iexact and username__iexact:
username__iexact: Directly filters the model (User) with the username field (e.g., User).
user__username__iexact: Filters a model (e.g., Post) based on the username of its related User model.

Use user__username__iexact when you want to reference a related model (User) through a ForeignKey. 
Use username__iexact when you're working with the model that directly has the username field.

**The user in user__username__iexact represents the field name for the ForeignKey in the Post model,
and by referencing it, you are querying the related model (the inbuilt User model in this case)
which has an inbuilt username field
"""


class PostList(SelectRelatedMixin, generic.ListView):
    """
    The SelectRelatedMixin is a mixin used in Django to optimise database queries when retrieving objects that have
    related fields.
    It works in conjunction with Django's select_related query optimisation
    to reduce the number of database queries for related models.

    select_related: Allows Django to fetch related objects in a single query using an SQL JOIN.
    This greatly improves performance for queries involving related models.
    It prevents the n+1 problem.


    """
    model = models.Post
    # select_related specifies the related fields to optimise
    select_related = ('user', 'group')


class UserPosts(generic.ListView):
    model = models.Post
    template_name = 'posts/user_post_list.html'

    def get_queryset(self):
        """
        get_queryset decides which posts (or objects) the page should display.
        Normally, a ListView automatically shows all the objects of the Post model, but here, we're customising it.
        """
        try:
            """
            This line finds a User in the database whose username matches the username
            in the URL (self.kwargs.get('username') gets that value).
            
            User.objects: This accesses the query manager for the User model, which allows performing database queries
            
            prefetch_related('posts') makes it more efficient by pre-loading all the posts connected to that user
            in one go, instead of fetching them one by one later.
            
            get(): Retrieves a single object from the database based on the given query parameters.
            
            username__iexact: is a case-insensitive lookup for the username field. For example:
            If username in the database is JohnDoe, this query will match johndoe, JOHNDOE, or any other case variation
            
            self.kwargs.get('username'): retrieves the value of the username parameter from the kwargs dictionary, 
            which contains URL parameters passed to the view. For example, if the URL is:
            
            post_user is is created and assigned explicitly here
            """
            self.post_user = User.objects.prefetch_related('posts').get(
                username__iexact=self.kwargs.get('username'))
        except User.DoesNotExist:
            # If no user is found with that username, the code raises a Http404 error, which means "page not found."
            raise Http404
        else:
            # If the user exists, it fetches all the posts by that user. These are what will be displayed on the page
            return self.post_user.posts.all()

    def get_context_data(self, **kwargs):
        """
        get_context_data: is used to add extra context (data) to the template in
        addition to what is already provided by default in this case, a ListView.

        super().get_context_data(**kwargs): This retrieves the default context data provided by the ListView.
        Without this, the default data (like the list of posts) wouldn’t be passed to the template.


        context['post_user'] = self.post_user: This assigns the user object to a variable in the template context.
        """
        context = super().get_context_data(**kwargs)
        context['post_user'] = self.post_user
        return context


class PostDetail(SelectRelatedMixin, generic.DetailView):
    model = models.Post
    select_related = ('user', 'group')

    def get_queryset(self):
        # returns the default queryset for this view i.e. all posts
        queryset = super().get_queryset()
        return queryset.filter(user__username__iexact=self.kwargs.get('username'))


class CreatePost(LoginRequiredMixin, SelectRelatedMixin, generic.CreateView):
    fields = ('message', 'group')
    model = models.Post

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)


class DeletePost(LoginRequiredMixin, SelectRelatedMixin, generic.DeleteView):
    model = models.Post
    select_related = ('user', 'group')
    success_url = reverse_lazy('posts:all')

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user_id=self.request.user.id)

    def delete(self, *args, **kwargs):
        messages.success(self.request, "Post Deleted")
        return super().delete(*args, **kwargs)
