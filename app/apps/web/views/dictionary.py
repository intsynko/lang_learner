from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseForbidden
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.views.generic import TemplateView

from apps.dictionary import models as dict_models
from apps.web.forms import DictionaryForm, WordForm
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
        return redirect(request.POST.get("path") or "/")


class DictionaryUnpin(DictionaryDetailPage):

    @method_decorator(csrf_protect)
    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        id = kwargs['id']
        try:
            dict = dict_models.Dictionary.queryset_wit_rating().get(id=id)
        except dict_models.Dictionary.DoesNotExist:
            raise Http404()
        dict.pinned.remove(request.user)
        dict.save()
        return redirect(request.POST.get("path") or "/")


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


def word_template(reqeust):
    return render(reqeust, "web/components/word.html", context={"form": WordForm()})


class DictionaryCreatePage(TemplateView):
    template_name = "web/dictionary_create_page.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['form'] = DictionaryForm()
        context['languages'] = [LanguageSerizlizer(instance=lang).data for lang in dict_models.Language.objects.all()]
        context['levels'] = [LevelSerizlizer(instance=level).data for level in dict_models.Level.objects.all()]
        context['tags'] = [TagSerizlizer(instance=tag).data for tag in dict_models.Tag.objects.all()]
        return context

    @method_decorator(csrf_protect)
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs, request=request)
        return self.render_to_response(context)

    @method_decorator(csrf_protect)
    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        form = DictionaryForm(request.POST)
        if form.is_valid():
            dict = form.save(commit=False)
            dict.owner = request.user
            dict.save()
            return redirect(f'/dictionary/{form.instance.id}/')

        context = self.get_context_data(**kwargs, request=request)
        context["form"] = form
        return render(request, self.template_name, context)


class DictionaryUpdatePage(DictionaryCreatePage):

    @method_decorator(csrf_protect)
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        try:
            dict = dict_models.Dictionary.active().get(id=int(kwargs['id']))
        except dict_models.Dictionary.DoesNotExist:
            raise Http404()
        context = self.get_context_data(**kwargs, request=request)
        context['form'] = DictionaryForm(instance=dict)
        context['dict_id'] = dict.id
        return self.render_to_response(context)


class DictionaryRemovePage(DictionaryCreatePage):

    @method_decorator(csrf_protect)
    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        try:
            dict = dict_models.Dictionary.active().get(id=int(kwargs['id']))
        except dict_models.Dictionary.DoesNotExist:
            raise Http404()
        if not dict.owner == request.user:
            return HttpResponseForbidden()
        dict.is_active = False
        dict.save()
        return redirect(request.POST.get("path") or "/")
