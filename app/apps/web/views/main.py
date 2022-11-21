from django.views.generic import TemplateView

from apps.dictionary import models as dict_models
from apps.web.serializers import DictionarySerializer, LanguageSerizlizer, LevelSerizlizer, \
    TagSerizlizer


class MainPage(TemplateView):
    template_name = "web/main_page.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        dicts = dict_models.Dictionary.get_top(**kwargs, amount=10)
        context['dictionaries'] = [DictionarySerializer(instance=dict).data for dict in dicts]
        context['languages'] = [LanguageSerizlizer(instance=lang).data for lang in dict_models.Language.objects.all()]
        context['levels'] = [LevelSerizlizer(instance=level).data for level in dict_models.Level.objects.all()]
        context['tags'] = [TagSerizlizer(instance=tag).data for tag in dict_models.Tag.objects.all()]
        context.update({'q': kwargs})
        return context

    def get(self, request, *args, **kwargs):
        params = dict(self.request.GET.items())
        params['tags'] = self.request.GET.getlist('tags')
        return super().get(request, *args, **kwargs, **params)
