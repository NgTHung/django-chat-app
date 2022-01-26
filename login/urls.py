from django.urls import path
from django.views.generic.base import TemplateView, View
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("", TemplateView.as_view(template_name="./home.html"), name="home"),
    path("login/", views.login, name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="/"), name="logout"),
    path("register/", views.register),
    path("forget/", views.forget),
    path("chat/r/<str:room>/", views.chat, name='chat'),
    path("chat/", views.wrong),
    path("chat/r/", views.wrong),
    path(".well-known/acme-challenge/<str:file>/", views.acme),
    path(".well-known/pki-validation/<str:file>/",views.acme),
    # path('logn/',views.logn),
    # path('sign_up/',views.sign_up),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
