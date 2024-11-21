from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.login, name='login'),
    path('callback/', views.callback, name='callback'),
    path('spotify/wrapped-page/', views.wrapped_page, name='wrapped_page'),
    # path('/spotify/callback/', views.callback, name='spotify_callback'),
]
