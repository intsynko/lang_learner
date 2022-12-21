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


class WordCreatePage(TemplateView):

    @method_decorator(csrf_protect)
    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        instance = dict_models.Words.objects.filter(id=request.POST.get('id')).first()
        if instance and instance.dictionary.owner != request.user:
            return HttpResponseForbidden()
        form = WordForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            word = form.save(commit=False)
            if not word.prononsiation:
                word.load_prononsiation()
            word.save()
            #return render(request, "web/components/word.html", context={"form": form})
        return render(request, "web/components/word_creation.html", context={"form": form})


class WordDeletePage(TemplateView):

    @method_decorator(csrf_protect)
    @method_decorator(login_required)
    def post(self, request, *args, id, **kwargs):
        try:
            word = dict_models.Words.objects.get(id=id)
        except dict_models.Words.DoesNotExist:
            raise Http404()
        if word.dictionary.owner != request.user:
            return HttpResponseForbidden()
        word.active = False
        word.save()
        return HttpResponse()
