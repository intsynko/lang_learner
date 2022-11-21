from django.contrib.auth import views as auth_views


class LoginPage(auth_views.LoginView):
    redirect_authenticated_user = True
    template_name = "web/login_page.html"
