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
from firebase_admin.auth import InvalidIdTokenError

from firebase_admin.auth import InvalidIdTokenError
from huggingface_hub import InferenceClient
import json
# Create your views here.
from django.contrib.auth.models import User
import requests
from django.views import View
from django import forms


import firebase_admin
from firebase_admin import auth
from pycparser.ply.yacc import LRTable

from firebase import firestore_db


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
    print("register_view")
    return render(request, "core/register.html")

def password_reset_view(request):
    return render(request, "core/index.html")

def my_wraps_view(request):
    user_id = request.session.get('userID', None)
    wraps_ref = firestore_db.collection('wraps')
    query = wraps_ref.where('user_id', '==', str(user_id))

    results = query.stream()

    items = []
    for doc in results:
        items.append(doc.to_dict())

    images_to_push = []
    wrap_ids = []
    combined = []

    for doc in items:
        images_to_push.append(doc["top_song_image"])
        wrap_ids.append(doc["id"])
        combined.append((doc["top_song_image"], doc["id"], doc["published"]))

    return render(request, "core/my_wraps.html", {"combined": combined})

def generate_view(request):
    logged_in = request.session.get("logged_in", None)
    print(logged_in)
    if logged_in is None or False:
        return render(request, 'core/login.html')

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
    scope = settings.SCOPE
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
    request.session['access_token'] = token_data.get('access_token')
    request.session['refresh_token'] = token_data.get('refresh_token')
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
    print("register_user")
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
    if request.method == "POST":
        fm = UserCreationForm(request.POST)
        if fm.is_valid():
            fm.save()
    else:
        fm = UserCreationForm()
    return render(request, 'enroll/signup.html', {'form':fm})




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

@login_required
def game(request):
    """Homepage to display the top track and preview button."""
    access_token = request.session.get('access_token')
    if not access_token:
        return JsonResponse({'error': 'Access token is missing or invalid'}, status=400)
    headers = {
        'Authorization': f'Bearer {access_token}',
    }

    # Get the user's top track (limit to 1 track)
    response = requests.get('https://api.spotify.com/v1/me/top/tracks?limit=1', headers=headers)



    if response.status_code != 200:
        error_message = response.json() if response.text else "No response content"
        return JsonResponse({'error': 'Failed to fetch top tracks'}, status=400)

    try:
        top_track = response.json()['items'][0]
        track_name = top_track['name']
        track_artists = ', '.join([artist['name'] for artist in top_track['artists']])
        preview_url = top_track.get('preview_url', None)

        if not preview_url:
            return JsonResponse({'error': 'No preview available for the top track'}, status=400)

        return render(request, 'core/home.html', {
            'track_name': track_name,
            'track_artists': track_artists,
            'preview_url': preview_url
        })

    except KeyError:
        return JsonResponse({'error': 'Unexpected response structure from Spotify API'}, status=500)

@login_required
def play_snippet(request):
    """Handle playing the 2-second snippet (frontend will handle actual playback)."""
    preview_url = request.GET.get('preview_url', None)

    if not preview_url:
        return JsonResponse({'error': 'No preview URL provided'}, status=400)

    # Return the preview URL to the frontend for playback
    return JsonResponse({'preview_url': preview_url})












# from django.shortcuts import render, redirect
# from .forms import RegisterForm
# from django.contrib.auth.models import User
#
# def register_member(request):
#     if request.method == "POST":
#         form = RegisterForm(request.POST)
#         if form.is_valid():
#             # Save the member object
#             member = form.save()
#             # Redirect to a new page to display member details
#             return redirect('member_detail', pk=member.pk)
#     else:
#         form = RegisterForm()
#     return render(request, 'core/register.html', {'form': form})
#
#
# from django.shortcuts import get_object_or_404
#
# def member_detail(request, pk):
#     member = get_object_or_404(User, pk=pk)
#     return render(request, 'core/my_wraps.html', {'member': member})




from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegisterForm


