from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from apps.account import models as account_models
from apps.dictionary import models as dict_models


class RegistrationForm(forms.Form):
    email = forms.EmailField(initial="")
    username = forms.CharField(initial="")
    password = forms.CharField(min_length=4, max_length=30)
    password_repeat = forms.CharField(min_length=4, max_length=30)

    def clean_email(self):
        email = self.data['email']
        if account_models.User.objects.filter(email=email).exists():
            raise ValidationError(_("User with same email already exists"))
        return email

    def clean_username(self):
        username = self.data['username']
        if account_models.User.objects.filter(username=username).exists():
            raise ValidationError(_("User with same username already exists"))
        return username

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data["password"] != cleaned_data["password_repeat"]:
            self.errors["password_repeat"].append(_("Password and repeat password doesn't match"))
        return cleaned_data

    def save(self):
        return account_models.User.objects.create(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password'],
        )


class DictionaryForm(forms.ModelForm):
    id = forms.IntegerField(required=False)

    class Meta:
        model = dict_models.Dictionary
        fields = ("id", "name", "language_from", "language_to", "level", "tags",
                  "is_public", "session_count", "learning_mods")


class WordForm(forms.ModelForm):
    id = forms.IntegerField(initial=0)
    word_from = forms.CharField(initial="")
    word_to = forms.CharField(initial="")
    example_1 = forms.CharField(initial="")
    example_2 = forms.CharField(initial="")

    class Meta:
        model = dict_models.Words
        fields = ("id", "dictionary", "word_from", "word_to", "example_1", "example_2", "image", "transcription")


class RepeatForm(forms.Form):
    word = forms.IntegerField()
    success = forms.BooleanField()
