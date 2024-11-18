import requests
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.conf import settings
from urllib.parse import urlencode


def login(request):
    # Construct the Spotify authorization URL
    params = {
        "client_id": settings.CLIENT_ID,
        "response_type": "code",
        "redirect_uri": settings.SPOTIFY_REDIRECT_URI,
        "scope": settings.SCOPE,
    }
    auth_url = f"https://accounts.spotify.com/authorize?{urlencode(params)}"
    print(f"Authorization URL: {auth_url}")
    return HttpResponseRedirect(auth_url)


def callback(request):
    # Get the authorization code from the callback
    code = request.GET.get("code")

    if not code:
        return JsonResponse({"error": "Authorization code not provided."}, status=400)

    # Exchange the authorization code for an access token
    token_url = "https://accounts.spotify.com/api/token"
    payload = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": settings.SPOTIFY_REDIRECT_URI,
        "client_id": settings.CLIENT_ID,
        "client_secret": settings.CLIENT_SECRET,
    }
    response = requests.post(token_url, data=payload)

    if response.status_code != 200:
        return JsonResponse({"error": "Failed to retrieve access token."}, status=response.status_code)

    token_info = response.json()
    access_token = token_info.get("access_token")

    # Store the access token securely (e.g., in a session)
    request.session["access_token"] = access_token
    return HttpResponseRedirect("/accounts/profile")


def get_top_tracks(request):
    if request.method == 'GET':
        # Get the access token from the session
        access_token = request.session.get("access_token")
        if not access_token:
            return JsonResponse({"error": "Access token not found."}, status=401)

        # Make the request to the Spotify API
        headers = {"Authorization": f"Bearer {access_token}"}
        top_tracks_url = "https://api.spotify.com/v1/me/top/tracks"
        params = {"limit": 5, "offset": 0, "time_range": "long_term"}
        response = requests.get(top_tracks_url, headers=headers, params=params)

        if response.status_code != 200:
            return JsonResponse({"error": "Failed to retrieve top tracks."}, status=response.status_code)

        # Parse the response and extract top tracks
        top_tracks = response.json().get("items", [])
        tracks = [
            {
                "image": track["album"]["images"][0]["url"] if track["album"]["images"] else None,
                "name": track["name"],
                "artist": track["artists"][0]["name"] if track["artists"] else "Unknown Artist",
                "album": track["album"]["name"],
            }
            for track in top_tracks
        ]

        print(f"Top Tracks: {tracks}")
        return render(request, 'accounts/profile.html', {'tracks': tracks})

    else:
        return JsonResponse({"error": "Invalid request method."}, status=405)
