from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import CharField, ModelForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, ButtonHolder, Submit, Div
from .models import Author


class RegisterUserForm(UserCreationForm):
    username = CharField(required=True, label="Email")

    class Meta:
        model = User
        fields = ("username", "password1", "password2")


class AuthorForm(ModelForm):

    class Meta:
        model = Author
        fields = ["first_name", "last_name"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                Div("first_name", css_class="col"),
                Div("last_name", css_class="col"),
                css_class="col-lg-3",
            ),
            ButtonHolder(
                Submit('submit', 'Create', css_class='button')
            )
        )
