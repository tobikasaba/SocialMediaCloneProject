from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from . import forms


# Create your views here.
class SignUp(CreateView):
    form_class = forms.UserCreateForm
    # after successful login, user is redirected to login page
    success_url = reverse_lazy('login')
    template_name = 'accounts/signup.html'
