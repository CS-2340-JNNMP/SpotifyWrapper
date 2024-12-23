from . import views
from django.urls import path

from .views import spotify_login, spotify_callback
from .views import GenreAnalysisView
from accounts.views import callback, wrapped_page
urlpatterns = [
path('translate/', views.translate_text, name='translate_text'),
    # path('login/', views.login, name='login'),  # Reference your login_user function here
    path('register_user/', views.register_user, name='register_user'),
    # path('profile/', views.profile, name='profile'),
    # path('logout/', views.logout_user, name='logout'),
    path('', views.index, name='index'),
    # path('login/', views.login_view, name='login'),
    path('login/', views.login_function, name='login'),
    # path('register/', views.register_view, name='register'),
    path('password-reset/', views.password_reset_view, name='password_reset'),
    path('my-wraps/', views.my_wraps_view, name='my_wraps'),
    path('generate/', views.generate_view, name='generate'),
    path('wrapped-page/', views.wrapped_page_view, name='wrapped_page'),
    path('spotify/login/', spotify_login, name='spotify_login'),

    # path('login/', views.login_user, name='login'),  # Reference your login_user function here
    path('register_user/', views.register_user, name='register_user'),
    path('music_analysis/', GenreAnalysisView.as_view(), name='music_analysis'),
    path('spotify/callback/', callback, name='spotify_callback'),
    path('spotify/user-data/', views.get_user_data, name='spotify_user_data'),
    path('index/', views.index, name='index'),
    path('game/', views.game, name='game'),

    path('wrapped-page/<uuid:wrap_id>/', views.wrapped_page_with_id, name='wrapped_page'),

    path('register/', views.register_function, name='register'),
    # path('register/', views.register_member, name='register'),
    # path('register/', views.register_view, name='register'),

    # path('member/<int:pk>/', views.member_detail, name='member_detail'),
    # path('contact/', views.contact_us, name='contact'),
    path('contact/', views.contact_us, name='contact'),
    path('logout/', views.logout_function, name='logout'),
    path('public_wraps/', views.public_wraps, name='public_wraps'),
    path('wrapped-page-delete/<uuid:wrap_id>/', views.wrapped_page_delete, name='wrapped_page_delete'),
    path('wrapped-page-publish/<uuid:wrap_id>/', views.wrapped_page_publish, name='wrapped_page_publish'),
    path('delete_account/', views.delete_account, name='delete_account'),
]

