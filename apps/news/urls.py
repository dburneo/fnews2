from django.urls import path, include
from django.contrib import admin
from django.conf.urls import url, include
# from smarturls import surls
from django.contrib.auth import views as auth_views

from apps.news import views as news_views

urlpatterns = [
    path('', news_views.home, name="home"),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='registration/logout.html'), name='logout'),     # OK, pero con el logout de admin
    path('signup/', news_views.signup, name='signup'),
    path('settings/', news_views.settings, name='settings'),
    path('settings/password/', news_views.password, name='password'),
    path('accounts/profile/', news_views.profile, name='profile'),
    path('oauth/', include('social_django.urls', namespace='social')),
]
