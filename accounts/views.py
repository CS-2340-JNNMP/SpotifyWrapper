import spotipy
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from spotipy import SpotifyOAuth

from django.conf import settings


def login(request):
    # Create a SpotifyOAuth object
    sp_oauth = SpotifyOAuth(client_id=settings.CLIENT_ID, client_secret=settings.CLIENT_SECRET, redirect_uri=settings.SPOTIFY_REDIRECT_URI, scope = settings.SCOPE)

    # Print the sp_oauth object to the console
    print("\n\nSP_OAuth Object:" ,sp_oauth, "\n\n")

    # Redirect the user to the Spotify login page
    # Get the authorization URL
    url = sp_oauth.get_authorize_url()
    # Print the authorization url to the console
    print(url)

    # Redirect the user to the Spotify login page
    return HttpResponseRedirect(url)

def callback(request):
    # Create a SpotifyOAuth object
    sp_oauth = SpotifyOAuth(client_id=settings.CLIENT_ID, client_secret=settings.CLIENT_SECRET, redirect_uri=settings.SPOTIFY_REDIRECT_URI, scope=settings.SCOPE)

    # Get the authorization code from the query parameters
    code = request.GET.get("code")

    # Request an access token using the authorization code
    token_info = sp_oauth.get_access_token(code)

    # Extract the access token
    access_token = token_info["access_token"]

    # Store the access token in a secure way (e.g. in a session or database)
    request.session["access_token"] = access_token

    # Redirect the user to the top tracks page
    return HttpResponseRedirect("/accounts/profile")

def get_top_tracks(request):
    if request.method == 'GET':
        # Get the access token from the session
        access_token = request.session.get("access_token")
        print('\n\n ACCESS TOKEN: ', access_token, '\n\n')

        # Create a Spotipy client using the access token
        sp = spotipy.Spotify(auth=access_token)

        print('\n\n ACCESS TOKEN: ', access_token, '\n\n')

        # retrieve the user's profile information
        try:
            response = sp.me()
        except spotipy.exceptions.SpotifyException as e:
            return JsonResponse({"error": str(e)})

        if response is not None:
            # The access token is valid
            print("The access token is valid.\n\n")
        else:
            # The access token is invalid or has expired
            print("The access token is invalid or has expired.\n\n")

        # Make the HTTP GET request
        response = sp.current_user_top_tracks(limit=5, offset=0, time_range="long_term")

        # Extract the top tracks from the response
        top_tracks = response["items"]

        tracks = []
        for track in top_tracks:
            track_info = {
                "name": track["name"],
                "artist": track["artists"][0]["name"],
                "album": track["album"]["name"],
            }
            tracks.append(track_info)

        # print tracks list to console
        print("\n\n\nLIST OF TRACKS:",tracks)

        return render(request, 'accounts/profile.html', {'tracks': tracks})

        # Return a JSON response containing the top tracks
        # return JsonResponse(tracks, safe=False)

    else:
        error = "An error has occurred"
        return error