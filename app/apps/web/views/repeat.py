from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseForbidden, HttpResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.views.generic import TemplateView

from apps.dictionary import models as dict_models
from apps.web.forms import WordForm


def word_template(reqeust, id):
    return render(reqeust, "web/components/word_creation.html", context={"form": WordForm({"dictionary": id, "id": 0})})


class RepeatPage(TemplateView):

    def get(self, request, *args, id, **kwargs):
        dict = dict_models.Dictionary.objects.filter(id=id).first()
        words = dict.words.all()
        word = words[0]
        return render(request, "web/learning_page.html", context={"form": {
            "type": "choices",
            "word": WordForm(instance=word),
            "choices": [word_.word_to for word_ in [*words.exclude(id=word.id)[:3], word]],
        }})

    def post(self, request, *args, **kwargs):
        word = dict_models.Words.objects.filter(id=request.POST.get('word')).first()
        success = request.POST.get('success') == 'true'
        # continue