def register_function(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            return render(request, 'core/register.html', {'error': 'Passwords do not match'})

        try:
            user = auth.create_user(
                email=email,
                password=password,
            )
            return redirect('login')
        except Exception as e:
            return render(request, 'core/register.html', {'error': str(e)})

    return render(request, 'core/register.html')


# def login_function(request):
#     userid = request.session.get('userID', None)
#     if userid is not None:
#         return redirect('my_wraps')
#
#     if request.method == "POST":
#         email = request.POST.get('email')
#         password = request.POST.get('password')
#
#         try:
#             print("WHY IS THIS NOT WORKING")
#             user = auth.get_user_by_email(email)
#             request.session['userID'] = user.uid
#             request.session["logged_in"] = True
#             return redirect('my_wraps')
#         except Exception as e:
#             return render(request, 'core/login.html', {'error': 'Invalid credentials'})
#
#     return render(request, 'core/login.html')

def login_function(request):
    userid = request.session.get('userID', None)
    if userid is not None:
        return redirect('my_wraps')

    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = verify_password(email, password)
            verified_user = auth.verify_id_token(user["idToken"])
            id = (verified_user["user_id"])
            request.session['userID'] = id
            request.session["logged_in"] = True
            return redirect('my_wraps')
        except Exception as e:
            return render(request, 'core/login.html', {'error': 'Invalid credentials'})

    return render(request, 'core/login.html')

def verify_password(email, password):
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={settings.FIREBASE_WEB_API_KEY}"

    payload = {
        'email': email,
        'password': password,
        'returnSecureToken': True
    }

    response = requests.post(url, json=payload)
    if response.status_code == 200:
        return response.json()  # Successfully authenticated
    else:
        raise Exception("Invalid credentials")

def wrapped_page_with_id(request, wrap_id):
    # Replace 'collection_name' with your collection and 'userId' with the desired user ID.
    collection_ref = firestore_db.collection('wraps')
    query = collection_ref.where('id', '==', str(wrap_id))

    results = query.stream()

    items = []
    for doc in results:
        items.append(doc)

    final = items[0].to_dict()

    return render(request, "accounts/wrapped-page.html", {"data": final})



def contact_us(request):
    if request.method == 'POST':
        print("WHYYYYY ME")
        message = request.POST.get('message')
        print(message)

        if message is None or message.strip() == "":
            return render(request, 'core/contact.html', {'error': 'Please enter your message'})
        # Add the message to Firestore
        print("WHYYYY")
        firestore_db.collection('feedback').add({'content': message})

        # Redirect or render a success message
        return redirect('index')  # Redirect to a success page or show the form again

        # return render(request, 'core/contact.html', {'form': form})

def logout_function(request):
    request.session['logged_in'] = False
    request.session['userID'] = None
    return redirect('index')

def public_wraps(request):
    wraps_ref = firestore_db.collection('wraps')
    query = wraps_ref.where('published', '==', True)

    results = query.stream()

    items = []
    for doc in results:
        items.append(doc.to_dict())

    images_to_push = []
    wrap_ids = []
    combined = []

    for doc in items:
        images_to_push.append(doc["top_song_image"])
        wrap_ids.append(doc["id"])
        combined.append((doc["top_song_image"], doc["id"]))

    return render(request, "core/public_wraps.html", {"combined": combined})

def wrapped_page_delete(request, wrap_id):
    try:
        docs = firestore_db.collection("wraps").where("id", "==", str(wrap_id)).stream()

        for doc in docs:
            doc.reference.delete()
            print(f"Deleted document with ID: {doc.id}")

    except Exception as e:
        print(f"Error deleting documents: {e}")

    return render(request, "core/my_wraps.html")

def wrapped_page_publish(request, wrap_id):
    try:
        docs = firestore_db.collection("wraps").where("id", "==", str(wrap_id)).stream()

        for doc in docs:
            published = doc.to_dict()["published"]
            change = {"published": not published}

            doc.reference.update(change)
            print(f"Updated document ID: {doc.id}")

        print("Update operation completed.")
    except Exception as e:
        print(f"Error updating document(s): {e}")

    return my_wraps_view(request)