from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views


class MainPage(TemplateView):
    template_name = "web/main_page.html"


class LoginPage(auth_views.LoginView):
    redirect_authenticated_user = True
    template_name = "web/login_page.html"
