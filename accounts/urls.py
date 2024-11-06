from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.login, name='login'),
    path('callback/', views.callback, name='callback'),
    path('profile/', views.get_top_tracks, name='profile'),
    # path('/spotify/callback/', views.callback, name='spotify_callback'),
]
