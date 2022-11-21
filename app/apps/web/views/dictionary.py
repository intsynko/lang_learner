from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.views.generic import TemplateView

from apps.dictionary import models as dict_models
from apps.web.serializers import DictionaryDetailSerializer, LanguageSerizlizer, LevelSerizlizer, \
    TagSerizlizer


class DictionaryDetailPage(TemplateView):
    template_name = "web/dictionary_detail_page.html"

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


class DictionaryPin(DictionaryDetailPage):

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


class DictionaryPage(TemplateView):
    template_name = "web/dictionary_page.html"

    @method_decorator(csrf_protect)
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs, request=request)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dicts = dict_models.Dictionary.my(user=kwargs['request'].user)
        context['dictionaries'] = [
            DictionaryDetailSerializer(instance=dict, context={"request": kwargs['request']}).data
            for dict in dicts
        ]
        return context


class DictionaryCreatePage(TemplateView):
    template_name = "web/dictionary_create_page.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['languages'] = [LanguageSerizlizer(instance=lang).data for lang in dict_models.Language.objects.all()]
        context['levels'] = [LevelSerizlizer(instance=level).data for level in dict_models.Level.objects.all()]
        context['tags'] = [TagSerizlizer(instance=tag).data for tag in dict_models.Tag.objects.all()]
        return context

    @method_decorator(csrf_protect)
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs, request=request)
        return self.render_to_response(context)
