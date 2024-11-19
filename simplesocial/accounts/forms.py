from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


class UserCreateForm(UserCreationForm):
    class Meta:
        fields = ('username', 'email', 'password1', 'password2')
        """
        get_user_model is a utility function provided by Django to retrieve the currently
        active user model in your project.
        It can also used in situations where you want to reference the user model but do not want to directly rely on
        Django's default auth.User model.
        This function ensures compatibility with custom user models.
        """
        model = get_user_model()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # setting the label names for the inbuilt fields
        self.fields['username'].label = 'Display Name'
        self.fields['email'].label = 'Email Address'
        self.fields['password1'].label = 'Password'
        self.fields['password2'].label = 'Confirm Password'
