import requests
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.conf import settings
from urllib.parse import urlencode, parse_qs

from firebase import firestore_db
import uuid

def login(request):
    # Construct the Spotify authorization URL
    duration = request.GET.get("duration", "long_term")
    params = {
        "client_id": settings.CLIENT_ID,
        "response_type": "code",
        "redirect_uri": settings.SPOTIFY_REDIRECT_URI,
        "scope": settings.SCOPE,
        "state": f"duration={duration}",
    }
    auth_url = f"https://accounts.spotify.com/authorize?{urlencode(params)}"
    print(f"Authorization URL: {auth_url}")
    return HttpResponseRedirect(auth_url)


def callback(request):

    code = request.GET.get("code")
    state = request.GET.get("state")

    if state:
        state_params = parse_qs(state)
        duration = state_params.get("duration", ["long_term"])[0]
    else:
        duration = "long_term"

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
    request.session["duration"] = duration
    return HttpResponseRedirect('wrapped-page')
    # return HttpResponseRedirect("/accounts/profile")

def wrapped_page(request):
    access_token = request.session.get("access_token")
    duration = request.session.get("duration", "long_term")
    print(duration)

    if not access_token:
        return JsonResponse({"error": "Access token not found."}, status=401)

    headers = {"Authorization": f"Bearer {access_token}"}
    top_tracks_url = "https://api.spotify.com/v1/me/top/tracks"
    top_artists_url = "https://api.spotify.com/v1/me/top/artists"

    # Fetch top tracks
    tracks_response = requests.get(
        top_tracks_url, headers=headers, params={"limit": 5, "time_range": duration}
    )

    # Fetch top artists
    artists_response = requests.get(
        top_artists_url, headers=headers, params={"limit": 5, "time_range": duration}
    )

    if tracks_response.status_code != 200 or artists_response.status_code != 200:
        return JsonResponse({"error": "Failed to retrieve Spotify data."}, status=500)

    # Parse the responses
    tracks_data = tracks_response.json().get("items", [])
    artists_data = artists_response.json().get("items", [])

    # Extract required fields
    top_songs = [track["name"] for track in tracks_data[:3]]
    top_song_image = tracks_data[0]["album"]["images"][0]["url"] if tracks_data[0]["album"]["images"] else None
    top_artists = [artist["name"] for artist in artists_data[:3]]
    top_artist_image = artists_data[0]["images"][0]["url"] if artists_data[0]["images"] else None
    genres = []

    print(top_song_image)
    print(top_artist_image)
    # Aggregate genres from the top artists
    for artist in artists_data:
        genres.extend(artist.get("genres", []))
    top_genres = list(dict.fromkeys(genres))[:3]  # Get the top 3 unique genres

    # Structure data for the template
    data = {
        "id": str(uuid.uuid4()),
        "songs": top_songs,
        "top_song_image": top_song_image,
        "artists": top_artists,
        "top_artist_image": top_artist_image,
        "genres": top_genres,
    }

    wraps_ref = firestore_db.collection('wraps')
    wraps_ref.add(data)

    return render(request, "core/wrapped-page.html", {"data": data})

def get_top_tracks(request):
    if request.method == 'GET':
        access_token = request.session.get("access_token")
        if not access_token:
            return JsonResponse({"error": "Access token not found."}, status=401)

        headers = {"Authorization": f"Bearer {access_token}"}
        top_tracks_url = "https://api.spotify.com/v1/me/top/tracks"
        params = {"limit": 5, "offset": 0, "time_range": "long_term"}
        response = requests.get(top_tracks_url, headers=headers, params=params)

        if response.status_code != 200:
            error_details = response.json()  # Log the error details
            print(f"Spotify API Error: {error_details}")
            try:
                response_data = response.json()
                print(response.json)
            except ValueError:  # Catch JSON decoding errors
                response_data = {"non_json_response": response.text}
            return JsonResponse({
                "error": "Failed to retrieve Spotify data.",
                "status_code": response.status_code,
                "details": response_data
            }, status=response.status_code)

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
        return JsonResponse({"tracks": tracks})
