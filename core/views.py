from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import requests
from django.conf import settings
from urllib.parse import urlencode
# Create your views here.

def index(request):
    return render(request, 'core/index.html')

def login_view(request):
    # if request.method == 'POST':
    #     email = request.POST.get('email')
    #     password = request.POST.get('password')
    #     user = authenticate(request, username=email, password=password)
    #     if user is not None:
    #         login(request, user)
    #         return redirect('home')
    return render(request, 'core/login.html')

def register_view(request):
    return render(request, "core/register.html")

def password_reset_view(request):
    return render(request, "core/index.html")

def my_wraps_view(request):
    return render(request, "core/my_wraps.html")

def generate_view(request):
    return render(request, "core/generate.html")

def wrapped_page_view(request):
    # This is where you'd get data from your library
    # Example data structure:
    data = {
        'songs': [
            'Dancing in the Moonlight - Stellar Dreams',
            'Midnight Symphony - The Echo Chamber',
            'Neon Nights - Crystal Cascade'
        ],
        'artists': [
            'The Echo Chamber',
            'Stellar Dreams',
            'Crystal Cascade'
        ],
        'genres': [
            'Electronic',
            'Indie Rock',
            'Synthwave'
        ]
    }
    return render(request, "core/wrapped-page.html", {'data': data})

def spotify_login(request):
    scope = 'user-read-recently-played'
    auth_query = {
        'response_type': 'code',
        'client_id': settings.CLIENT_ID,
        'scope': scope,
        'redirect_uri': settings.SPOTIFY_REDIRECT_URI,
    }
    url = 'https://accounts.spotify.com/authorize?' + urlencode(auth_query)
    return redirect(url)


def spotify_callback(request):
    code = request.GET.get('code')
    token_url = 'https://accounts.spotify.com/api/token'

    payload = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': settings.SPOTIFY_REDIRECT_URI,
        'client_id': settings.CLIENT_ID,
        'client_secret': settings.CLIENT_SECRET,
    }

    response = requests.post(token_url, data=payload)
    token_data = response.json()

    # Store token_data['access_token'] for future API calls
    return JsonResponse(token_data)

def get_user_data(request):
    access_token = request.session.get('access_token')
    headers = {
        'Authorization': f'Bearer {access_token}',
    }
    response = requests.get('https://api.spotify.com/v1/me/player/recently-played', headers=headers)
    return JsonResponse(response.json())
