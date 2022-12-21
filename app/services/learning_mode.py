import datetime
import json
import uuid
import random

from django.conf import settings
from django.core.cache import caches as caches

from apps.achievements import models as attempt_models
from apps.dictionary import models as dict_models


cache = caches['repeats']


class Answer:
    def __init__(self, word_id, type_, success):
        self.word_id = word_id
        self.type = type_
        self.success = success


class LearningModeService:
    CART = 'cart'
    CHOICES = 'choice'
    CHOICES_REVERSE = 'choice_reverse'
    WORD_BUILD = 'word_builder'
    WORD_WRITE = 'word_writer'
    TYPES = [CART, CHOICES, CHOICES_REVERSE, WORD_BUILD, WORD_WRITE]

    def __init__(self, timeout: int = settings.LEARNER_SESSION_TIMEOUT):
        self.default_timeout = timeout

    def init_session(self, request, dict_id):
        session = uuid.uuid4()
        words = dict_models.Words.objects.filter(dictionary__id=dict_id, active=True)
        dict_ = dict_models.Dictionary.objects.prefetch_related('learning_mods').get(pk=dict_id)
        init_data = {
            'user_id': request.user.is_authenticated and request.user.id or None,
            'dict_id': dict_id,
            'mods': [mode.code for mode in dict_.learning_mods.all()],
            'words': {
                word.id: {
                    'id': word.id,
                    'word_from': word.word_from,
                    'word_to': word.word_to,
                    'transcription': word.transcription,
                    'prononsiation': word.prononsiation and word.prononsiation.url or None,
                    'image': word.image and word.image.url or None,
                    'example_1': word.example_1,
                    'example_2': word.example_2,
                    'progress': {type_: None for type_ in self.TYPES},
                }
                for word in words
            },
            'answered': 0,
            'answers_count': dict_.session_count or (len(words) * 2)
        }
        cache.set(str(session), json.dumps(init_data), timeout=self.default_timeout)
        return session

    def next(self, request, session: str, answer: Answer = None):
        context = cache.get(session)
        context = json.loads(context)
        if answer and not context['words'][answer.word_id]['progress'][answer.type]:
            context['words'][answer.word_id]['progress'][answer.type] = answer.success
            if answer.success:
                context['answered'] += 1
            cache.set(session, json.dumps(context), timeout=self.default_timeout)
        if context['answered'] >= context['answers_count']:
            user = request.user.is_authenticated and request.user or None
            if user and user.id == context['user_id'] and context['answered'] > 0:
                attempt_models.Attempt.objects.create(user=user, dictionary_id=context['dict_id'])
            return {
                "type": "finish",
                "progress": 100,
                "last_attempts": user and user.attempts.filter(date__gte=datetime.date.today()) or [],
            }
        return self._next(context)

    def _next(self, context):
        words = [word for word in context['words'].values() if not all(word['progress'].values())]
        words = words or list(context['words'].values())
        # 10 попыток чтобы выбирать рандомное слово и взять для него след. режим
        for i in range(10):
            next_word = random.choice(words)
            default_form = {
                "progress": round(context['answered'] / context['answers_count'] * 100),
            }
            if not next_word['progress'][self.CART]:
                return {
                    **default_form,
                    "type": self.CART,
                    "word": next_word,
                }
            if self.CHOICES in context['mods'] and not next_word['progress'][self.CHOICES]:
                choices = [*[word['word_to']
                             for word in context['words'].values()
                             if word['id'] != next_word['id']][:3],
                           next_word['word_to']]
                random.shuffle(choices)
                return {
                    **default_form,
                    "type": self.CHOICES,
                    "word": next_word,
                    "choices": choices
                }
            elif self.CHOICES_REVERSE in context['mods'] and not next_word['progress'][self.CHOICES_REVERSE]:
                choices = [*[word['word_from']
                             for word in context['words'].values()
                             if word['id'] != next_word['id']][:3],
                           next_word['word_from']]
                random.shuffle(choices)
                return {
                    **default_form,
                    "type": self.CHOICES_REVERSE,
                    "word": next_word,
                    "choices": choices
                }
            if self.WORD_BUILD in context['mods'] and not next_word['progress'][self.WORD_BUILD]:
                symbols = list(next_word['word_from'])
                random.shuffle(symbols)
                return {
                    **default_form,
                    "type": self.WORD_BUILD,
                    "word": next_word,
                    "symbols": symbols,
                }
            if self.WORD_WRITE in context['mods'] and not next_word['progress'][self.WORD_WRITE]:
                return {
                    **default_form,
                    "type": self.WORD_WRITE,
                    "word": next_word,
                }
