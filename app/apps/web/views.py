from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
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
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        search = self.request.POST.get('search', None)
        return super().get(request, *args, **kwargs, search=search)


class LoginPage(auth_views.LoginView):
    redirect_authenticated_user = True
    template_name = "web/login_page.html"


class DictionaryDetailSerializer(DictionarySerializer):
    owner = serializers.CharField(source='owner.username')
    rates_count = serializers.IntegerField(source='rates_cnt')
    date = serializers.DateField(source='date_created')
    pinned = serializers.SerializerMethodField()

    def get_pinned(self, obj):
        return obj.pinned.filter(id=self.context['request'].user.id).exists()


class DictionaryPage(TemplateView):
    template_name = "web/dictionary_page.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            dict = dict_models.Dictionary.queryset_wit_rating().get(id=kwargs['id'])
        except dict_models.Dictionary.DoesNotExist:
            raise Http404()
        context['dictionary'] = DictionaryDetailSerializer(instance=dict, context={"request": kwargs['request']}).data
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs, request=request)
        return self.render_to_response(context)


class DictionaryPin(DictionaryPage):

    @method_decorator(csrf_protect)
    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        id = kwargs['id']
        try:
            dict = dict_models.Dictionary.queryset_wit_rating().get(id=id)
        except dict_models.Dictionary.DoesNotExist:
            raise Http404()
        dict.pinned.add(request.user)
        dict.save()
        return redirect(f'/dictionary/{id}/')
        # return super().post(request, *args, **kwargs)
