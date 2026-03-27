from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.text import slugify


class CustomUserCreationForm(UserCreationForm):
    """UserCreationForm with optional username field; if left blank, username will be generated from email."""
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'password1', 'password2')

    email = forms.EmailField(required=True)
    username = forms.CharField(required=False, max_length=150)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # ensure username field exists (optional)
        # apply Bootstrap widget classes and placeholders
        widgets = {
            'first_name': {'class': 'form-control form-control-lg', 'placeholder': 'First name'},
            'last_name': {'class': 'form-control form-control-lg', 'placeholder': 'Last name'},
            'email': {'class': 'form-control form-control-lg', 'placeholder': 'you@example.com', 'type': 'email'},
            'username': {'class': 'form-control form-control-lg', 'placeholder': 'Choose a username (optional)'},
            'password1': {'class': 'form-control form-control-lg', 'placeholder': '•••••••••'},
            'password2': {'class': 'form-control form-control-lg', 'placeholder': '•••••••••'},
        }
        for name, attrs in widgets.items():
            if name in self.fields:
                for k, v in attrs.items():
                    self.fields[name].widget.attrs[k] = v

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username:
            username = username.strip()
            if User.objects.filter(username=username).exists():
                raise forms.ValidationError('This username is already taken.')
        return username

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        # set email
        email = self.cleaned_data.get('email')
        user.email = email

        provided_username = (self.cleaned_data.get('username') or '').strip()
        if provided_username:
            username = provided_username
        else:
            # generate a username from email local-part or name
            base = slugify(email.split('@')[0]) if email else slugify((self.cleaned_data.get('first_name') or '') + '-' + (self.cleaned_data.get('last_name') or ''))
            if not base:
                base = 'user'
            username = base
            counter = 1
            while User.objects.filter(username=username).exists():
                username = f"{base}{counter}"
                counter += 1

        user.username = username

        if commit:
            user.save()
        return user
