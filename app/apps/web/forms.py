from django import forms

from apps.dictionary import models as dict_models


class DictionaryForm(forms.ModelForm):
    id = forms.IntegerField()
    file = forms.ImageField()

    class Meta:
        model = dict_models.Dictionary
        fields = ("id", "name", "language_from", "language_to", "level", "tags", "is_public")


class WordForm(forms.ModelForm):
    id = forms.IntegerField(initial=0)
    word_from = forms.CharField(initial="")
    word_to = forms.CharField(initial="")
    example_1 = forms.CharField(initial="")
    example_2 = forms.CharField(initial="")

    class Meta:
        model = dict_models.Words
        fields = ("id", "dictionary", "word_from", "word_to", "example_1", "example_2", "image")


class RepeatForm(forms.Form):
    word = forms.IntegerField()
    success = forms.BooleanField()