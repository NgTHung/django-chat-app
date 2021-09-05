from django.urls import path
from django.views.generic.base import TemplateView
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", TemplateView.as_view(template_name="./home.html"), name="home"),
    path("login/", views.login, name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="/"), name="logout"),
    path("register/", views.register),
    path("forget/", views.forget),
    path("chat/r/<str:room>/", views.chat),
    path("chat/", views.wrong),
    path("chat/r/", views.wrong),
    # path('logn/',views.logn),
    # path('sign_up/',views.sign_up),
]
