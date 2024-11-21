from . import views
from django.urls import path

from .views import spotify_login, spotify_callback
from .views import GenreAnalysisView
from accounts.views import callback, wrapped_page
urlpatterns = [
    # path('login/', views.login, name='login'),  # Reference your login_user function here
    path('register_user/', views.register_user, name='register_user'),
    # path('profile/', views.profile, name='profile'),
    # path('logout/', views.logout_user, name='logout'),
    path('', views.index, name='index'),
    # path('login/', views.login_view, name='login'),
    path('login/', views.login_function, name='login'),
    path('verify_token/', views.verify_token, name='verify_token'),
    # path('register/', views.register_view, name='register'),
    path('password-reset/', views.password_reset_view, name='password_reset'),
    path('my-wraps/', views.my_wraps_view, name='my_wraps'),
    path('generate/', views.generate_view, name='generate'),
    path('wrapped-page/', views.wrapped_page_view, name='wrapped_page'),
    path('spotify/login/', spotify_login, name='spotify_login'),

    path('login/', views.login_user, name='login'),  # Reference your login_user function here
    path('register_user/', views.register_user, name='register_user'),
    path('music_analysis/', GenreAnalysisView.as_view(), name='music_analysis'),
    path('spotify/callback/', callback, name='spotify_callback'),
    path('spotify/user-data/', views.get_user_data, name='spotify_user_data'),
    path('index/', views.index, name='index'),



    path('register/', views.register_function, name='register'),
    # path('register/', views.register_member, name='register'),
    # path('register/', views.register_view, name='register'),

    # path('member/<int:pk>/', views.member_detail, name='member_detail'),
]

