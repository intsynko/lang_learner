from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views
from rest_framework import serializers

from apps.dictionary import models as dict_models


class DictionarySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    lang = serializers.SerializerMethodField()
    lang_from = serializers.ImageField(source='language_from.icon')
    lang_to = serializers.ImageField(source='language_to.icon')
    level = serializers.CharField(source="level.name")
    tags = serializers.ListSerializer(child=serializers.CharField(source="name"))
    rating = serializers.SerializerMethodField()

    def get_lang(self, dictionary):
        return f"{dictionary.language_from.code.upper()}-{dictionary.language_to.code.upper()}"

    def get_rating(self, dictionary):
        return dictionary.average_rate or "-"


class MainPage(TemplateView):
    template_name = "web/main_page.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        dicts = dict_models.Dictionary.get_top(kwargs.get('search'), amount=10)
        context['dictionaries'] = [DictionarySerializer(instance=dict).data for dict in dicts]
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        search = self.request.POST.get('search', None)

        context = self.get_context_data(**kwargs, search=search)
        return self.render_to_response(context)


class LoginPage(auth_views.LoginView):
    redirect_authenticated_user = True
    template_name = "web/login_page.html"
