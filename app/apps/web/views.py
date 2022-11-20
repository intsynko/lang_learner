from django.views.generic import TemplateView


class MainPage(TemplateView):
    template_name = "web/main_page.html"


class LoginPage(TemplateView):
    template_name = "web/login_page.html"
