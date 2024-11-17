from . import views
from django.urls import path

from .views import spotify_login, spotify_callback
from .views import GenreAnalysisView
from accounts.views import callback

urlpatterns = [
    # path('login/', views.login_user, name='login'),  # Reference your login_user function here
    # path('register_user/', views.register_user, name='register_user'),
    # path('profile/', views.profile, name='profile'),
    # path('logout/', views.logout_user, name='logout'),
    path('login/', views.login_user, name='login'),  # Reference your login_user function here
    path('register_user/', views.register_user, name='register_user'),
    path('spotify/login/', spotify_login, name='spotify_login'),
    path('music_analysis/', GenreAnalysisView.as_view(), name='music_analysis'),
    path('spotify/callback/', callback, name='spotify_callback'),
    path('spotify/user-data/', views.get_user_data, name='spotify_user_data'),
    path('index/', views.index, name='index'),
    path('game/', views.game, name='game')

]

