from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import CharField, ModelForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, ButtonHolder, Submit, Div
from .models import Author, Book


class RegisterUserForm(UserCreationForm):
    username = CharField(required=True, label="Email")

    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "password1", "password2")

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.helper = FormHelper()
            self.helper.layout = Layout(
                Div(
                    Div("first_name", css_class="col-md-6"),
                    Div("last_name", css_class="col-md-6"),
                    Div("username", css_class="col-sm-6"),
                    Div("password1", css_class="col-md-6"),
                    Div("password1", css_class="col-md-6"),
                    css_class="row px-4"
                ),
                ButtonHolder(
                    Submit('submit', 'Submit', css_class='button'),
                    css_class="btn btn-primary ps-4"
                )
            )


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
                css_class="col-lg-3 px-4",
            ),
            ButtonHolder(
                Submit('submit', 'Create', css_class='button'),
                css_class="ps-4"
            )
        )

class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = ["name", "author", "publisher", "year", "status", "description"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                Div("name", css_class="col-md-6"),
                Div("author", css_class="col-sm-6"),
                Div("publisher", css_class="col-sm-6"),
                Div("year", css_class="col-6 col-md-3", placeholder="2000"),
                Div("status", css_class="col-6 col-md-3"),
                Div("description", css_class="col-12 col-md-8"),
                css_class="row px-4"
            ),
            ButtonHolder(
                Submit('submit', 'Create', css_class='button'),
                css_class="ps-4"
            )
        )

