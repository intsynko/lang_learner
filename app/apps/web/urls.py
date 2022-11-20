from django.urls import path

from apps.web.views import MainPage, LoginPage

urlpatterns = [
    path('', MainPage.as_view(), name="main"),
    path('login/', LoginPage.as_view(), name="login")
]

app_name = "web"
