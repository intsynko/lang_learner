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
    TYPES = ['choices', ]

    def __init__(self, timeout: int = settings.LEARNER_SESSION_TIMEOUT):
        self.default_timeout = timeout

    def init_session(self, request, dict_id):
        session = uuid.uuid4()
        words = dict_models.Words.objects.filter(dictionary__id=dict_id)
        init_data = {
            'user_id': request.user.is_authenticated and request.user.id or None,
            'dict_id': dict_id,
            'words': {
                word.id: {
                    'id': word.id,
                    'word_from': word.word_from,
                    'word_to': word.word_to,
                    'image': word.image and word.image.url or None,
                    'example_1': word.example_1,
                    'example_2': word.example_2,
                    'progress': {type_: None for type_ in self.TYPES},
                }
                for word in words
            },
            'answered': 0,
            'answers_count': len(words) * 2
        }
        cache.set(str(session), json.dumps(init_data), timeout=self.default_timeout)
        return session

    def next(self, request, session: str, answer: Answer = None):
        context = cache.get(session)
        context = json.loads(context)
        if answer:
            context['words'][answer.word_id]['progress'][answer.type] = answer.success
            context['answered'] += 1
            cache.set(session, json.dumps(context), timeout=self.default_timeout)
        if context['answered'] >= context['answers_count']:
            user = request.user.is_authenticated and request.user or None
            if user and user.id == context['user_id'] and context['answered'] > 0:
                attempt_models.Attempt.objects.create(user=user, dictionary_id=context['dict_id'])
            return {
                "type": "finish",
                 "progress": 100,
                "last_attempts": user and user.attempts.filter(date__gte=datetime.date.today()) or []
            }
        return self._next(context)

    def _next(self, context):
        words = [word for word in context['words'].values() if not all(word['progress'].values())]
        words = words or list(context['words'].values())
        next_word = random.choice(words)
        # if not next_word['progress']['choices']:
        choices = [*[word['word_to']
                     for word in context['words'].values()
                     if word['id'] != next_word['id']][:3],
                   next_word['word_to']]
        random.shuffle(choices)
        return {
            "progress": round(context['answered'] / context['answers_count'] * 100),
            "type": "choices",
            "word": next_word,
            "choices": choices
        }
