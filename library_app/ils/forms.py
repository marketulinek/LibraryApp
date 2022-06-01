from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import CharField

class RegisterUserForm(UserCreationForm):
    username = CharField(required=True, label="Email")

    class Meta:
        model = User
        fields = ("username", "password1", "password2")
        # fields = ("first_name", "last_name", "username", "password1", "password2")
