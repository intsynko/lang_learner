from django.urls import path

from apps.web.views import MainPage

urlpatterns = [
    path('', MainPage.as_view(), name="main"),
]

app_name = "web"
