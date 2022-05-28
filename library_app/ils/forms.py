from django.contrib.auth.forms import AuthenticationForm
from django import forms

# Adding widgets to style Django built-in login and authentication form
class CustomLoginForm(AuthenticationForm):

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.fields['username'].widget.attrs.update(
      {'class': 'w-username form-control', 'placeholder': 'Username'}
    )
    self.fields['password'].widget.attrs.update(
      {'class': 'w-password form-control', 'placeholder': 'Password'}
    )

