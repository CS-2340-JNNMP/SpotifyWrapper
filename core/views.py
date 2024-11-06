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
from django.contrib.auth.models import User
from django.utils.translation import activate

from django.shortcuts import redirect
from django.utils import translation
from django.utils.translation import activate
from django.shortcuts import render
from django.utils import translation
from django.shortcuts import redirect
from django.urls import translate_url
from django.utils.translation import gettext as _


from django.shortcuts import render, redirect

from googletrans import Translator

def home(request):
    translator = Translator()

    # Get the current language from the session or default to 'en'
    current_language = request.session.get('current_language', 'en')

    # Translate the content
    welcome_message = translator.translate('Welcome to my website', dest=current_language).text
    language_toggle = translator.translate('Switch to %(language)s', dest=current_language, src='en').text % {'language': 'French' if current_language == 'en' else 'English'}

    context = {
        'welcome_message': welcome_message,
        'language_toggle': language_toggle,
    }

    return render(request, 'home.html', context)

def change_language(request):
    # Get the current language from the session or default to 'en'
    current_language = request.session.get('current_language', 'en')

    # Toggle the language
    new_language = 'fr' if current_language == 'en' else 'en'
    request.session['current_language'] = new_language

    return redirect('home')


def index(request):
    return render(request, "core/index.html")



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

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)  # Redirect to success page
            return redirect('profile')
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('login')
    else:
        return render(request, 'core/login.html', {})

def logout_user(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('index')


class UserCreationFormWrapper(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(UserCreationFormWrapper, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-styles'})



def register_user(request):
    if request.method == 'POST':
        form = UserCreationFormWrapper(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Registration successful!')
                return redirect('profile')
    else:
        form = UserCreationFormWrapper()
    return render(request, 'core/register_user.html', {'form' : form})
def sign_up(request):
    return render(request, "core/sign_up.html")
from django.contrib.auth.decorators import login_required

@login_required
def profile(request):
    return render(request, 'core/profile.html', {'user': request.user})

def contact(request):
    return render(request, "core/contact.html")
