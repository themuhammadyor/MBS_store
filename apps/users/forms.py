from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.exceptions import ValidationError

from .models import User, Feedback, UserCard


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Username', max_length=254)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2', 'avatar')

    def save(self, commit=True):
        user = super().save(commit=True)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password', 'avatar')


class FeedbackCreateForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ('body',)


class FeedbackUpdateForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ('body',)


class UserCardCreateForm(forms.ModelForm):
    password1 = forms.CharField(max_length=28)
    password2 = forms.CharField(max_length=28)

    def save(self, commit=True):
        user_card = super().save(commit=True)
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 == password2:
            user_card.set_password(password1)
            user_card.save()
        else:
            raise ValidationError('Password must be match!')

    class Meta:
        model = UserCard
        fields = ('card', 'color', 'password1', 'password2', 'code')


class UserCardUpdateForm(forms.ModelForm):
    password1 = forms.CharField(max_length=28)
    password2 = forms.CharField(max_length=28)

    def save(self, commit=True):
        user_card = super().save(commit=True)
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 == password2:
            user_card.set_password(password1)
            user_card.save()
        else:
            raise ValidationError('Password must be match!')

    class Meta:
        model = UserCard
        fields = ('card', 'color', 'password1', 'password2', 'code')
