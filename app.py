import time
from typing import List, Any

import pandas as pd
from bs4 import element

from flask import Flask, request, url_for, session, redirect
import spotipy
import spotipy.util as util
from spotipy import SpotifyOAuth

app = Flask(__name__)
app.secret_key = "BLs029sjO1"
app.config['SESSION_COOKIE_NAME'] = 'Session Cookie 1'
TOKEN_INFO = "token_info"


@app.route('/')
def login():
    sp = spotify_oauth()
    auth_url = sp.get_authorize_url()
    return redirect(auth_url)


@app.route('/redirect')
def redirectUser():
    sp = spotify_oauth()
    session.clear()
    code = request.args.get('code')
    token_info = sp.get_access_token(code)
    session[TOKEN_INFO] = token_info
    return redirect(url_for('genres', _external=True))


def get_token():
    token_info = session.get(TOKEN_INFO, None)
    if not token_info:
        raise "exception"
    now = int(time.time())

    is_expired = token_info['expires_at'] - now < 60
    if is_expired:
        sp = spotify_oauth()
        token_info = sp.refresh_access_token(token_info['refresh_token'])
    return token_info


@app.route('/genres')
def genres():
    try:
        token_info = get_token()
    except:
        print("Please login")
        return redirect("/")

    sp_launch = spotipy.Spotify(auth=token_info['access_token'])
    i = 0
    genre_list = []
    track_genre_list = []

    # loops through your last 30 liked songs and gets the genres of each
    while i < 30:
        track = sp_launch.current_user_saved_tracks(limit=50, offset=0)['items'][i]
        artist = sp_launch.artist(track['track']['album']["artists"][0]["external_urls"]["spotify"])
        genre_list += artist['genres']
        i += 1
        track_genre_list.append([track['track']['id'], artist['genres']])

    # remove duplicates in list
    updated_g_list = pd.unique(genre_list).tolist()

    for index, genre in enumerate(updated_g_list):
        print(f"{index + 1}- {genre}")

    # gets the genre that the user wants
    genre_index = (input("What genre should your new playlist be? "))
    seed_genre = updated_g_list[int(genre_index) - 1]

    def find_match(seed):  # searches the list in the second column of each row for a match
        temporary_list = []
        i = 0
        while i in range(len(track_genre_list)):
            temporary_list += track_genre_list[i][1]  # creating new list from 2d array
            i += 1
            j = 0  # resetting j to zero
            while j in range(len(temporary_list)):
                if temporary_list[j] == seed:  # searching list for the genre
                    return temporary_list
                j += 1
            temporary_list.clear()  # clearing list for next entry (only one entry at a time)
        return 'could not find match'

    search_2 = find_match(seed_genre)

    def find_id(list):  # takes in search_2 and returns the corresponding id
        i = 0
        while i in range(len(track_genre_list)):
            if list == track_genre_list[i][1]:
                return track_genre_list[i][0]
            else:
                i += 1
        return 'could not find match'

    track_id = find_id(search_2)
    formatted_id = ['spotify:track:' + track_id]
    recommended_tracks = sp_launch.recommendations(None, seed_genre, formatted_id, 10, None)
    username = input('What is your spotify username?\n')
    name = input('What should I name your playlist?\n')
    new_playlist_id = sp_launch.user_playlist_create(username, name, True, False, "")['id']
    #TO DO add recommended tracks to playlist
    return str(recommended_tracks)


# Spotify object
def spotify_oauth():
    return SpotifyOAuth(
        client_id= "Client Id",
        client_secret="Client Secret",
        redirect_uri=url_for('redirectUser', _external=True),
        scope='user-library-read user-top-read playlist-modify-public')
