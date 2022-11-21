from django.urls import path
from django.contrib.auth import views as auth_views

from apps.web.views.main import MainPage
from apps.web.views.auth import  LoginPage
from apps.web.views.dictionary import DictionaryDetailPage, DictionaryPin, DictionaryPage, DictionaryCreatePage


urlpatterns = [
    path('', MainPage.as_view(), name="main"),
    # path("login/", auth_views.LoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    # path("password_change/", auth_views.PasswordChangeView.as_view(), name="password_change"),
    # path("password_change/done/", auth_views.PasswordChangeDoneView.as_view(), name="password_change_done",),
    # path("password_reset/", auth_views.PasswordResetView.as_view(), name="password_reset"),
    # path("password_reset/done/", auth_views.PasswordResetDoneView.as_view(), name="password_reset_done",),
    # path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm",),
    # path("reset/done/", auth_views.PasswordResetCompleteView.as_view(),name="password_reset_complete",),
    path('login/', LoginPage.as_view(), name="login"),
    path('dictionary/', DictionaryPage.as_view(), name="dictionary"),
    path('dictionary/create/', DictionaryCreatePage.as_view(), name="dictionary-pin"),
    path('dictionary/<int:id>/', DictionaryDetailPage.as_view(), name="dictionary-detail"),
    path('dictionary/<int:id>/pin/', DictionaryPin.as_view(), name="dictionary-pin"),
]

app_name = "web"
