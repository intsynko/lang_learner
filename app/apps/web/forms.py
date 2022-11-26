from django import forms

from apps.dictionary import models as dict_models


class DictionaryForm(forms.ModelForm):
    class Meta:
        model = dict_models.Dictionary
        fields = ("id", "name", "language_from", "language_to", "level", "tags", "is_public")


class WordForm(forms.ModelForm):
    word_from = forms.CharField(initial="")
    word_to = forms.CharField(initial="")

    class Meta:
        model = dict_models.Words
        fields = ("id", "word_from", "word_to")
