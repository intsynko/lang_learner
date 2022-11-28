from django.urls import path
from django.contrib.auth import views as auth_views

from apps.web.views.main import MainPage
from apps.web.views.auth import  LoginPage
from apps.web.views import dictionary as dictionary_views

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
    path('dictionary/', dictionary_views.DictionaryPage.as_view(), name="dictionary"),
    path('dictionary/create/', dictionary_views.DictionaryCreatePage.as_view(), name="dictionary-pin"),
    path('dictionary/<int:id>/', dictionary_views.DictionaryDetailPage.as_view(), name="dictionary-detail"),
    path('dictionary/<int:id>/pin/', dictionary_views.DictionaryPin.as_view(), name="dictionary-pin"),
    path('dictionary/<int:id>/unpin/', dictionary_views.DictionaryUnpin.as_view(), name="dictionary-unpin"),
    path('dictionary/<int:id>/update/', dictionary_views.DictionaryUpdatePage.as_view(), name="dictionary-update"),
    path('dictionary/<int:id>/remove/', dictionary_views.DictionaryRemovePage.as_view(), name="dictionary-remove"),

    path('word/create/', dictionary_views.WordCreatePage.as_view(), name="word-create"),
    path('word/<int:id>/delete/', dictionary_views.WordDeletePage.as_view(), name="word-delete"),

    path('htmx/dictionary/<int:id>/word/', dictionary_views.word_template, name="word-form"),
]

app_name = "web"
