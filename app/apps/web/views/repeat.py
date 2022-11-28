from django.shortcuts import render, redirect
from django.views.generic import TemplateView

from services.learning_mode import LearningModeService, Answer


learning_service = LearningModeService()


def repeat(reqeust, id):
    session = learning_service.init_session(reqeust, id)
    return redirect(reqeust.path + str(session) + "/")


class RepeatPage(TemplateView):
    def get(self, request, *args, id, session, **kwargs):
        form = learning_service.next(request, session)
        return render(request, "web/learning_page.html", context={"form":form})

    def post(self, request, *args, id, session, **kwargs):
        form = learning_service.next(request, session, Answer(request.POST.get('word'),
                                                              request.POST.get('type'),
                                                              request.POST.get('success') == 'true'
                                                              ))
        return render(request, "web/learning_page.html", context={"form": form})
