import datetime
from itertools import groupby

from django.db.models import Count
from django.utils import timezone
from django.views.generic import TemplateView

from apps.achievements.models import Attempt
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
        if self.request.user.is_authenticated:
            attempts = Attempt.objects.filter(
                user=self.request.user,
                date__gte=timezone.now() - datetime.timedelta(days=30)
            ).values(
                'dictionary_id', 'dictionary__name', 'date'
            ).annotate(
                amount=Count('date')
            ).order_by('dictionary_id', 'date')
            context['progress'] = []
            for dict_id, attempts in groupby(attempts, key=lambda x: x['dictionary_id']):
                attempts = list(attempts)
                data = {
                    "dictionary_id": dict_id,
                    "dictionary__name": attempts[0]["dictionary__name"],
                    "attempts": attempts,
                    "amount": sum([attempt['amount'] for attempt in attempts])
                }
                context['progress'].append(data)
        context.update({'q': kwargs})
        return context

    def get(self, request, *args, **kwargs):
        params = dict(self.request.GET.items())
        params['tags'] = self.request.GET.getlist('tags')
        return super().get(request, *args, **kwargs, **params)
