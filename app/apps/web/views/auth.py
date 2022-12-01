from django.contrib.auth import views as auth_views, login
from django.shortcuts import redirect, render
from django.views.generic import TemplateView

from apps.web.forms import RegistrationForm


class LoginPage(auth_views.LoginView):
    redirect_authenticated_user = True
    template_name = "web/login_page.html"


class RegistrationPage(TemplateView):
    template_name = 'web/registration.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = RegistrationForm()
        return context

    def post(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')

        context = self.get_context_data(**kwargs)
        context['form'] = form
        return render(request, self.template_name, context)
