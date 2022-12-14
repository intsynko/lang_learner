import logging
import uuid

from django.utils.translation import gettext_lazy as _
from django.contrib.auth.decorators import login_required
from django.core.cache import caches
from django.http import Http404, HttpResponseForbidden
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.views.generic import TemplateView

from apps.dictionary import models as dict_models
from apps.web.forms import DictionaryForm, WordForm, DictUploadForm, DictSelectForm
from apps.web.serializers import DictionaryDetailSerializer, LanguageSerizlizer, LevelSerizlizer, \
    TagSerizlizer, LearningModeSerizlizer


logger = logging.getLogger(__name__)


class DictionaryDetailPage(TemplateView):
    template_name = "web/dictionary_detail_page.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            dict = dict_models.Dictionary.queryset_wit_rating().get(id=kwargs['id'])
        except dict_models.Dictionary.DoesNotExist:
            raise Http404()
        context['dictionary'] = DictionaryDetailSerializer(instance=dict, context={"request": kwargs['request']}).data
        context['words'] = [WordForm(instance=word) for word in dict.words.filter(active=True)]
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


class DictionaryCreatePage(TemplateView):
    template_name = "web/dictionary_create_page.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['form'] = DictionaryForm({"learning_mods": dict_models.LearningMode.objects.all()})
        context['languages'] = [LanguageSerizlizer(instance=lang).data for lang in dict_models.Language.objects.all()]
        context['levels'] = [LevelSerizlizer(instance=level).data for level in dict_models.Level.objects.all()]
        context['tags'] = [TagSerizlizer(instance=tag).data for tag in dict_models.Tag.objects.all()]
        context['learning_mods'] = [LearningModeSerizlizer(instance=mode).data for mode in dict_models.LearningMode.objects.all()]
        return context

    @method_decorator(csrf_protect)
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs, request=request)
        return self.render_to_response(context)

    @method_decorator(csrf_protect)
    @method_decorator(login_required)
    def post(self, request, *args, id=None, **kwargs):
        instance = None
        if id:
            try:
                instance = dict_models.Dictionary.objects.get(id=id)
            except dict_models.Dictionary.DoesNotExist:
                raise Http404()

        form = DictionaryForm(request.POST, instance=instance)
        if form.is_valid():
            dict = form.save(commit=False)
            dict.owner = request.user
            form.save()
            return redirect(f'/dictionary/{form.instance.id}/update/')

        context = self.get_context_data(**kwargs, request=request)
        context["form"] = form
        context["words"] = [WordForm(instance=word) for word in form.instance.words.filter(active=True)] \
            if form.instance.id else []
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
        context['words'] = [WordForm(instance=word) for word in dict.words.filter(active=True)]
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


class DictionaryUpload(TemplateView):
    template_name = 'web/dictionary_upload.html'
    cache = caches['file_uploading']

    def post(self, request, *args, **kwargs):
        import json
        if request.POST.get('type') == 'file':
            form = DictUploadForm(request.POST, request.FILES)
            if not form.is_valid():
                return render(request, self.template_name, context={"form": form})
            try:
                file = form.cleaned_data['file']
                data = file.read()
                parsed_data = json.loads(data)
            except Exception as ex:
                logger.info(f"error while file parsing {ex}")
                form.errors['file'] = _("Error while file parsing")
                return render(request, self.template_name, context={"form": form, })
            key = str(uuid.uuid4())
            self.cache.set(key, data, timeout=5 * 60)
            return render(request, self.template_name, context={
                "form": form,
                "parsed": {
                    "data_example": parsed_data[0],
                    "key": key
                }
            })

        form = DictSelectForm(request.POST)
        if not form.is_valid():
            return render(request, self.template_name, context={"form": form})


        key = form.cleaned_data["key"]
        data = self.cache.get(key)
        parsed_data = json.loads(data)
        return render(request, self.template_name, context={
            "form": form,
            "parsed": {
                "data_example": parsed_data[0],
                "key": form.cleaned_data["key"]
            }
        })
