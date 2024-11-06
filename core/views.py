from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import requests
from django.conf import settings
from urllib.parse import urlencode
from huggingface_hub import InferenceClient
import json
# Create your views here.
from django.contrib.auth.models import User
import requests
from django.views import View
from django import forms

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
    print(settings.SPOTIFY_REDIRECT_URI)
    scope = 'user-read-recently-played'
    # print(settings.CLIENT_ID)
    # print(settings.CLIENT_SECRET)
    # print(settings.SPOTIFY_REDIRECT_URI)
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


# Define your form
class GenreForm(forms.Form):
    genre = forms.CharField(label='Favorite Music Genre', max_length=100)

class GenreAnalysisView(View):
    def get(self, request):
        form = GenreForm()
        return render(request, 'core/music_analysis.html', {'form': form})

    def post(self, request):
        form = GenreForm(request.POST)
        if form.is_valid():
            genre = form.cleaned_data['genre']
            result = self.call_hugging_face(genre)
            return render(request, 'core/music_analysis.html', {'form': form, 'result': result})
        return render(request, 'core/music_analysis.html', {'form': form})

    def call_hugging_face(self, genre):
        llm_client = InferenceClient(
            model="microsoft/Phi-3-mini-4k-instruct",
            timeout=120,
        )
        response = llm_client.post(
            json={
                "inputs": f"Describe how people feel, think, and dress when they listen to {genre} music. Be creative and provide detailed insights.",
                "parameters": {"max_new_tokens": 300, "temperature": 0.9},
                "task": "text-generation",
            },
        )
        response_text = json.loads(response.decode())[0]["generated_text"]

        # Initialize response dictionary
        response_dict = {"feel": "", "think": "", "dress": ""}

        # Define keywords to identify sections
        feel_keywords = ["feel", "emotion", "emotionally"]
        think_keywords = ["think", "thoughts"]
        dress_keywords = ["dress", "fashion", "wear"]

        # Split the response into sentences
        sentences = response_text.split('. ')

        for sentence in sentences:
            sentence_lower = sentence.lower()
            if any(keyword in sentence_lower for keyword in feel_keywords):
                response_dict["feel"] += sentence + ' '
            elif any(keyword in sentence_lower for keyword in think_keywords):
                response_dict["think"] += sentence + ' '
            elif any(keyword in sentence_lower for keyword in dress_keywords):
                response_dict["dress"] += sentence + ' '

        # Clean up any trailing spaces
        for key in response_dict:
            response_dict[key] = response_dict[key].strip()

        return response_dict

        # headers = {
        #     'Authorization': f'Bearer {"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"}',
        #     'Content-Type': 'application/json'
        # }
        # model = "gpt2"  # or any other model from Hugging Face
        # url = f"https://api.huggingface.co/gpt2"
        #
        # data = {
        #     "inputs": f"What do people usually feel, think, and dress like if they listen to {genre} music?"
        # }
        #
        # response = requests.post(url, headers=headers, json=data)
        # if response.status_code == 200:
        #     return response.json()[0]['generated_text']  # Adjust based on the response structure
        # else:
        #     print(response.status_code, response.text)  # Log the error response
        # return "Error: Could not retrieve data."

def home(request):
    return render(request, "core/home.html")
